"""
    Package "centopy"

    This module provides helpful objects
"""
import re


def clean_string(text: str, pattern: str=None) -> str:
    """
    Cleans up a string by replacing any non-alphanumeric characters
    (except spaces and dot) with underscores.

    Parameters
    ----------
    text : str
        The input string to be cleaned up.
    pattern : str, optional
        A regular expression pattern to use for replacing non-alphanumeric
        characters. Defaults to None,
        which uses the pattern r"[^a-zA-Z0-9\.\s]+".

    Returns
    -------
    str
        The cleaned up string with non-alphanumeric characters (except spaces)
        replaced by underscores.

    Notes
    -----
    This function replaces any characters in the input `text` that are not
    alphanumeric (excluding spaces) with underscores,
    effectively cleaning up the input string. If a `pattern` argument is provided,
    it will be used instead of the default
    pattern r"[^a-zA-Z0-9\s]+".

    Examples
    --------
    >>> clean_string("Hello, World! How are you today?")
    'Hello__World__How_are_you_today_'
    
    >>> clean_string("Hello, World! How are you today?", pattern=r"[^\w\s]+")
    'Hello__World__How_are_you_today_'
    """

    if pattern is None:
        pattern = r"[^a-zA-Z0-9\.\s]+"
    return re.sub(pattern, "_", text.replace(" ", "_"))
