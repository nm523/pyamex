import re

def clean_key(name):
    """
    camelCase to camel_case
    https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def to_list(obj):
    """
    Wraps an object in a list if it's not already one
    """
    if isinstance(obj, list):
        return obj
    return [obj]