# Module to read a simple settings file

_settings = {}


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
    print(f"Loading settings from {file_path}")
    try:
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                # Ignore empty lines and comments
                if line and not line.startswith("#"):
                    key, value = line.split("=")
                    _settings[key.strip()] = value.strip()
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
    d = get_settings_dict(file_path)
    return (d.get(k, None) for k in args)
