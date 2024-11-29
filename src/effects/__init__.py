"""
Description: This module provides functions and a class to initialize and run effects on the matrix.
It includes a base class for all effects, utility functions and constants, and an asynchronous mode.

Author: Karijn Wessing and Gijs Mos, Sensemakers Amsterdam
Maintainer: Sensemakers Amsterdam  https://sensemakersams.org

Functions:
- init_effects(matrix, use_async=False): Initialize the effects module with the given matrix object.
- get_effects(): Return a tuple of all registered effect objects, sorted by effect name.
- get_effect_name(effect): Return the name of the effect passed in.
- all_effect_names(): Return a tuple of the names of all registered effects sorted.
- get_effect_purpose(effect): Return the purpose of the effect as a string.
- get_effect_json(effect): Return the JSON string to use to start the effect.
- effect_by_name(effect_name): Return the effect object by name or None if not found.
- effect_loop(): Execute the loop method of the current effect if it exists.
- start_effect(effect, params=None): Start an effect with optional effect-specific parameters.
- start_effect_by_name(effect_name, params=None): Start an effect by name with optional effect-specific parameters.
- start_effect_from_json(json_str): Start an effect from a JSON string.
- mqtt_effect_handler(topic, msg): Handler for the /effect MQTT sub topic.
- wheel(pos): Input a value 0 to 255 to get a color value.
- random_color(color_list=RAINBOW): Return a random color from the list passed in.
- full_help(): Return a string with the help for all effects.
"""

import json
from os import listdir
from random import choice
from time import ticks_ms
import senselogging as logging

_ASYNC = False  # Use asyncio for effect loop if True
_matrix = None  # holds the matrix object to render the effects on
_effects = ()  # holds the list of defined effects
_current_effect = None  # holds the running effect object


def init_effects(matrix, use_async=False):
    """
    Initialize the effects module with the given matrix object and an optional asynchronous flag.
    This function dynamically imports all Python modules in the current package directory
    (excluding __init__.py) and collects their 'register' attributes if they exist. The collected
    effects are then sorted by their name and stored in a global variable.
    Args:
        matrix (object): The matrix object to be used by the effects.
        use_async (bool, optional): If True, enables asynchronous mode. Defaults to False.
    Raises:
        ImportError: If any of the dynamically imported modules do not have a 'register' attribute.
    Side Effects:
        Sets the global variables _matrix and _effects with the provided matrix and the collected effects.
        If use_async is True, sets the global variable _ASYNC to True.
    """
    global _matrix, _effects

    _matrix = matrix
    e = []
    pack_dir = __file__.rsplit("/", 1)[0]
    for f in listdir(pack_dir):
        if f.endswith(".py") and f != "__init__.py":
            name = "effects." + f[:-3]
            logging.debug("Importing %s", name)
            exec(f"import {name}")
            m = eval(name)
            if hasattr(m, "register"):
                e += m.register
            else:
                raise ImportError(f"Module {m} does not have a register attribute")
    _effects = tuple(sorted(e, key=lambda x: x.__name__.lower()))

    if use_async:
        global _ASYNC
        _ASYNC = True


def get_effects():
    """
    Return a tuple of all registered effect objects, sorted by effect name.

    Returns:
        tuple: A tuple containing all registered effect objects, sorted by their name.
    """
    return _effects


def get_effect_name(effect):
    """
    Return the name of the effect passed in.

    Args:
        effect: The effect class to get the name of.

    Returns:
        str: The name of the effect in lowercase.
    """
    if not issubclass(effect, EffectBase):
        raise TypeError(f"Not an effect {effect}")
    return effect.__name__.lower()


def all_effect_names():
    """
    Return a tuple of the names of all registered effects sorted.

    Returns:
        tuple: A tuple containing the names of all registered effects in lowercase.
    """
    return tuple(get_effect_name(e) for e in _effects)


def get_effect_purpose(effect):
    """
    Return the purpose of the effect as a string.

    Args:
        effect: The effect class to get the purpose of.

    Returns:
        str: The purpose of the effect. If the effect has a 'help_purpose' attribute, it returns that.
             Otherwise, it returns a default message indicating the effect's name.
    """
    assert issubclass(effect, EffectBase), f"Not an effect {effect}"
    if hasattr(effect, "help_purpose"):
        return effect.help_purpose
    else:
        return f"Display {get_effect_name(effect)} on the matrix."


def get_effect_json(effect):
    """
    Return the JSON string to use to start the effect.

    Args:
        effect: The effect class to get the JSON string for.

    Returns:
        str: The JSON string representation of the effect. If the effect has a 'help_json' attribute,
             it returns that. Otherwise, it returns a default JSON string with the effect's name.
    """
    assert issubclass(effect, EffectBase), f"Not an effect {effect}"
    if hasattr(effect, "help_json"):
        return effect.help_json
    else:
        return f'{{ "effect": "{get_effect_name(effect)}" }}'


def effect_by_name(effect_name):
    """
    Return the effect object by name or None if not found.

    Args:
        effect_name (str): The name of the effect to retrieve.

    Returns:
        EffectBase: The effect class if found, otherwise None.
    """
    assert isinstance(effect_name, str), "str with effect name expected"
    effect_name = effect_name.lower()
    for e in _effects:
        if get_effect_name(e) == effect_name:
            return e
    return None


def effect_loop():
    """
    Execute the loop method of the current effect if it exists.

    This function checks if there is a current effect set, and if so, calls its loop method.
    """
    if _current_effect:
        _current_effect.loop()


if _ASYNC:
    # Setup the asyncio version and create the effect task
    import uasyncio as asyncio

    async def effect_loop_async():
        """
        Asynchronous loop to execute the effect loop method.

        This function calls the effect_loop function and then sleeps for 0 seconds to yield control.
        """
        effect_loop()
        await asyncio.sleep(0)

    asyncio.create_task(effect_loop_async())


def start_effect(effect, params=None):
    """
    Start an effect with optional effect-specific parameters.

    Args:
        effect (EffectBase): The class of the effect to start.
        params (dict, optional): A dictionary of parameters specific to the effect. Defaults to None.
                                 Unrecognised parameters are ignored.

    Returns:
        The result of the efect's start() method, or None if not found.
    """
    global _current_effect
    if params is None:
        params = {}
    _current_effect = effect(_matrix, params)
    return _current_effect.start()


def start_effect_by_name(effect_name, params=None):
    """
    Start an effect by name with optional effect-specific parameters.

    Args:
        effect_name (str): The name of the effect to start.
        params (dict, optional): A dictionary of parameters specific to the effect. Defaults to None.
                                 Unrecognised parameters are ignored.

    Returns:
        The result of the effect's start() method, or None if not found.
    """
    effect = effect_by_name(effect_name)
    if effect is not None:
        return start_effect(effect, params)
    else:
        logging.warning("Effect not defined: %s", effect_name)
    return None


def start_effect_from_json(json_str):
    """
    Start an effect from a JSON string.

    Args:
        json_str (str): The JSON string to parse and start the effect from.

    Returns:
        The result of the effect's start() method, or None if not found.
    """
    try:
        effect_params = json.loads(json_str)
        effect_name = effect_params.get("effect")
        if effect_name is not None:
            return start_effect_by_name(effect_name, effect_params)
        logging.warning('No "effect" in JSON: %s', json_str)
    except Exception as e:
        logging.exc(e, "Could not start: %s", json_str)

    return None


def mqtt_effect_handler(topic, msg):
    """Handler for the /effect MQTT sub topic."""
    msg = msg.decode().strip()
    logging.info("From MQTT: %s - %s", topic, msg)
    if topic == "effect":
        start_effect_from_json(msg)


###
# Base class for all effects
#
class EffectBase:
    """
    Base class for all effects.

    Attributes:
        _matrix: The matrix object to apply the effect on.
        _start_ms (int): Start time in milliseconds of current effect step.
        _wait (int): Wait time in milliseconds between updates.
    """

    def __init__(self, matrix, params):
        """
        Initialize the base effect.

        Args:
            matrix: The matrix object to apply the effect on.
            params: Additional parameters for the effect.
        """
        self._matrix = matrix
        self._params = params
        self._start_ms = ticks_ms()
        self._wait = params.get("wait", 100)

    def start(self):
        """
        Start the effect by rendering it initially.

        Returns:
            bool: True if the effect started successfully, False otherwise.
        """
        try:
            self._start_ms = ticks_ms()
            self.render()
            return True
        except Exception as e:
            logging.exc(e, "Could not start %s.", self.__class__.__name__)
            return False

    def render(self):
        """
        Render the effect on the matrix.

        This method should be implemented by subclasses to define how the effect is rendered.
        """
        raise NotImplementedError("render")

    def advance(self):
        """
        Advance the effect to the next state.

        This method should be implemented by subclasses to define how the effect progresses.
        """
        raise NotImplementedError("advance")

    def loop(self):
        """
        Main loop to render and advance the effect based on the wait time.

        This method checks if the wait time has passed, then calls the render and advance methods.
        """
        if ticks_ms() > self._start_ms + self._wait:
            self.render()
            self.advance()
            self._start_ms = ticks_ms()


###
# Utility constants
#
RAINBOW = (
    (126, 1, 0),
    (114, 13, 0),
    (102, 25, 0),
    (90, 37, 0),
    (78, 49, 0),
    (66, 61, 0),
    (54, 73, 0),
    (42, 85, 0),
    (30, 97, 0),
    (18, 109, 0),
    (6, 121, 0),
    (0, 122, 5),
    (0, 110, 17),
    (0, 98, 29),
    (0, 86, 41),
    (0, 74, 53),
    (0, 62, 65),
    (0, 50, 77),
    (0, 38, 89),
    (0, 26, 101),
    (0, 14, 113),
    (0, 2, 125),
    (9, 0, 118),
    (21, 0, 106),
    (33, 0, 94),
    (45, 0, 82),
    (57, 0, 70),
    (69, 0, 58),
    (81, 0, 46),
    (93, 0, 34),
    (105, 0, 22),
    (117, 0, 10),
)


###
# Utility functions
#
def wheel(pos):
    """
    Input a value 0 to 255 to get a color value.
    The colors are a transition r - g - b - back to r.

    Args:
        pos (int): Position in the color wheel (0-255).

    Returns:
        tuple: A tuple representing the RGB color.
    """
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def random_color(color_list=RAINBOW):
    """
    Return a random color from the list passed in.

    Args:
        color_list (list): A list of colors to choose from. Defaults to RAINBOW.

    Returns:
        tuple: A tuple representing the RGB color.
    """
    return choice(color_list)


def full_help():
    """
    Return a string with the help for all effects.

    Returns:
        str: A string with the help for all effects.
    """
    help_lines = [f"Available effects: {", ".join(all_effect_names())}.\n"]
    for e in get_effects():
        name = get_effect_name(e)
        help_lines.append(f"{name}: {get_effect_purpose(e)}")
        help_lines.append(f"{'':{len(name)+1}} {get_effect_json(e)}")
    return "\n".join(help_lines)


def text2color(params, default_color_rgb=(255, 0, 0)):
    """
    Get the color string from the params dict and convert it to a color setting.

    Args:
        params (dict): The parameters to get the color from.

    Returns:
        tuple: The color as a tuple (r, g, b).
    """
    try:
        color = params.get("color", f"{default_color_rgb}")
        color_rgb = eval(color)
        if not isinstance(color_rgb, tuple) or len(color_rgb) != 3:
            raise TypeError(f'"color" must be a stringified tuple of three integers, not "{color_rgb}".')
    except TypeError as e:
        logging.exc(e, "Cannot convert color setting, setting to {default_color_rgb}}")
        color_rgb = default_color_rgb
    return color_rgb


def fader(fade_index: int, fade_max : int, fade_from, fade_to):
    """
    Fade from one color/set to an orher.

    Args:
        fade_index (int): The current fade step.
        fade_max (int):   The number of fade steps.
        fade_from (int/tuple/list-of-tuples): The first fade step.
        fade_to (int/tuple/list-of-tuples): The last fade step.

    Returns:
        tuple: The color as a tuple (r, g, b).
    """
    if isinstance(fade_from, tuple) and isinstance(fade_to, tuple):
        #print(f"fade tuples {fade_index}, {fade_max}, {fade_from}, {fade_to}")
        return tuple([fader(fade_index, fade_max, fade_from[i], fade_to[i]) for i in range(min(len(fade_from), len(fade_to)))])
    if isinstance(fade_from, list) and isinstance(fade_to, list):
        #print(f"fade tuples {fade_index}, {fade_max}, {fade_from}, {fade_to}")
        return [fader(fade_index, fade_max, fade_from[i], fade_to[i]) for i in range(min(len(fade_from), len(fade_to)))]  
    else:
        #print(f"fade floats {fade_index}, {fade_max}, {fade_from}, {fade_to}")
        return round(((fade_from * (fade_max - fade_index)) + (fade_to * fade_index)) / fade_max)
    
