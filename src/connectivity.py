"""
Description: This module provides functions to connect to WiFi and MQTT, and to synchronize time using NTP.
Written for the Xmas Tree Lights Controller project.

Author: Gijs Mos, Sensemakers Amsterdam based on the original code by Karijn Wessing.
Maintainer: Sensemakers Amsterdam  https://sensemakersams.org

Functions:
- mqtt_register_callback(topic, callback): Register a callback for a topic.
- mqtt_connect(clean_session=True): Connects to the MQTT broker using the provided settings.
- mqtt_poll(): Polls the MQTT client for incoming messages.
- mqtt_publish(sub_topic, msg, main_topic=None, retain=False): Publishes a message to the MQTT broker.
- mqtt_connected(): Checks if the MQTT client is connected.
- is_wifi_connected(): Check the connectivity status of the device.
- wifi_connect(reconnect=False): Connects to a WiFi network or starts an access point if no network is available.
- ntp_sync_time(): Synchronizes the system time with an NTP server.
"""

import senselogging as logging
import time
from binascii import hexlify

import machine
import network
import ntptime
import settings

from sensemqtt.robust import MQTTClient

# MQTT related stuff
_callbacks = {}  # topic -> callback mapping.
_main_topic = b"#"  # Default to all topics (not recommended)
_mqtt_client = None  # The MQTT client object


def mqtt_register_callback(topic, callback):
    """
    Register a callback for a topic. If the callback is None, the topic is unregistered.
    The callback will be called with two arguments: the topic (str) and the message (bytes like).

    Args:
        topic (str): The topic for which the callback is to be registered.
        callback (function or None): The callback function to be registered for the topic.
                                     If None, the topic is unregistered.

    Returns:
        The previous callback for the topic, or None if there was none.
    """
    global _callbacks
    if callback is None:
        # We are dealing with a delete request
        previous_cb = None
        if topic in _callbacks:
            previous_cb = _callbacks[topic]
            del _callbacks[topic]
        return previous_cb
    # A new one, just register it
    _callbacks[topic] = callback
    return None


def _mqtt_incoming(topic, msg):
    """
    Handles incoming MQTT messages by dispatching them to the appropriate handler.
    This function processes the incoming MQTT message by stripping and decoding the topic,
    checking if it starts with the main topic, and then dispatching it to the corresponding
    handler if one exists. If no handler is found for the topic, it logs a message. Any
    exceptions raised during the handling process are caught and logged.
    Args:
        topic (bytes): The topic of the incoming MQTT message.
        msg (bytes): The payload of the incoming MQTT message.
    Raises:
        Exception: If an unexpected error occurs during the processing of the message.
    """
    try:
        topic = topic.strip().decode()  # Convert to string
        if topic.startswith(_main_topic):
            topic = topic[len(_main_topic) :]  # Strip the main topic prefix

        handler = _callbacks.get(topic, None)  # Is there a handler for the topic?
        if handler is not None:
            # Call the handler and hope for the best ;-)
            try:
                handler(topic, msg)
            except Exception as e:
                logging.exc(e, "Error in handler for %s.", topic)
        else:
            logging.warning('No handler for MQTT sub-topic: "%s".', topic)
    except Exception as e:
        logging.exc(e, "Unexpected error in incoming MQTT handling.")


def _mqtt_has_connected():
    """Set subscription on (re)connection."""
    if _mqtt_client is not None:
        _mqtt_client.subscribe(_main_topic + "#", qos=0)


def mqtt_connect(clean_session=True):
    """
    Connects to the MQTT broker using the provided settings.
    This function retrieves MQTT settings, initializes the MQTT client, and attempts to connect to the MQTT broker.
    If a connection attempt fails, it will retry indefinitely until a connection is established.
    Args:
        clean_session (bool): If True, the broker will not send retained messages. Defaults to True.
    Returns:
        MQTTClient: The connected MQTT client instance.
    Raises:
        Exception: If an error occurs during the connection process.
    """
    global _main_topic, _mqtt_client

    if _mqtt_client is not None:
        # Disconnect the existing client if any
        try:
            _mqtt_client.disconnect()
        except Exception:
            pass
        _mqtt_client = None  #  Dispose of the old one if any

    # Get all parameters from settings
    (
        mqtt_user,
        mqtt_pass,
        mqtt_client_id,
        mqtt_server,
        _main_topic,
    ) = settings.settings_get_many(
        "mqtt_user",
        "mqtt_pass",
        "mqtt_client_id",
        "mqtt_server",
        "main_topic",
    )
    # Provide a default client_id if required
    mqtt_client_id = hexlify(
        mqtt_client_id.encode() if mqtt_client_id else machine.unique_id()
    )

    # Normalize main topic
    if not _main_topic.endswith("/"):
        _main_topic += "/"
    _main_topic = _main_topic.encode()

    logging.info(
        "Connecting to MQTT server %s with main topic %s", mqtt_server, _main_topic
    )
    _mqtt_client = MQTTClient(
        mqtt_client_id, mqtt_server, user=mqtt_user, password=mqtt_pass, keepalive=60
    )

    _mqtt_client.set_callback(_mqtt_incoming)
    _mqtt_client.set_on_connect(_mqtt_has_connected)

    while True:
        try:
            _mqtt_client.connect(clean_session=clean_session)
            break
        except Exception as e:
            logging.exc(
                e, "Failed to connect to MQTT broker %s as %s.", mqtt_server, mqtt_user
            )
            time.sleep(1)

    logging.info("MQTT Connected and subscribed to %s", _main_topic + "#")

    return _mqtt_client


def mqtt_poll():
    """
    Polls the MQTT client for incoming messages.
    This function polls the MQTT client for incoming messages and processes them using the
    registered handlers. If no client is connected, it will attempt to reconnect to the MQTT
    broker before polling for messages.
    Returns:
        None
    Raises:
        Exception: If an error occurs during the polling process.
    """
    global _mqtt_client
    if _mqtt_client is None:
        return
    try:
        _mqtt_client.check_msg()
    except Exception as e:
        logging.exc(e, "Error polling MQTT.")
        _mqtt_client = None  # Abandon the client to force a reconnect


def mqtt_publish(sub_topic, msg, main_topic=None, retain=False):
    """
    Publishes a message to the MQTT broker.
    This function publishes a message to the MQTT broker using the provided topic and message.
    Args:
        topic (str|bytes): The topic to which the message should be published.
        msg (bytes): The message to be published.
        main_topic (str|bytes): The main topic to be used for the message.
            If None, the default main topic is used. If empty, no main topic is prepended and
            just the sub_topic is used.
        retain (bool): If True, the message will be retained by the broker. Defaults to False.
    Returns:
        MQTTMessageInfo: An instance of MQTTMessageInfo, which provides information about the message delivery.
    Raises:
        Exception: If an error occurs during the publishing process.
    """
    if _mqtt_client is None:
        raise RuntimeError("MQTT client not connected.")

    topic = _main_topic if main_topic is None else main_topic
    if isinstance(topic, str):
        topic = topic.encode()
    if isinstance(sub_topic, str):
        sub_topic = sub_topic.encode()
    topic = topic.strip(b"/ ") + b"/" + sub_topic.strip(b"/ ")

    logging.debug("Publishing to %s: %s", topic, msg)
    return _mqtt_client.publish(topic, msg, retain=retain)


def mqtt_connected():
    return _mqtt_client is not None and _mqtt_client.isconnected()


## WiFi orelated stuff
#
_wifi_ap = network.WLAN(network.AP_IF)
_wifi_sta = network.WLAN(network.STA_IF)


def is_wifi_connected():
    """
    Check the connectivity status of the device.

    Returns:
        str: "STA" if connected to a WiFi station, "AP" if acting as an access point,
             or None if not connected to anything.
    """
    if _wifi_sta.isconnected():
        # BUG: This is not reliable, as the connection may have been lost anyway.
        # So we also check if we have an IP address.
        if _wifi_sta.ifconfig()[0] != "0.0.0.0":
            return "STA"  # We are connected to a WiFi station
        else:
            _wifi_sta.active(False)  # Connection lost, disable it
    if _wifi_ap.active():
        return "AP"  # We are an access point
    return None  # We are not connected to anything


def wifi_connect(reconnect=False):
    """
    Connects to a WiFi network or starts an access point if no network is available.
    If the device is already connected to a WiFi network and `reconnect` is False,
    the function will do nothing. Otherwise, it will attempt to connect to the WiFi
    networks listed in the settings. If no connection is successful, it will start
    an access point.
    Args:
        reconnect (bool): If True, forces reconnection to the WiFi network even if
                          already connected. Defaults to False.
    Raises:
        Exception: If there is an error parsing the wifi_stations setting.
    Returns:
        Same as is_connected().
    """
    if not reconnect and is_wifi_connected():
        logging.info("Already connected to WiFi; nothing done.")
        return is_wifi_connected()

    # Dispose of earlier connections if any.
    _wifi_ap.active(False)
    _wifi_sta.active(False)

    try:
        station_list = eval(settings.settings_get("wifi_stations", "[]"))
    except Exception as e:
        logging.exc(e, "Error parsing wifi_stations setting.")
        raise

    # Attempt all stations in the list
    for ssid, passwd in station_list:
        logging.info('Attempting WiFi network "%s".', ssid)
        _wifi_sta.active(True)
        _wifi_sta.connect(ssid, passwd)
        print(f"{ssid}: .", end="")
        for _ in range(50):
            if not _wifi_sta.isconnected():
                time.sleep(0.5)
                print(".", end="")
            else:
                print()
                logging.info(
                    'Connected to Wifi network "%s" with IP %s.',
                    ssid,
                    _wifi_sta.ifconfig()[0],
                )
                return is_wifi_connected()
        print()
        logging.info('Connecting WiFi network "%s" failed!', ssid)
        _wifi_sta.active(False)

    # No WiFi network found, start an access point as fall-back
    ap = settings.settings_get("wifi_ap_pfx", "sense") + "-" + hexlify(machine.unique_id()).decode()
    logging.info('No WiFi network found. Starting AP with SSID "%s".', ap)
    _wifi_ap.active(True)
    _wifi_ap.config(
        essid=ap,
        authmode=network.AUTH_WPA_WPA2_PSK,
        password=settings.settings_get("wifi_ap_passwd", "xmas-tree"),
    )
    logging.info("AP %s started with IP %s", ap, _wifi_ap.ifconfig()[0])

    return is_wifi_connected()


## NTP Time
#
def ntp_sync_time():
    """
    Synchronizes the system time with an NTP server.
    This function checks if the device is connected to WiFi. If it is connected,
    it retrieves the current time from an NTP server and adjusts it according to
    the time offset specified in the settings. The adjusted time is then set to
    the device's real-time clock (RTC).
    Returns:
        None
    """
    if not _wifi_sta.isconnected():
        logging.info("Not connected to WiFi, cannot set time.")
        return

    old_time = time.gmtime()
    for _ in range(3):
        try:
            t = ntptime.time()  # seconds since epoch in UTC
            break
        except Exception:
            time.sleep(1)  # ntp too busy, wait a bit
    else:
        logging.info("Failed to synchronize time with NTP.")
        return
    offset = int(settings.settings_get("time_offset", 0)) * 60
    tm = time.gmtime(t + offset)
    machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
    new_time = time.gmtime()
    logging.info(
        "Time synchronized with NTP from %s to %s, using UTC offset %d minutes.",
        "{0:02}/{1:02}/{2:02} {3:02}:{4:02}:{5:02}".format(*old_time),
        "{0:02}/{1:02}/{2:02} {3:02}:{4:02}:{5:02}".format(*new_time),
        offset // 60,
    )
