import machine
import network
import settings
from umqtt.robust import MQTTClient
import time
from binascii import hexlify

_callbacks = {}
_main_topic = "#"

_client = None

def register_callback(topic, callback):
    topic.strip()
    if callback is None:
        if topic in _callbacks:
            del _callbacks[topic]
        return
    _callbacks[topic] = callback


def mqtt_message(topic, msg):
    try:
        topic = topic.strip().decode()
        if topic.startswith(_main_topic):
            topic = topic[len(_main_topic) :]

        handler = _callbacks.get(topic, None)
        if handler is not None:
            try:
                handler(msg)
            except Exception as e:
                print(f"Error in handler for {topic}: {e}")
        else:
            print(f"No handler for {topic}")
    except Exception as e:
        print("Unexpected error ignored: ", e)


def connect_mqtt(clean_session=True):
    global _main_topic, _client
    
    if _client is not None:
        try:
            _client.disconnect()
        except Exception:
            pass

    (
        mqtt_user,
        mqtt_pass,
        mqtt_client_id,
        mqtt_server,
        mqtt_user,
        mqtt_pass,
        _main_topic,
    ) = settings.get_settings(
        "mqtt_user",
        "mqtt_pass",
        "mqtt_client_id",
        "mqtt_server",
        "mqtt_user",
        "mqtt_pass",
        "main_topic",
    )
    mqtt_client_id = hexlify(
        mqtt_client_id.encode() if mqtt_client_id else machine.unique_id()
    )
    if not _main_topic.endswith("/"):
        _main_topic += "/"

    print("Connecting to MQTT...", end="")
    _client = MQTTClient(mqtt_client_id, mqtt_server, user=mqtt_user, password=mqtt_pass, keepalive=60)
    
    isconnected = False
    while True:
        try:
            _client.connect(clean_session=clean_session)
            break
        except Exception as e:
            print(".", end="")
            time.sleep(1)

    _client.set_callback(mqtt_message)
    _client.subscribe(_main_topic + "#")
    print("MQTT Connected")

    return _client


print("Connecting to WiFi...", end="")
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifi_ssid, wifi_passwd)
while not wifi.isconnected():
    print(".", end="")
    sleep(0.25)
print(f"Connected to WIFI {wifi.ifconfig()[0]}")

_client = connect_mqtt()
