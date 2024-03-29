try:
    from typing import Any, Tuple
except ImportError:
    # for python2
    pass
try:
    from collections.abc import Mapping  # only works on python 3.3+
except ImportError:
    from collections import Mapping  # type: ignore[attr-defined, no-redef]


def safe_dict(dictionary, blacklist=('key', 'token', 'pass'), max_deep=5):
    # type: (Mapping[str, Any], Tuple[str,...], int)  -> Mapping[str, Any]
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
        elif any(b in key.lower() for b in blacklist):
            result[key] = '********'  # type:ignore[assignment]
        else:
            result[key] = dictionary[key]
    return result
