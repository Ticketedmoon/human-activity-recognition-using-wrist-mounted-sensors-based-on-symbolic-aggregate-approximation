import socket
import paho.mqtt.client as mqtt
import time
import base64
import sys

sys.path.append("../")

from symbolic_aggregate_approximation import SymbolicAggregateApproximation

class Client:

    def __init__(self):
        self.client_id = socket.gethostname()
        self.client = mqtt.Client(self.client_id)
        self.symbol_converter = SymbolicAggregateApproximation()
        self.has_disconnected = False

    def on_publish(self, client, userdata, mid) :
        print ("Client with ID {} has published message with ID {} Published".format(self.client_id, mid))

    # The callback for when a PUBLISH message is received from the server.
    # def on_message(self, client, userdata, msg):
    #     if (msg.topic == "prediction_receive"):
    #         message = msg.payload.decode("utf-8", "ignore")

    #         # When message received, update UI
    #         print("Client with ID {} received message: {}".format(self.client_id, message))

    def prevent_publish_mechanism(self):
        self.has_disconnected = True

    # on_connect
    def on_connect(self, client, userdata, flags, rc):
        if (rc == 0):
            print("Connected Successful")
        else:
            print("Bad connection - Returned Code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        client.publish("client_connections", "Client with ID {" + str(self.client_id) + "} disconnected...")
        print("Client with ID {} has been disconnected...".format(self.client_id))

    def on_subscribe(self, client, userdata, flags, rc):
        # Do nothing
        pass

    def disconnect(self):
        self.client.disconnect()
        sys.exit()

    def send(self) :
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish

        host      = "127.0.0.1"
        port      = 1883
        keepalive = 60

        # Default Connection statements
        print ("\nClient with ID {} connecting to {}... keepalive {}".format(self.client_id, host, keepalive))
        self.client.connect(host=host, port=port, keepalive=keepalive)

        if (not self.has_disconnected):
            self.client.publish("client_connections", "Client with ID {" + str(self.client_id) + "} connected...")
            self.client.subscribe("prediction_receive")
            print("Client with ID {} subscribing to topic {}".format(self.client_id, "prediction_receive"))

            self.client.loop_forever()

    def convert_and_send(self, csv_path):
        symbolic_data = self.symbol_converter.generate(csv_path)
        encoded_symbolic_data = base64.b64encode(bytes(symbolic_data, 'utf-8'))
        self.client.publish("sax_check", encoded_symbolic_data)

if __name__ == "__main__":
    client = Client()
    client.send()
