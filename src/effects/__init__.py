"""
effect_base.py:
    - Functions to initialize and run effects on the matrix.
    - Base class for all effects.
    - Utility functions and constants.
"""

from time import ticks_ms
from os import listdir
from random import choice

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
            print(f"Importing {name}")
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
    Return a tuple of all registered effect objects, pre-sorted by name.

    Returns:
        tuple: A tuple containing all registered effect objects, sorted by their name.
    """
    return _effects


def effect_name(e):
    """
    Return the name of the effect passed in.

    Args:
        e: The effect class to get the name of.

    Returns:
        str: The name of the effect in lowercase.
    """
    return e.__name__.lower()


def all_effect_names():
    """
    Return a tuple of the names of all registered effects sorted.

    Returns:
        tuple: A tuple containing the names of all registered effects in lowercase.
    """
    return tuple(effect_name(e) for e in _effects)


def effect_purpose(effect):
    """
    Return the purpose of the effect as a string.

    Args:
        effect: The effect class to get the purpose of.

    Returns:
        str: The purpose of the effect. If the effect has a 'help_purpose' attribute, it returns that.
             Otherwise, it returns a default message indicating the effect's name.
    """
    if hasattr(effect, "help_purpose"):
        return effect.help_purpose
    else:
        return f"Display {effect.__name__} on the matrix."


def effect_json(effect):
    """
    Return the JSON string to use to start the effect.

    Args:
        effect: The effect class to get the JSON string for.

    Returns:
        str: The JSON string representation of the effect. If the effect has a 'help_json' attribute,
             it returns that. Otherwise, it returns a default JSON string with the effect's name.
    """
    if hasattr(effect, "help_json"):
        return effect.help_json
    else:
        return f'{{ "effect": "{effect_name(effect)}" }}'


def effect_by_name(effect_name):
    """
    Return the effect object by name or None if not found.

    Args:
        effect_name (str): The name of the effect to retrieve.

    Returns:
        EffectBase: The effect class if found, otherwise None.
    """
    effect_name = effect_name.lower()
    for e in _effects:
        if effect_name(e) == effect_name:
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


def start_effect(effect_name, params=None):
    """
    Start an effect by name with optional effect-specific parameters.

    Args:
        effect_name (str): The name of the effect to start.
        params (dict, optional): A dictionary of parameters specific to the effect. Defaults to None.
                                 Unrecognised parameters are ignored.

    Returns:
        The result of the efect's start() method, or None if not found.
    """
    global _current_effect
    effect = effect_by_name(effect_name)
    if effect:
        if params is None:
            params = {}
        _current_effect = effect(_matrix, params)
        return _current_effect.start()
    return None


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
            print(f"Could not start {self.__class__.__name__} due to {e}")
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
        name = effect_name(e)
        help_lines.append(f"{name}: {effect_purpose(e)}")
        help_lines.append(f"{'':{len(name)+1}} {effect_json(e)}")
    return "\n".join(help_lines)