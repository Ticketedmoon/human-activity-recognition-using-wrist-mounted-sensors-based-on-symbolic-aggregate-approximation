import socket
import paho.mqtt.client as mqtt
import time
import base64


client_id = socket.gethostname()

#=========================================================================
def on_publish(client, userdata, mid) :
    print ("Message Published")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# on_connect
def on_connect(client, userdata, flags, rc):
    if (rc == 0):
        print("Connected Successful")
    else:
        print("Bad connection - Returned Code=", rc)

def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected result code: ", rc)

def on_subscribe(client, userdata, flags, rc):
    print("Subscribed")

#=========================================================================
def send() :
    client = mqtt.Client("clientA")
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_subscribe = on_subscribe
    client.on_publish = on_publish

    # Online Test Broker: "test.mosquitto.org"
    host      = "127.0.0.1"
    port      = 1883
    keepalive = 60

    # Default Connection statements
    print ("\nConnect to {}, keepalive {}".format(host, keepalive))
    client.connect(host=host, port=port, keepalive=keepalive)
    client.publish("client_connections", "Client with ID {" + str(client_id) + "} connected...")

    # Subscribe to image topic
    client.publish("image_check", IMAGEDTAILS)
    client.subscribe("prediction_receive")

    client.loop_forever()

def image_to_bytes(image_path):
    image = open(image_path, 'rb') 
    image_read = image.read() 
    image_64_encode = base64.encodestring(image_read)
    return image_64_encode

if __name__ == "__main__":
    send()
