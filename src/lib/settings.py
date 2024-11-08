# Module to read a simple settings file

_settings = {}
_loaded = False


def load_settings(file_path=".env"):
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
    global _settings

    if _loaded:
        return

    print(f"Loading settings from {file_path}")
    try:
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                # Ignore empty lines and comments
                if line and not line.startswith("#"):
                    key, value = line.split("=")
                    _settings[key.strip().lower()] = value.strip()
        _loaded = True
    except Exception as e:
        print(f"Error reading settings file: {e}")


def get_settings_dict(file_path=".env"):
    """
    Reads a settings file and returns a dictionary of settings.

    Args:
        file_path (str): Path to the settings file. Defaults to ".env".

    Returns:
        dict: A dictionary containing the settings.
    """
    load_settings(file_path)
    return _settings


def get_settings(*args, file_path=".env"):
    """
    Retrieves specific settings from the settings file.

    Args:
        *args: Keys of the settings to retrieve.
        file_path (str): Path to the settings file. Defaults to ".env".

    Returns:
        tuple: A generator returning the values of the requested settings in order.
    """
    load_settings(file_path)
    return (_settings.get(k.lower(), None) for k in args)


def get_setting(key, default=None):
    """
    Retrieves a specific setting from the settings file.

    Args:
        key (str): The key of the setting to retrieve.
        default: The default value to return if the setting is not found.

    Returns:
        str: The value of the setting if found, or the default value.
    """
    if not _loaded:
        raise RuntimeError("Settings not loaded. Call load_settings() first.")
    return _settings.get(key.lower(), default)
