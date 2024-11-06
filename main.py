"""
MicroPython MQTT NeoPixels Example for Wokwi.com

To control the pixels:

1. Go to http://www.hivemq.com/demos/websocket-client/
2. Click "Connect"
3. Under Public, set the Topic to :
            "sensemakers/xmas/karijn-1"
            "sensemakers/xmas/all"
4. in the Message field type [255, 0, 0] (or any other color RGB value)
5. click "Publish"

Copyright (C) 2022, Uri Shaked

https://wokwi.com/arduino/projects/315787266233467457
"""

import json
from binascii import hexlify
from time import sleep

import machine
import neopixel
import network
import pixellib
import settings
from umqtt.robust import MQTTClient

from effects import EffectBase, Effects
from effects.cross import Cross

# Keep these lines at the top to clear the LEDs asap after boot
strip = neopixel.NeoPixel(machine.Pin(0), 12)
strip.fill((0, 0, 0))
strip.write()

# Load settings from the .env file
(
    wifi_ssid,
    wifi_passwd,
    mqtt_user,
    mqtt_pass,
    mqtt_client_id,
    mqtt_server,
    mqtt_user,
    mqtt_pass,
    mtopic,
    atopic,
) = settings.get_settings(
    "wifi_ssid",
    "wifi_passwd",
    "mqtt_user",
    "mqtt_pass",
    "mqtt_client_id",
    "mqtt_server",
    "mqtt_user",
    "mqtt_pass",
    "mtopic",
    "atopic",
)

print(
    wifi_ssid,
    wifi_passwd,
    mqtt_user,
    mqtt_pass,
    mqtt_client_id,
    mqtt_server,
    mqtt_user,
    mqtt_pass,
    mtopic,
    atopic,
)

wifi_ssid = wifi_ssid.encode()
wifi_passwd = wifi_passwd.encode()
mqtt_client_id = hexlify(
    mqtt_client_id.encode() if mqtt_client_id else machine.unique_id()
)

matrix = pixellib.NeoPixMatrix(strip, 4, 3)

effects = Effects()
print(effects.help())

# Run the Cross effect by default
effect = Cross(matrix, None)
effect.wait = 1000
effect.start()


def mqtt_message(topic, msg):
    global effect
    try:
        topic = topic.decode()
        print(f"Start {topic=} -- {msg=}")
        if msg is not None:
            msg = msg.decode()
            params = json.loads(msg)
            topic = params.get("effect", topic)
        else:
            params = None
        print(f"params {params=}")

        helpstr = params.get("help", None)
        if helpstr is None:
            effect = effects.get(topic, EffectBase)(matrix, params)
        else:
            effect.start()
            print("get help on " + helpstr)
            provider = effects.get(helpstr, None)
            print(f"provider = '{provider}'")

            if provider is None:
                helptext = effects.help()
            else:
                helptext = provider.help_text()
            print(f"help: {helptext=}")
            client.publish(mtopic + "/help", helptext)
    except Exception as e:
        print("Error: ", e)


def connect_mqtt():
    global mtopic
    global atopic
    print("Connecting to MQTT---", end="")
    client = MQTTClient(mqtt_client_id, mqtt_server, user=mqtt_user, password=mqtt_pass)
    isconnected = False
    while not isconnected:
        try:
            client.connect()
            isconnected = True
        except:
            print("-", end="")

    client.set_callback(mqtt_message)
    client.subscribe(mtopic)
    client.subscribe(atopic)

    print("MQTT Connected")

    return client


print("Connecting to WiFi...", end="")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_passwd)
while not wifi.isconnected():
    print(".", end="")
    sleep(0.25)
print(f"Connected to WIFI {wifi.ifconfig()[0]}")

client = connect_mqtt()

while True:
    try:
        client.check_msg()
        if effect is not None:
            effect.loop()
    except Exception:
        pass
