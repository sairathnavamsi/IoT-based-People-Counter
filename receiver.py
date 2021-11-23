import random
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = ''
password = ''

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!") #successful connnection
        else:
            print("Failed to connect, return code %d\n", rc) #failed connection

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password) 
    client.on_connect = on_connect
    client.connect(broker, port) # connect to broker
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg): # on revieving the message, print count
        print(f"Number of people: `{msg.payload.decode()}`")
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt() # connect to the broker
    subscribe(client) # subscribe
    client.loop_forever() # infinit loop


if __name__ == '__main__':
    run()