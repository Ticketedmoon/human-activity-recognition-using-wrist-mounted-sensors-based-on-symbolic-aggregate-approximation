import socket
import paho.mqtt.client as mqtt
import time

client_id = socket.gethostname()

#=========================================================================  
def on_connect(client, userdata, flags, rc):
    topic = "client_connections"
    msg = "Server connected to broker for serving HAR application"

    print("Publish to {} msg {}".format(topic, msg))
    client.publish(topic, msg, qos=2)

#=========================================================================
def on_publish(client, userdata, mid) :
    print ("Message Published")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(message[2:-1])

# on_log
#def on_log(client, userdata, level, buf):
    #client.publish("connection_log", "Connected to Mosquitto Broker...")

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

def send() :
    client = mqtt.Client("Server")
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    host      = "127.0.0.1"
    port      = 1883
    keepalive = 60

    print ("\nConnect to {}, keepalive {}".format(host, keepalive))
    client.connect(host=host, port=port, keepalive=keepalive)
    
    client.subscribe("client_connections")

    client.loop_forever()

# Modify
def image_receive():
    image_64_decode = base64.decodestring(image_64_encode)
    image_result = open('deer_decode.gif', 'wb') # create a writable image and write the decoding result image_result.write(image_64_decode)

if __name__ == "__main__":
    send()
