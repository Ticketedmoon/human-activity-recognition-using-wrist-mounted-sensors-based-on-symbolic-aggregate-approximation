import socket
import paho.mqtt.client as mqtt
import time

client_id = socket.gethostname()

#=========================================================================  
def on_connect(client, userdata, flags, rc):
    topic = "topic"
    msg = "MY_MESSAGE"

    print("Publish to {} msg {}".format(topic, msg))
    client.publish(topic, msg, qos=2)

#=========================================================================
def on_publish(client, userdata, mid) :
    print ("Message Published")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

# on_log
def on_log(client, userdata, level, buf):
    print("Log: " + buf)

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
    client = mqtt.Client("broker")
    client.on_connect = on_connect
    client.on_log = on_log
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    host      = "127.0.0.1"
    # broker      = "test.mosquitto.org"
    port      = 1883
    keepalive = 60
    # client.loop_forever()

    print ("\nConnect to {}, keepalive {}".format(host, keepalive))
    client.connect(host=host, port=port, keepalive=keepalive)
    
    client.subscribe("messages")
    client.loop_forever()
# end send()

#=========================================================================
if __name__ == "__main__":
    send()
# end if