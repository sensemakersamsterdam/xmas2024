"""
Description: This module provides functions to load settings from a file,
store them in a global dictionary, and retrieve them as needed.

Author: Gijs Mos, Sensemakers Amsterdam
Maintainer: Sensemakers Amsterdam  https://sensemakersams.org

Functions:
- settings_load(file_path=DEFAULT_FILE_PATH): Load settings from a file and store them in a global dictionary.
- settings_get_dict(file_path=DEFAULT_FILE_PATH): Reads a settings file and returns a dictionary of settings.
- settings_get_many(*args, file_path=DEFAULT_FILE_PATH): Retrieves specific settings from the settings file.
- settings_get(key, default=None, file_path=DEFAULT_FILE_PATH): Retrieves a specific setting from the settings file.
"""

import senselogging as logging

DEFAULT_FILE_PATH = "dot.env"

_settings = {}
_loaded = False


def settings_load(file_path=DEFAULT_FILE_PATH):
    """
    Load settings from a file and store them in a global dictionary.

    This function reads a settings file line by line, parses each line to extract
    key-value pairs, and stores them in the global `_settings` dictionary. It ignores
    empty lines and lines that start with a comment character ('#').

    Args:
        file_path (str): The path to the settings file. Defaults to ".env".

    Raises:
        Exception: If there is an error reading the settings file.
    """
    global _settings, _loaded

    if _loaded:
        return

    logging.info(f"Loading settings from {file_path}.")
    try:
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                # Ignore empty lines and comments
                if line and not line.startswith("#"):
                    try:
                        key, value = line.split("=", 1)
                    except ValueError:
                        logging.warning("Skipping invalid settings line: %s,", line)
                        continue
                    value = value.partition("#")[0]
                    _settings[key.strip().lower()] = value.strip()
        _loaded = True
    except Exception as e:
        logging.exc(e, "Error reading settings file.")
        raise


def settings_get_dict(file_path=DEFAULT_FILE_PATH):
    """
    Reads a settings file and returns a dictionary of settings.

    Args:
        file_path (str): Path to the settings file. Defaults to ".env".

    Returns:
        dict: A dictionary containing the settings.
    """
    settings_load(file_path)
    return _settings


def settings_get_many(*args, file_path=DEFAULT_FILE_PATH):
    """
    Retrieves specific settings from the settings file.

    Args:
        *args: Keys of the settings to retrieve.
        file_path (str): Path to the settings file. Defaults to ".env".

    Returns:
        list: A list containing the values of the requested settings in order.
    """
    settings_load(file_path)
    return [_settings.get(k.lower(), None) for k in args]


def settings_get(key, default=None, file_path=DEFAULT_FILE_PATH):
    """
    Retrieves a specific setting from the settings file.

    Args:
        key (str): The key of the setting to retrieve.
        default: The default value to return if the setting is not found.

    Returns:
        str: The value of the setting if found, or the default value.
    """
    settings_load(file_path)
    return _settings.get(key.lower().strip(), default)
