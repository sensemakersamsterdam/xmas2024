import machine
import neopixel
import network
import pixellib
import settings
from umqtt.robust import MQTTClient
from binascii import hexlify
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
  mqtt_client_id = hexlify(
        mqtt_client_id.encode() if mqtt_client_id else machine.unique_id()
    )


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
        print(f"pa rams {params=}")

        helpstr = params.get("help", None)
        if helpstr is None:
            effect = effects.get(topic, EffectBase)(matrix, params)
        else:
            effect.start()
            print("get help on " + helpstr)
            provider = effects.get(helpstr, None)
            print(f"provider = '{provider}'")

            if provider is None:
                helptext = effects.help_text()
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
