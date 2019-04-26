import socket
import sys

import base64
import paho.mqtt.client as mqtt

# ../ from Desktop Application
# ../../ from MQTT-Protocol Module
sys.path.append("../")
from logger_module.Logger import Logger

sys.path.append("../../mqtt_protocol_module")
from client_controller import Client_Controller

sys.path.append("../../machine_learning_module")
from symbolic_aggregate_approximation import SymbolicAggregateApproximation

class Client(Client_Controller):

    # Logger
    logger = Logger("../../", "logs/Client")

    # Document length currently being read
    document_length_for_playback = 1

    def __init__(self, client_object=None):
        if client_object is None:
            super(Client, self).__init__()
            self.symbol_converter = SymbolicAggregateApproximation(False)
            self.has_disconnected = False
        else:
            self = client_object

    def on_publish(self, client, userdata, mid) :
        self.logger.info("Client with ID {} has published message with ID {} Published".format(self.client_id, mid))
        
    def prevent_publish_mechanism(self):
        self.has_disconnected = True

    def reset_publish_mechanism(self):
        self.has_disconnected = False

    # on_connect
    def on_connect(self, client, userdata, flags, rc):
        if (rc == 0):
            self.logger.info("Connected Successful")
        else:
            self.logger.info("Bad connection - Returned Code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        self.logger.info("Client with ID {} has been disconnected...".format(self.client_id))

    def on_subscribe(self, client, userdata, flags, rc):
        # Do nothing
        pass

    def disconnect(self):
        self.client.disconnect()

    def send(self) :
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish

        host      = "127.0.0.1"
        port      = 1883
        keepalive = 60

        # Default Connection statements
        self.logger.info("\nClient with ID {} connecting to {}... keepalive {}".format(self.client_id, host, keepalive))
        self.client.connect(host=host, port=port, keepalive=keepalive)

        if (not self.has_disconnected):
            # Client Objects and Prediction Subscription
            self.client.publish("client_connections", str(self.client_id))
            self.client.subscribe("prediction_receive")
            self.logger.info("Client with ID {} subscribing to topic {}".format(self.client_id, "prediction_receive"))

            # Clock reset for UI
            self.client.subscribe("clock_reset")
            self.logger.info("Client with ID {} subscribing to topic {}".format(self.client_id, "clock_reset"))
            self.client.loop_forever()

    def convert_and_send(self, csv_path):
        symbolic_data = self.symbol_converter.generate(csv_path)
        self.document_length_for_playback = len(symbolic_data)
        encoded_symbolic_data = base64.b64encode(bytes(symbolic_data, 'utf-8'))
        self.client.publish("sax_check", encoded_symbolic_data)
        self.logger.info("Client with ID {} has published Activity String data with length {} to Broker...".format(self.client_id, self.document_length_for_playback))

if __name__ == "__main__":
    client = Client()
    client.send()
