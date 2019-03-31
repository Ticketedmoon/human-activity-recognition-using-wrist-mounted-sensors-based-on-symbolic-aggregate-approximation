import socket
import paho.mqtt.client as mqtt
import time
import base64

class Client:

    client_id = socket.gethostname()

    #=========================================================================
    def on_publish(self, client, userdata, mid) :
        print ("Client: Message with ID {} Published".format(mid))

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        if (msg.topic == "prediction_receive"):
            message = msg.payload.decode("utf-8", "ignore")
            print(message)

    # on_connect
    def on_connect(self, client, userdata, flags, rc):
        if (rc == 0):
            print("Connected Successful")
        else:
            print("Bad connection - Returned Code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        client.publish("client_connections", "Client with ID {" + str(self.client_id) + "} disconnected...")
        print("Disconnected result code: ", rc)

    def on_subscribe(self, client, userdata, flags, rc):
        # Do nothing
        pass

    #=========================================================================
    def send(self) :
        client = mqtt.Client("clientA")
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        client.on_subscribe = self.on_subscribe
        client.on_publish = self.on_publish

        # Online Test Broker: "test.mosquitto.org"
        host      = "127.0.0.1"
        port      = 1883
        keepalive = 60

        # Default Connection statements
        print ("\nClient: Connect to {}, keepalive {}".format(host, keepalive))
        client.connect(host=host, port=port, keepalive=keepalive)

        client.publish("client_connections", "Client with ID {" + str(self.client_id) + "} connected...")

        client.subscribe("prediction_receive")
        print("Client: Subscribing to topic {prediction_receive}")

        self.send_compressed_image_for_prediction(client, "../pixel_bitmaps/test/Walk/Walk-test-1.png")

        client.loop_forever()

    # TODO: Remember to Disconnect client when program executes | Done via the desktop application
    def send_compressed_image_for_prediction(self, client, image_path):
        encoded_image = self.image_to_bytes(image_path)
        client.publish("image_check", encoded_image)

    def image_to_bytes(self, image_path):
        image = open(image_path, 'rb') 
        image_read = image.read() 
        image_64_encode = base64.encodestring(image_read)
        return image_64_encode

if __name__ == "__main__":
    client = Client()
    client.send()
