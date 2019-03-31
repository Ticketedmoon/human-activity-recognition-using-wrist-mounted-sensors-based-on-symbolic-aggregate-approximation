import socket
import paho.mqtt.client as mqtt
import time
import sys
import base64
import subprocess
import re

sys.path.append("../")

from label_image import initialize_prediction_process

client_id = socket.gethostname()

class Server:

    def on_connect(self, client, userdata, flags, rc):
        topic = "client_connections"
        msg = "Server connected to broker for serving HAR application"

        print("Publish to {} msg {}".format(topic, msg))
        client.publish(topic, msg, qos=2)

    def on_publish(self, client, userdata, mid) :
        print ("Message Published")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        if (msg.topic == "image_check"):
            self.image_receive(client, msg.payload)
        else:
            message = str(msg.payload)
            print(message[2:-1])

    # on_connect
    def on_connect(self, client, userdata, flags, rc):
        if (rc == 0):
            print("Server: Broker Connected Successful")
        else:
            print("Bad connection - Returned Code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        print("Disconnected result code: ", rc)

    def on_subscribe(self, client, userdata, flags, rc):
        # Do nothing
        pass

    def send(self):
        client = mqtt.Client("Server")
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        client.on_subscribe = self.on_subscribe

        host      = "127.0.0.1"
        port      = 1883
        keepalive = 60

        print ("\nServer: Connect to {}, keepalive {}".format(host, keepalive))
        client.connect(host=host, port=port, keepalive=keepalive)
        
        client.subscribe("client_connections")
        print("Server: Subscribing to topic {client_connections}")

        client.subscribe("image_check")
        print("Server: Subscribing to topic {image_check}")

        client.loop_forever()

    def image_receive(self, client, image_64_encode):
        print("Image decode request received.")
        image_64_decode = base64.decodestring(image_64_encode)
        with open("test.png", 'wb') as f:
            f.write(image_64_decode)  
        print("Image saved temporarily.")

        prediction = self.model_predict("test.png") 
        client.publish("prediction_receive", prediction)
        print("Activity classification: Resolved.")

    def model_predict(self, client_image_path):
        print("Resolving Classification...")
        p = subprocess.Popen(["python", "../label_image.py", "--graph=C:/tmp/output_graph.pb", "--labels=C:/tmp/output_labels.txt", "--input_layer=Placeholder",
                                    "--output_layer=final_result", "--image=../pixel_bitmaps/test/Walk/Walk-test-300.png"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        matches = re.findall("[wrlh]\w+ \d+\.\d+", str(out))
        return str(matches[0].split())

if __name__ == "__main__":
    server = Server()
    server.send()
