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

COLS = 4
PIXEL_PIN = 1   # Good for the XIAO-ESP32S3 board
ROWS = 3


def startup():
    """Startup function to initialize the device."""
    print("Starting Xmas Tree Lights Controller")

    settings.load_settings()

    # Setup LED stuff
    pix_pin = settings.get_setting("pix_pin", PIXEL_PIN)
    pix_columns = settings.get_setting("pix_columns", COLS)
    pix_rows = settings.get_setting("pix_rows", ROWS)
    pixels = neopixel.NeoPixel(machine.Pin(pix_pin), pix_columns * pix_rows)
    matrix = pixellib.NeoPixMatrix(pixels, pix_columns, pix_rows)
    init_effects(matrix)

    # Initial random effect
    initial_color = random_color()
    initial_effect = next(settings.get_setting("initial_effect")) or choice(
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
