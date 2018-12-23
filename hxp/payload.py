import paho.mqtt.client as mqtt
def on_connect(client, userdata, flags, rc):
    client.subscribe("$internal/admin/webcam")

def on_message(client, userdata, msg):
    print msg.payload
    exit()
client = mqtt.Client(transport="websockets")
client.on_connect = on_connect
client.on_message = on_message
client.connect('159.69.212.240', 60805, 60)
client.loop_forever()