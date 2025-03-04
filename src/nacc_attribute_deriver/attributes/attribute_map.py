"""
Collects all _create functions into a single map
"""
import re
import json
from inspect import isfunction, ismodule
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple
from types import ModuleType

from nacc_attribute_deriver.attributes import mqt, nacc


def generate_attribute_map(modules: List[ModuleType]) -> Dict[str, Callable]:
    """Recursively generates mapping of attributes to functions given the
    list of Python modules. Searches for all callables that start
    with _create. Key name is the function name without the leading
    underscore.

    Assumes no name clashes.

    Args:
        modules: Python moduules to iterate over
    """
    result = {}
    for module in modules:
        submodules = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isfunction(attr) and attr_name.startswith('_create_'):
                if attr_name in result:
                    raise ValueError(f"Duplicate create function name: {attr_name}")
                result[attr_name.lstrip('_')] = attr
            elif ismodule(attr):
                submodules.append(attr)

        if submodules:
            result.update(generate_attribute_map(submodules))

    return result


ATTRIBUTE_MAP = generate_attribute_map([nacc, mqt])


def parse_docs(name: str, docs: str) -> Dict[str, List[str]]:
    """Parses attribute docstrings. Looks for the following blocks
    in Google style at the bottom of the docstring:

        Location:
            List of locations, one per line. Should be in sync with Event
        Event:
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
        'Event:': [],
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

    if len(results['Location:']) != len(results['Event:']):
        raise ValueError(f"Function {name} has inconsistent location/event")

    return results


def generate_attribute_schema(outfile: Path,
                              date_key: str = 'file.info.forms.json.visitdate') -> None:
    """Generates a skeleton curation schema for every attribute
    and writes results to JSON.

    Args:
        outfile: File to write schema to
        date_key: Schema date key, defaults to
            file.info.forms.json.visitdate
    """
    def evaluate_grouping(grouping: Dict[str, Callable]) -> List[Dict[str, Any]]:
        schema = []
        for i, (name, function) in enumerate(grouping.items()):
            # parse type and description from docstring
            docs = function.__doc__
            results = parse_docs(name, function.__doc__)
            
            # skip intermediate variables
            if 'intermediate' in results['Type:']:
                continue

            schema.append({
                'function': name,
                'events': [{'location': results['Location:'][i], 'event': results['Event:'][i]}
                           for i in range(len(results['Location:']))],
                'type': ' '.join(results['Type:']),
                'description': ' '.join(results['Description:'])
            })
        return schema

    nacc_vars = generate_attribute_map([nacc])
    mqt_vars = generate_attribute_map([mqt])

    result = {
        'date_key': date_key,
        'nacc_derived_vars': evaluate_grouping(nacc_vars),
        'mqt_derived_vars': evaluate_grouping(mqt_vars)
    }

    with outfile.open('w') as fh:
        json.dump(result, fh, indent=4)
