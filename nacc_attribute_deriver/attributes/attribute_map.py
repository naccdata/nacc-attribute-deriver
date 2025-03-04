"""
Defines the attribute mapping
"""
import json

from inspect import isclass, ismodule
from pathlib import Path
from typing import Any, Callable, Dict, List
from types import ModuleType

import nacc_attribute_deriver.attributes.mqt as mqt
import nacc_attribute_deriver.attributes.nacc as nacc
from .attribute_collection import AttributeCollection


def generate_attribute_map(modules: List[ModuleType]) -> Dict[str, Dict[str, Callable]]:
    """Recursively generates mapping of attributes to attribute class/functions
    given the list of Python modules. Only considers classes of type AttributeCollection
    so that it can call collect_attributes on it. Assumes no name clashes.

    Args:
        modules: The Python modules to iterate over
    """
    result = {}
    for module in modules:
        submodules = []
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isclass(attr) and issubclass(attr, AttributeCollection):
                subattrs = attr.collect_attributes()

                # make sure no duplicate function names
                for name, func in subattrs.items():
                    if name in result:
                        if func != result[name]:
                            raise ValueError(f"Duplicate create function name '{name}'. "
                                + f"Defined as both {func} and {result[name]}")
                        continue
                    result[name] = func
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

    for k, v in results.items():
        if not v:
            raise ValueError(f"Function {name} missing docstring for {k}")

    return results


def generate_attribute_schema(outfile: Path = None,
                              date_key: str = 'file.info.forms.json.visitdate') -> Dict[str, Any]:
    """Generates a skeleton curation schema for every attribute
    and writes results to JSON.

    Args:
        outfile: File to write schema to
        date_key: Schema date key, defaults to
            file.info.forms.json.visitdate
    """
    def evaluate_grouping(grouping: Dict[str, Callable]) -> List[Dict[str, Any]]:
        schema = []
        for i, (name, source) in enumerate(grouping.items()):
            # parse type and description from docstring
            results = parse_docs(name, source['function'].__doc__)
            
            # skip intermediate variables
            if 'intermediate' in results['Type:']:
                continue

            schema.append({
                'attribute': name,
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

    if outfile:
        with outfile.open('w') as fh:
            json.dump(result, fh, indent=4)

    return result
