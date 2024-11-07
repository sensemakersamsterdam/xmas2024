"""Xmas tree lights controller using MQTT and NeoPixel matrix."""

from random import choice

import machine
import neopixel
import pixellib
import settings

from effects import (
    all_effect_names,
    effect_loop,
    full_help,
    init_effects,
    random_color,
    start_effect,
)

COLS = 3
PIXEL_PIN = 0
ROWS = 4


def startup():
    """Startup function to initialize the device."""
    print("Starting Xmas Tree Lights Controller")

    # Setup LED stuff
    pixels = neopixel.NeoPixel(machine.Pin(PIXEL_PIN), ROWS * COLS)
    matrix = pixellib.NeoPixMatrix(pixels, ROWS, COLS)
    init_effects(matrix)

    # Initial random effect
    initial_color = random_color()
    initial_effect = next(settings.get_settings("initial_effect")) or choice(
        all_effect_names()
    )
 
    print(f"Starting initial effect: {initial_effect} with color {initial_color}\n")
    start_effect(initial_effect, {"color": f"{initial_color}"})

    print(full_help())


def main():
    """Main function to run the device."""
    startup()

    while True:
        effect_loop()


# if __name__ in "__main__":
main()
