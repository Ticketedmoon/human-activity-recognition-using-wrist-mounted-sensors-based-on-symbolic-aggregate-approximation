import paho.mqtt.client as mqtt
import socket

class Client_Controller:

        def __init__(self):
                self.client_id = socket.gethostname()
                self.client = mqtt.Client(self.client_id)