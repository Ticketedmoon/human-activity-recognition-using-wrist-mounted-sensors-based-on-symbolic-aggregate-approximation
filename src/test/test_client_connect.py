from unittest.mock import MagicMock
import unittest 
import sys
import os
from mock import patch
import numpy as np

sys.path.append("code/machine_learning_module")
from symbolic_aggregate_approximation import SymbolicAggregateApproximation

sys.path.append('code/mqtt_protocol_module/')

from client_connect import Client
import base64
import time
import threading

class Test_Client_Connect(unittest.TestCase):

    def test__init__(self):
        client = Client('./code/', True)
        self.assertTrue(type(client.symbol_converter) == SymbolicAggregateApproximation)
        self.assertFalse(client.has_disconnected)
        self.assertTrue(client.document_length_for_playback == 1)
        self.assertFalse(client.client_requesting_real_time_activity_recognition_access)
        self.assertFalse(client.connected_flag)

    def test_prevent_publish_mechanism(self):
        client = Client('./code/', True)
        self.assertFalse(client.has_disconnected)
        client.prevent_publish_mechanism()
        self.assertTrue(client.has_disconnected)

    def test_reset_publish_mechanism(self):
        client = Client('./code/', True)
        self.assertFalse(client.has_disconnected)
        client.reset_publish_mechanism()
        self.assertFalse(client.has_disconnected)
        client.prevent_publish_mechanism()
        self.assertTrue(client.has_disconnected)
        client.reset_publish_mechanism()
        self.assertFalse(client.has_disconnected)

    def test_on_connect(self):
        client = Client('./code/', True)
        client.on_connect(None, None, None, 0)
        self.assertTrue(client.connected_flag)
        client.on_connect(None, None, None, 1)
        self.assertFalse(client.connected_flag)

    def test_on_disconnect(self):
        client = Client('./code/', True)
        self.assertFalse(client.connected_flag)
        client.on_connect(None, None, None, 0)
        self.assertTrue(client.connected_flag)
        client.on_disconnect(None, None, None, 0)
        self.assertFalse(client.connected_flag)

    def test_is_connected_to_broker(self):
        client = Client('./code/', True)
        assert client.connected_flag == client.is_connected_to_broker()
    
    def test_send(self):
        client = Client('./code/', True)
        client.client.connect = MagicMock()
        client.client.publish = MagicMock()
        client.client.subscribe = MagicMock()
        client.client.loop_forever = MagicMock()
        client.send()

        # Positive case
        self.assertTrue(client.client.connect.call_count == 1)
        self.assertTrue(client.client.publish.call_count == 1)
        self.assertTrue(client.client.subscribe.call_count == 2)
        self.assertTrue(client.client.loop_forever.call_count == 1)

        client.has_disconnected = True
        client.send()

        # Negative case
        self.assertTrue(client.client.connect.call_count == 2)
        self.assertTrue(client.client.publish.call_count == 1)
        self.assertTrue(client.client.subscribe.call_count == 2)
        self.assertTrue(client.client.loop_forever.call_count == 1)

    def test_convert_and_send(self):
        client = Client('./code/', True)
        test_csv_path = "../../test.csv"

        client.symbol_converter.generate = MagicMock()
        client.send_activity_string_to_broker = MagicMock()

        client.convert_and_send(test_csv_path)
        self.assertTrue(client.csv_path == test_csv_path)
        self.assertTrue(client.symbol_converter.generate.call_count == 1)
        self.assertTrue(client.send_activity_string_to_broker.call_count == 1)
        

    def test_convert_and_send_real_time(self):
        client = Client('./code/', True)
        test_microvolts = [1750, 1850, 1775, 1500, 1400, 1300, 1200, 1666, 1222, 2351]
        test_datastream = np.array(test_microvolts)

        client.symbol_converter.generate_real_time = MagicMock()
        client.send_activity_string_to_broker = MagicMock()
        client.client.publish = MagicMock()

        client.convert_and_send_real_time(test_datastream)
        self.assertTrue(client.symbol_converter.generate_real_time.call_count == 1)
        self.assertTrue(client.send_activity_string_to_broker.call_count == 1)
        self.assertTrue(client.client_requesting_real_time_activity_recognition_access == True)
        self.assertTrue(client.client.publish.call_count == 1)

        client.convert_and_send_real_time(test_datastream)
        self.assertTrue(client.symbol_converter.generate_real_time.call_count == 2)
        self.assertTrue(client.send_activity_string_to_broker.call_count == 2)
        
        # Important test: Notice it is the same as the positive case, call count only 1
        self.assertTrue(client.client.publish.call_count == 1)

    def test_send_activity_string_to_broker(self):
        client = Client('./code/', True)
        test_sax_string = "aabbcc"

        client.client.publish = MagicMock()

        # Check None Case
        client.send_activity_string_to_broker(None)
        self.assertTrue(client.client.publish.call_count == 0)

        client.send_activity_string_to_broker(test_sax_string)
        self.assertTrue(client.client.publish.call_count == 1)

        client.send_activity_string_to_broker(test_sax_string)
        self.assertTrue(client.client.publish.call_count == 2)