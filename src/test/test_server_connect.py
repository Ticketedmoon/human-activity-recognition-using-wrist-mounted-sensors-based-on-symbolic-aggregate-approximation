from unittest.mock import MagicMock
import unittest 
import sys
from mock import patch

sys.path.append('./code/mqtt_protocol_module/')

# from server_connect import Server
import base64

# class Test_Server_Connect(unittest.TestCase):

#     def test_on_message(self):
#         server = Server()
#         server.start_playback_mode_loop = MagicMock()
#         test_message = Test_Message("sax_check", "aabbcc")
#         test_client = None
#         test_user_data = None
#         self.assertTrue(not server.is_exercise_simulation_active)
#         server.on_message(test_message, test_client, test_user_data)
#         self.assertTrue(server.is_exercise_simulation_active)
#         pass

# class Test_Message:

#     def __init__(self, topic, payload):
#         self.topic = topic
#         self.payload = base64.b64encode(bytes(payload, utf-8))