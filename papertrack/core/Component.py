

from typing import Collection
from functools import partial

_DOWNLOADERS = [] 
_COLLECTORS = []
_VIEWERS = [] 

def register_downloader(cls):
    _DOWNLOADERS.append(cls)
    return cls


def register_collector(cls):
    _COLLECTORS.append(cls)
    return cls


def register_viewer(cls):
    _VIEWERS.append(cls)
    return cls

def simple_ask_fn(name, param_type, description, choices: list) -> str:
    value = None
    while value is None:
        if choices and len(choices) > 0:
            print("%s (%s)" % (name, description))
            for i,c in enumerate(choices):
                print(" > %d %s" % (i+1, c))
            try:
                value = int(input("Selection >"))
                value = choices[value - 1]
            except:
                value = None
        else:
            print("%s (%s)" % (name, description),)
            value = input("> ")
    return value


def _convert_type(value, type):
    if type in ["str", "string"]:
        return str(value)
    elif type in ["int", "integer", "number"]:
        return int(value)
    elif type in ["bool", "boolean"]:
        return bool(value)
    else:
        raise TypeError("Wrong type")

def _get_component_class(name, type):
    components = None
    if type == "downloader":
        components = _DOWNLOADERS
    elif type == "collector":
        components = _COLLECTORS
    elif type == "viewer":
        components = _VIEWERS
    else:
        raise TypeError("Wrong type of component. Contact developer to resolve this.")
    result = None
    for component in components:
        if component.name == name:
            result = component
    if not result:
        raise ValueError("Component with name %s not found" % name)
    return result

def _get_component_instance(name, ask_param_fn, type, **params):
    result = _get_component_class(name, type)
    config = {}
    for param, definition in result.params.items():
        if "default" not in definition and param not in params:
            value = ask_param_fn(
                param, 
                definition.get("type", "string"), 
                definition.get("description", ""), 
                definition.get("choices", [])
            )
            config[param] = _convert_type(value, definition.get("type", "string"))
        elif "default" in definition and param not in params:
            config[param] = _convert_type(value, definition["type"])
        else:
            config[param] = _convert_type(value, params[param])
    return result(**config)
    
get_downloader_instance = partial(_get_component_instance,  type="downloader")
get_collector_instance = partial(_get_component_instance,  type="collector")
get_viewer_instance = partial(_get_component_instance,  type="viewer")



