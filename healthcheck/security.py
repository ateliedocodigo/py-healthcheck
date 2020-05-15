try:
    from collections.abc import Mapping  # only works on python 3.3+
except ImportError:
    from collections import Mapping


def safe_dict(dictionary, blacklist=('key', 'token', 'pass'), max_deep=5):
    """ Avoid listing passwords and access tokens or keys in the dictionary

    :param dictionary: Input dictionary
    :param blacklist: blacklist keys
    :param max_deep: Maximum dictionary dict iteration
    :return: Safe dictionary
    """
    if max_deep <= 0:
        return dictionary
    result = {}
    for key in dictionary.keys():
        if isinstance(dictionary[key], Mapping):
            result[key] = safe_dict(dictionary[key], blacklist, max_deep - 1)
        elif any([b in key.lower() for b in blacklist]):
            result[key] = "********"
        else:
            result[key] = dictionary[key]
    return result
