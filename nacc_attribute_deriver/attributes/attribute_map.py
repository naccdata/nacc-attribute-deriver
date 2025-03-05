"""
Defines the attribute mapping
"""
import json

from pathlib import Path
from typing import Any, Callable, Dict, List

from nacc_attribute_deriver.attributes.attribute_collection import (
    AttributeCollection,
    AttributeCollectionRegistry,
    MQTAttribute,
    NACCAttribute,
)

from nacc_attribute_deriver.attributes import mqt, nacc

def discover_collections():
    """There seems to be an issue with walking over python files like
    the plugin example shows due to the way Pants selectively imports
    files (the files "don't exist" if it's not imported to begin with).

    So currently doing the hacky thing where we just go ahead
    and explicitly import everything under mqt/nacc, so we're not really
    "discovering" anything. Ultimately the end result is the same though
    (everything gets imported).
    """
    return AttributeCollectionRegistry.collections


def parse_docs(name: str, docs: str) -> Dict[str, List[str]]:
    """Parses attribute docstrings. Looks for the following blocks
    in Google style at the bottom of the docstring:

        Location:
            List of locations, one per line. Should be in sync with Event
        Operation:
            List of events, one per line. Should be in sync with Location
        Type:
            The type of the attribute, e.g. cross-section, longitudinal, etc.
        Description:
            Description of the attribute
    
    This is pretty hacky and could probably be improved.

    Args:
        name: Name of the function being evaluated
        docs: The docs from the function being evaluated
    """
    doc_parts = [x.strip() for x in docs.split('\n')]
    results = {
        'Location:': [],
        'Operation:': [],
        'Type:': [],
        'Description:': []
    }

    cur_str = None
    for part in doc_parts:
        if not part:
            continue

        if part in results:
            cur_str = results[part]
        elif cur_str is not None:
            cur_str.append(part)

    if len(results['Location:']) != len(results['Operation:']):
        raise ValueError(f"Function {name} has inconsistent location/event")

    for k, v in results.items():
        if not v:
            raise ValueError(f"Function {name} missing docstring for {k}")

    return results


def generate_attribute_schema(outfile: Path = None,
                              date_key: str = 'file.info.forms.json.visitdate',
                              collections: List[AttributeCollection] = None) -> Dict[str, Any]:
    """Generates a skeleton curation schema for every attribute
    and writes results to JSON.

    Args:
        outfile: File to write schema to
        date_key: Schema date key, defaults to
            file.info.forms.json.visitdate
    """
    def evaluate_grouping(grouping: List[AttributeCollection]) -> List[Dict[str, Any]]:
        schema = []
        for collection in grouping:
            for name, func in collection.get_all_hooks().items():
                # parse type and description from docstring
                results = parse_docs(name, func.__doc__)
                
                # skip intermediate variables
                if 'intermediate' in results['Type:']:
                    continue

                schema.append({
                    'function': name,
                    # TODO - need to change docstring name to operation
                    'events': [{'location': results['Location:'][i], 'operation': results['Operation:'][i]}
                               for i in range(len(results['Location:']))],
                    'type': ' '.join(results['Type:']),
                    'description': ' '.join(results['Description:'])
                })
        return schema

    if not collections:
        collections = discover_collections()

    nacc_vars = []
    mqt_vars = []

    for c in collections:
        if issubclass(c, NACCAttribute):
            nacc_vars.append(c)
        else:
            mqt_vars.append(c)

    result = {
        'date_key': date_key,
        'nacc_derived_vars': evaluate_grouping(nacc_vars),
        'mqt_derived_vars': evaluate_grouping(mqt_vars)
    }

    if outfile:
        with outfile.open('w') as fh:
            json.dump(result, fh, indent=4)

    return result
