import time
import senselogging as logging
from effects import (
    all_effect_names,
    effect_loop,
    random_color,
    start_effect,
    effect_by_name,
)
from main import startup


def test_effects():
    """
    Main function to test all effects in a loop.
    It initializes the system, then cycles through effects every 10 seconds.
    """
    startup()

    start_time = time.time()
    effect_names = list(all_effect_names())

    while True:
        if start_time + 10 < time.time():
            curr_effect = effect_names[0]
            effect_names = effect_names[1:] + [curr_effect]
            start_effect(effect_by_name(curr_effect), {"color": f"{random_color()}"})
            logging.info("Starting effect: &s", curr_effect)
            start_time = time.time()
        effect_loop()


test_effects()
