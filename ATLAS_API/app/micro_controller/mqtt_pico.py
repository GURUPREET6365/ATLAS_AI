import os
import paho.mqtt.client as mqtt_client
from dotenv import load_dotenv
from ATLAS_API.app.telegram.utilities.send_message import send_message


load_dotenv()
ADMIN_CHAT_ID= os.getenv('ADMIN_CHAT_ID')
CLIENT_ID_MQTT = os.getenv("CLIENT_ID_MQTT")
BROKER_MQTT = os.getenv("BROKER_MQTT")

client = mqtt_client.Client(client_id=CLIENT_ID_MQTT)

# Step 2: Connect to broker
client.connect("broker.hivemq.com", 1883, 60)

# This will keep the connection alive.
client.loop_start()

def send_true():
    # print('send true')
    client.publish("laptop/battery/switch/control", "true")
    send_message(ADMIN_CHAT_ID, 'Now your laptop is charging!')

def send_false():
    client.publish("laptop/battery/switch/control", "false")