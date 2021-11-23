
# IoT based People Counter
A project that combines computer vision and IoT technologies thst can count number of people in a room and send the data over a secure channel to the person concerned. This can especially be useful in public places like shops during COVID.

It uses haar cascade classifier to detect faces from real time feed and send the people count over MQTT protocol to the receiver. 

### Requirements
- Python 3.7
- OpenCV
- PahoMQTT

### Notes
- The MQTT broker used is EMQX.
- Replace the username and password fields with the ones you generated.
