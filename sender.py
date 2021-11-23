import cv2
import os
import random
from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = ''
password = ''

def connect_mqtt(): #connect to the mqtt broker
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

client = connect_mqtt() #connect to the mqtt broker
client.loop_start() #stay connected

# load haar cascade classifier
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
msg_count = 0
video_capture = cv2.VideoCapture(0)
while True: #infinit loop
    # Capture frame-by-frame
    ret, frames = video_capture.read()
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    person = 1
    #Draw a rectangle around the faces
    for x,y,w,h in faces:
        cv2.rectangle(frames, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frames, f'person {person}', (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        person += 1
    #show status, no of people on cv2 window
    cv2.putText(frames, 'Status : Detecting ', (40,40), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.putText(frames, f'Total Persons : {person-1}', (40,70), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255,0,0), 2)
    cv2.imshow('output', frames)
    msg = person-1
    result = client.publish(topic, msg) # publish to the broker
    status = result[0]
    if status == 0:
        print(f"Sent People count : {msg} to topic `{topic}`") # published successfully
    else:
        print(f"Failed to send message to topic {topic}") #failed
    msg_count += 1
    if cv2.waitKey(1) & 0xFF == ord('q'): #press q to quit
        break
        
video_capture.release() #free memory
cv2.destroyAllWindows()