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

    # Client Real-Time Flag
    client_requesting_real_time_activity_recognition_access = False

    def __init__(self):
        super(Client, self).__init__()
        self.symbol_converter = SymbolicAggregateApproximation(False)
        self.has_disconnected = False

    def on_publish(self, client, userdata, mid) :
        # self.logger.info("Client with ID {} has published message with ID {} Published".format(self.client_id, mid))
        pass
        
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

    def stop_real_time_connection(self):
        self.client.publish("real_time_check", "stop_real_time_recognition_for_client")

    def disconnect(self):
        self.stop_real_time_connection()
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
        self.send_activity_string_to_broker(symbolic_data)

    def convert_and_send_real_time(self, datastream):
        symbolic_data = self.symbol_converter.generate_real_time(datastream)
        self.send_activity_string_to_broker(symbolic_data, "real_time_input_feed")

        if not self.client_requesting_real_time_activity_recognition_access:
            self.client_requesting_real_time_activity_recognition_access = True
            self.logger.info("starting Real Time Activity Recognition...")
            self.client.publish("real_time_check", "start_real_time_recognition_for_client")

    def send_activity_string_to_broker(self, data, topic="sax_check"):
        if data is not None:
            self.document_length_for_playback = len(data)
            encoded_symbolic_data = base64.b64encode(bytes(data, 'utf-8'))
            self.client.publish(topic, encoded_symbolic_data)
            # self.logger.info("Client with ID {} has published Activity String data with length {} to Broker...".format(self.client_id, self.document_length_for_playback))
        else:
            self.logger.warning("Data conversion to string failed... Is there enough data in the csv submitted? Size {}".format(self.document_length_for_playback))

if __name__ == "__main__":
    client = Client()
    client.send()
