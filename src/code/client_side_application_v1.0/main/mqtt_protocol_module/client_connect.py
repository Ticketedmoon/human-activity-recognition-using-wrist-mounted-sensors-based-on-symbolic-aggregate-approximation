import socket
import sys

import base64
import paho.mqtt.client as mqtt

from logger_module.Logger import Logger
sys.path.append("./mqtt_protocol_module")
from client_controller import Client_Controller
from symbolic_aggregate_approximation import SymbolicAggregateApproximation

"""
This class is the connection between the client and server.
It interacts with the MQTT broker over the MQTT communication network.
There are various methods that involve publishing messages and data
across the network and these can be seen below. Messages are published
to a particular topic and the server can perform a specific function based
on the message type as well as based on the particular topic that the data has 
been published to.
"""
class Client(Client_Controller):

    # Constructor Method
    def __init__(self, logger_path="../../", test_mode=False):
        super(Client, self).__init__()

        # Logger
        self.logger = Logger(logger_path, "logs/Client", test_mode)

        # Symbolic Aggregate Approximation Object
        self.symbol_converter = SymbolicAggregateApproximation(False)
        
        # Boolean for connectivity
        self.has_disconnected = False

        # Document length currently being read
        self.document_length_for_playback = 1

        # Client Real-Time Flag
        self.client_requesting_real_time_activity_recognition_access = False

        # Client connected flag
        self.connected_flag = False

        # Path
        self.csv_path = None

    # This method is called every time the client publishes a message to the broker across the MQTT network.
    # This method has only been used for debugging purposes.
    def on_publish(self, client, userdata, mid) :
        pass
        
    # Setter method
    def prevent_publish_mechanism(self):
        self.has_disconnected = True

    # Setter method
    def reset_publish_mechanism(self):
        self.has_disconnected = False

    # on_connect method 
    # Is called whenever the client successfully connects with the broker.
    # This happens at the start of the application running
    def on_connect(self, client, userdata, flags, rc):
        if (rc == 0):
            self.logger.info("Connected Successful")
            self.connected_flag = True
        else:
            self.logger.info("Bad connection - Returned Code=" + str(rc))
            self.connected_flag = False

    # on_disconnect method
    # Called whenever client is disconnected from the broker.
    # Important to set connection flag to false here to ensure any active threads are aware.
    def on_disconnect(self, client, userdata, flags, rc=0):
        self.connected_flag = False
        self.logger.info("Client with ID {} has been disconnected...".format(self.client_id))

    # Similarly to the on_publish method above, do nothing when calle.
    # This again is only useful to me for debugging purposes.
    def on_subscribe(self, client, userdata, flags, rc):
        pass

    # Getter method
    def is_connected_to_broker(self):
        return self.connected_flag

    # Publish a message to the server that the real time functionality must be stopped.
    # The server will react to this and stop processing for that particular client.
    def stop_real_time_connection(self):
        self.client.publish("real_time_check", "stop_real_time_recognition_for_client")

    # If the client disconnects from the broker, ensure the real_time_connection has stopped.
    # Also ensure that the client flags have been set.
    def disconnect(self):
        self.stop_real_time_connection()
        self.client.disconnect()

    # Initialization method for MQTT client.
    # Instantiate broker connection with necessary parameters.
    # host/port/keepalive need not be global variables.
    # After client subscribes to necessary topics, ensure logging is done adequately for debugging.
    # Ensure client loops forever, we don't want the connection to end immediately after this method.
    # Client should be actively listening to the server. 
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
            # Set connected flag
            self.connected_flag = True

            # Client Objects and Prediction Subscription
            self.client.publish("client_connections", str(self.client_id))
            self.client.subscribe("prediction_receive")
            self.logger.info("Client with ID {} subscribing to topic {}".format(self.client_id, "prediction_receive"))

            # Clock reset for UI
            self.client.subscribe("clock_reset")
            self.logger.info("Client with ID {} subscribing to topic {}".format(self.client_id, "clock_reset"))
            
            # Loop forever until we receive a disconnection message from the application.
            # An example might be when they close the window for example.
            self.client.loop_forever()

        # If the control flow reaches this point, we know a disconnection between client-broker has occurred.
        self.connected_flag = False

    # Method requirement for activity recognition playback function.
    # Convert the string to base64 and send it across the network.
    def convert_and_send(self, csv_path):
        self.csv_path = csv_path
        symbolic_data = self.symbol_converter.generate(csv_path)
        self.send_activity_string_to_broker(symbolic_data)

    # Method different to the above yet contains similar properties.
    # Method must publish to a different topic and generate the string in a different manner.
    def convert_and_send_real_time(self, datastream):
        symbolic_data = self.symbol_converter.generate_real_time(datastream)
        self.send_activity_string_to_broker(symbolic_data, "real_time_input_feed")

        if not self.client_requesting_real_time_activity_recognition_access:
            self.client_requesting_real_time_activity_recognition_access = True
            self.logger.info("starting Real Time Activity Recognition...")
            self.client.publish("real_time_check", "start_real_time_recognition_for_client")

    # Return Vector representation of a time series.
    # Numpy + Pandas used for this
    def get_data_vector_properties(self):
        return self.symbol_converter.get_data_vector_properties(self.csv_path)

    # 1. Set the document length based on the time-series data size.
    #    - This is useful for the progress meters found in the controller pane.
    # 2. Encode data to base64 for encrypted and efficient transmission.
    # 3. Publish the encoded information to the topic requested via parameter insertion. 
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
