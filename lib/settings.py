# Module to read a simple settings file

def get_settings_dict(file_path=".env"):
    """
    Reads a settings file and returns a dictionary of settings.

    Args:
        file_path (str): Path to the settings file. Defaults to ".env".

    Returns:
        dict: A dictionary containing the settings.
    """
    settings = {}
    try:
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                # Ignore empty lines and comments
                if line and not line.startswith("#"):
                    key, value = line.split("=")
                    settings[key.strip()] = value.strip()
    except Exception as e:
        print(f"Error reading settings file: {e}")
    return settings

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
