"""Xmas tree lights controller using MQTT and NeoPixel matrix."""

from random import choice

import machine
import neopixel
import pixellib
import settings

from effects import (
    get_effect_json,
    get_effects,
    init_effects,
    effect_loop, # noqa: F401
    full_help, # noqa: F401,
    start_effect_from_json
)

# Default settings, good for Xiao ESP32S3 with corresponding MicroPython firmware
# Override these in .env file if needed.
COLS = 4  # override with pix_columns setting
ROWS = 3  # override with pix_rows setting
PIXEL_PIN = 1  # override with pix_pin setting
SDA_PIN = 0  # override with sda_pin setting
SCL_PIN = 1  # override with scl_pin setting


def start_initial_effect():
    # Initial random effect, override with the initial_effect setting in .env file
    json_effect = settings.get_setting("initial_effect")
    if json_effect is None:
        json_effect = get_effect_json(choice(get_effects()))
    if json_effect is not None:
        start_effect_from_json(json_effect)
        print("Started initial effect:", json_effect)


def startup():
    """Startup function to initialize the device."""
    print("Starting Xmas Tree Lights Controller")

    settings.load_settings()

    # Setup LED & effects stuff
    pix_pin = int(settings.get_setting("pix_pin", PIXEL_PIN))
    pix_columns = int(settings.get_setting("pix_columns", COLS))
    pix_rows = int(settings.get_setting("pix_rows", ROWS))
    pixels = neopixel.NeoPixel(machine.Pin(pix_pin), pix_columns * pix_rows)
    matrix = pixellib.NeoPixMatrix(pixels, pix_columns, pix_rows)
    init_effects(matrix)

    start_initial_effect()
   
