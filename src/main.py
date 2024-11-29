"""
Description: Xmas tree lights app using a NeoPixel matrix and MQTT for communication.
It includes functions to initialize settings and logging, connect to WiFi and MQTT, start effects,
and handle the main loop of the application.

Author: Gijs Mos, Sensemakers Amsterdam based on the original code by Karijn Wessing.
Maintainer: Sensemakers Amsterdam  https://sensemakersams.org

Functions:
- start_initial_effect(): Starts the initial effect for the application.
- init_settings_and_logging(): Initializes settings and logging.
- startup(): Initializes the device and sets up LED and effects.
- start_cloud(): Connects to WiFi and MQTT, and syncs time with NTP server.
- main(print_help=True, enable_cloud=True): Main function to run the device.
- allow_repl(): Allows REPL access by sleeping for 5 seconds.
"""

import gc
from random import choice
from time import sleep, ticks_diff, ticks_ms

import machine
import micropython
import neopixel
import pixellib
import senselogging as logging
import settings

from connectivity import (
    is_wifi_connected,
    mqtt_connect,
    mqtt_poll,
    mqtt_register_callback,
    ntp_sync_time,
    wifi_connect,
)
from effects import (
    effect_loop,
    full_help,
    get_effect_json,
    get_effects,
    init_effects,
    mqtt_effect_handler,
    start_effect_from_json,
)

GC_INTERVAL = 30000  # 30 seconds in ms between garbage collection runs

# Default settings, good for Xiao ESP32S3 with corresponding MicroPython firmware
# Override these in .env file if needed.
COLS = 4  # override with pix_columns setting
ROWS = 3  # override with pix_rows setting
PIXEL_PIN = 1  # override with pix_pin setting
SDA_PIN = 0  # override with sda_pin setting
SCL_PIN = 1  # override with scl_pin setting


def start_initial_effect():
    """
    Starts the initial effect for the application.

    This function retrieves the initial effect setting from the dot.env file. If the setting is
    not found, it selects a random effect from the available effects. The selected effect is then
    started.

    Returns:
        None
    """
    json_effect = settings.settings_get("initial_effect")
    logging.debug("Initial effect from settings: %s", json_effect)
    if json_effect is None:
        json_effect = get_effect_json(choice(get_effects()))
        logging.debug("Initial random effect: %s", json_effect)
    if json_effect is not None:
        start_effect_from_json(json_effect)
        logging.info("Started initial effect: %s.", json_effect)
        effect_loop()  # Run the effect first step
    else:
        logging.error("No initial effect found.")


def init_settings_and_logging():
    FMT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(
        level=logging.INFO,
        format=FMT,
    )
    logging.info("Initializing settings and logging")
    settings.settings_load()
    level = settings.settings_get("log_level", "INFO")
    match_level = level.upper().strip()
    # Bit of a hack to get the logging level from the module
    for lvl_id, lvl_name in logging._level_dict.items():
        if lvl_name == match_level:
            logging.basicConfig(level=lvl_id, format=FMT)
            break
    else:
        logging.error("Invalid log level in settings: %s", level)


def startup():
    """
    Startup function to initialize the device.
    This function performs the following tasks:
    1. Allocates an emergency exception buffer for MicroPython.
    2. Prints a startup message to indicate the initialization of the Xmas Tree Lights Controller.
    3. Loads the settings using the `settings.load_settings()` method.
    4. Sets up the LED and effects by:
       - Retrieving the pixel pin, columns, and rows from the settings or using default values.
       - Initializing the NeoPixel object with the specified pin and total number of pixels.
       - Creating a NeoPixMatrix object with the initialized NeoPixel object, columns, and rows.
    5. Initializes the effects using the `init_effects(matrix)` function.
    """

    micropython.alloc_emergency_exception_buf(100)
    init_settings_and_logging()
    logging.info("Starting Xmas Tree Lights Controller.")

    # Setup LED & effects stuff
    pix_pin = int(settings.settings_get("pix_pin", PIXEL_PIN))
    pix_columns = int(settings.settings_get("pix_columns", COLS))
    pix_rows = int(settings.settings_get("pix_rows", ROWS))
    pixels = neopixel.NeoPixel(machine.Pin(pix_pin), pix_columns * pix_rows)
    matrix = pixellib.NeoPixMatrix(pixels, pix_columns, pix_rows)
    init_effects(matrix)


def start_cloud():
    """
    Connect to WiFi and MQTT and attempt to sync time with NTP server in the cloud.

    This function attempts to connect to a WiFi network and then to an MQTT broker.
    If the WiFi connection is successful, it proceeds to connect to the MQTT broker
    and synchronizes the time using NTP.

    Raises:
        ConnectionError: If the WiFi connection fails.
    """
    logging.info("Connecting to WiFi and MQTT")
    # We can re-use an existing STA connection, but will reconnect if not connected or AP.
    reconnect = is_wifi_connected() != "STA"
    if wifi_connect(reconnect=reconnect) == "STA":
        mqtt_register_callback("effect", mqtt_effect_handler)
        mqtt_connect()
        ntp_sync_time()
    else:
        logging.info(
            "No WiFi network connection available, AP mode only. No MQTT and NTP."
        )


def main(print_help=True, enable_cloud=True):
    """Main function to run the device."""
    startup()

    if enable_cloud:
        start_cloud()
    start_initial_effect()

    if print_help:
        print("\n" + full_help())

    last_gc = ticks_ms()
    try:
        while True:
            effect_loop()  # Run the effect's next step
            mqtt_poll()  # Poll for incoming MQTT messages
            if ticks_diff(ticks_ms(), last_gc) > GC_INTERVAL:
                gc.collect()
                last_gc = ticks_ms()

    except Exception as e:
        logging.exc(e, "An unhandled exception occurred.")
        logging.error("Re-booting the Xmas Tree Lights Controller.")
        # Give the logging module some time to write the error message
        # and prevent a fast reboot loop in case of a persistent error.
        sleep(20)
        machine.reset()
        while True:
            pass


def allow_repl():
    """Allow REPL access by sleeping for 5 seconds."""
    print(
        "You have 5 seconds to press Ctrl+C to stop the program and enter the REPL.",
        end="",
    )
    for i in range(10):
        print(".", end="")
        sleep(0.5)
    print()


if __name__ == "__main__":
    allow_repl()
    main()
