import paho.mqtt.client as mqtt
import socket

"""
This class acts as a wrapper for the actual client connection.
This client is enabled using the paho.mqtt.client library.
"""
class Client_Controller:

        def __init__(self):
                self.client_id = socket.gethostname()
                self.client = mqtt.Client(self.client_id)