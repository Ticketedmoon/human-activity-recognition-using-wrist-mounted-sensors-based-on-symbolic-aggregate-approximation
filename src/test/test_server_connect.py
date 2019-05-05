from unittest.mock import MagicMock
import unittest 
import sys
import os
from mock import patch

sys.path.append('code/mqtt_protocol_module/')

from server_connect import Server
import base64
import time
import threading

class Test_Server_Connect(unittest.TestCase):

    def test_on_message_topic_sax_check(self):
        server = Server(logger_path="./code/", test_mode=True)
        server.start_playback_mode_loop = MagicMock()
        test_message = Test_Message("sax_check", "aabbcc")
        test_message.payload = test_message.encoded_payload
        test_client = None
        test_user_data = None
        self.assertFalse(server.is_exercise_simulation_active)
        server.on_message(test_client, test_user_data, test_message)
        self.assertTrue(server.is_exercise_simulation_active)

    def test_on_message_topic_real_time_check(self):
        server = Server(logger_path="./code/", test_mode=True)
        server.start_real_time_mode_loop = MagicMock()
        server.classifier.real_time_prediction_setup = MagicMock()
        test_client = None
        test_user_data = None

        # Test prior to any on_message
        self.assertFalse(server.real_time_playback_is_active)

        # Test Positive Case
        test_message = Test_Message("real_time_check", "start_real_time_recognition_for_client")
        test_message.payload = bytes(test_message.payload, 'utf-8')
        server.on_message(test_client, test_user_data, test_message)
        self.assertTrue(server.real_time_playback_is_active)
        # Test Negative Case

        test_message = Test_Message("real_time_check", "stop_real_time_recognition_for_client")
        test_message.payload = bytes(test_message.payload, 'utf-8')
        server.on_message(test_client, test_user_data, test_message)
        self.assertFalse(server.real_time_playback_is_active)

    def test_on_message_topic_real_time_input_feed(self):
        server = Server(logger_path="./code/", test_mode=True)
        test_client = "test_client"
        test_user_data = None
        test_message = Test_Message("real_time_input_feed", "___")
        test_message.payload = test_message.encoded_payload
        self.assertTrue(len(server.client_input_buffer) == 0) 
        server.on_message(test_client, test_user_data, test_message)
        self.assertTrue(len(server.client_input_buffer) > 0) 
        self.assertTrue(len(server.client_input_buffer[test_client]) > 0)
        self.assertTrue(server.client_input_buffer[test_client][0] == "___")

    def test_on_message_topic_disconnections(self):
        server = Server(logger_path="./code/", test_mode=True)
        test_client = "test_client"
        test_user_data = None
        server.classifier.discontinue_client_connection = MagicMock()

        # Set flags of server
        server.is_exercise_simulation_active = True
        server.real_time_playback_is_active = True
        server.client_objects[test_client] = "test"
        
        test_message = Test_Message("disconnections", "")
        server.on_message(test_client, test_user_data, test_message)

        # Check flags have been switched
        self.assertFalse(server.is_exercise_simulation_active)
        self.assertFalse(server.real_time_playback_is_active)

        # Check that classifier call has been made
        assert server.classifier.discontinue_client_connection.call_count == 1

    def test_on_message_topic_client_connections(self):
        server = Server(logger_path="./code/", test_mode=True)
        test_client = "test_client"
        test_user_data = None

        self.assertTrue(test_client not in server.client_objects.keys())

        test_message = Test_Message("client_connections", test_client)
        test_message.payload = bytes(test_message.payload, 'utf-8')
        server.on_message(test_client, test_user_data, test_message)

        self.assertTrue(test_client in server.client_objects.keys())
        self.assertTrue(server.client_objects[test_client] is not None)

    def test_send(self):
        test_server = Server(logger_path="./code/", test_mode=True)
        test_server.server.connect = MagicMock()
        test_server.server.subscribe = MagicMock()
        test_server.server.loop_forever = MagicMock()

        test_server.send()

        assert test_server.server.connect.call_count == 1
        assert test_server.server.subscribe.call_count == 5
        assert test_server.server.loop_forever.call_count == 1

    def test_start_playback_mode_loop(self):
        # Set up
        server = Server(logger_path="./code/", test_mode=True)
        test_client_name = "test_client"
        test_client_obj = Test_Client(test_client_name)
        server.client_objects[test_client_obj] = test_client_name
        test_user_data = None
        test_sax_string = "aabbcc"
        server.image_encode_activity = MagicMock()

        # Testing Stage
        # Test: Negative Case
        server.start_playback_mode_loop(test_client_obj, test_sax_string)
        self.assertTrue(test_client_obj.publish_call_count == 1)
        assert server.image_encode_activity.call_count == 0

        # Test: Positive Case
        # Unit test - Not integration, no linkage of functions.
        server.is_exercise_simulation_active = True
        test_loop = threading.Thread(target=server.start_playback_mode_loop, args=[test_client_obj, test_sax_string])
        test_loop.start()
        time.sleep(0.5)
        server.is_exercise_simulation_active = False
        assert server.image_encode_activity.call_count > 10000

    def test_start_real_time_mode_loop(self):
        # Set up
        server = Server(logger_path="./code/", test_mode=True)
        test_client_name = "test_client"
        test_client_obj = Test_Client(test_client_name)
        test_user_data = None
        test_sax_string = "aabbcc"

        # Mocks
        server.destroy_temp_folder = MagicMock()
        server.image_encode_activity = MagicMock()
        server.server_bitmap_generator.generate_single_bitmap_real_time = MagicMock()

        # Test Try block - Negative Case
        server.real_time_playback_is_active = False
        test_loop = threading.Thread(target=server.start_real_time_mode_loop, args=[test_client_obj])
        test_loop.start()

        time.sleep(0.5)
        self.assertTrue(len(server.client_input_buffer.keys()) == 0)
        assert server.destroy_temp_folder.call_count == 0
        
        server.client_input_buffer[test_client_obj] = []
        time.sleep(3.5)

        # Test Finally
        assert server.destroy_temp_folder.call_count == 1

         # Test Try block (Again) - Positive Case
        server.real_time_playback_is_active = True
        test_loop = threading.Thread(target=server.start_real_time_mode_loop, args=[test_client_obj])
        test_loop.start()

        self.assertTrue(len(server.client_input_buffer.keys()) == 1)
        
        server.client_input_buffer[test_client_obj] = [test_client_name]
        time.sleep(3.5)
        server.real_time_playback_is_active = False

        self.assertTrue(server.server_bitmap_generator.generate_single_bitmap_real_time.call_count > 0)
        time.sleep(0.5)

        assert server.destroy_temp_folder.call_count == 2

    def test_image_encode_activity(self):
        # Set up
        server = Server(logger_path="./code/", test_mode=True)
        test_client_name = "test_client"
        test_client_obj = Test_Client(test_client_name)
        test_user_data = None
        test_sax_string = "aabbcc" * 1000

        # Mocks
        server.simulate_activity_recognition = MagicMock()
        server.server_bitmap_generator.generate_single_bitmap = MagicMock()

        server.image_encode_activity(test_client_obj, test_sax_string, 0, 20)
        assert server.server_bitmap_generator.generate_single_bitmap.call_count == 20
        assert server.simulate_activity_recognition.call_count == 1

    def test_simulate_activity_recognition(self):
        # Set up
        server = Server(logger_path="./code/", dir_path="./code/mqtt_protocol_module/temp", test_mode=True)
        test_client_name = "test_client"
        test_client_obj = Test_Client(test_client_name)
        test_user_data = None
        test_sax_string = "aabbcc" * 1000

        # Mocks
        server.model_predict = MagicMock()
        server.destroy_temp_folder = MagicMock()

        # Testing Instantiate
        server.simulate_activity_recognition(test_client_obj, 20)

        assert server.model_predict.call_count == 1
        assert server.destroy_temp_folder.call_count == 1

    def test_model_predict(self):
        server = Server(logger_path="./code/", test_mode=True)
        test_client_name = "test_client"
        test_client_obj = Test_Client(test_client_name)
        
         # Mocks
        server.classifier.initialize_prediction_process = MagicMock()

        # Testing Instantiate
        server.model_predict(test_client_obj, 20)
        assert server.classifier.initialize_prediction_process.call_count == 1

    def test_destroy_temp_folder(self):
        server = Server(logger_path="./code/", dir_path="./code/mqtt_protocol_module/temp", test_mode=True)
        test_client_name = "test_client"
        test_client_obj = Test_Client(test_client_name)

        # Step #0: Clear the directory prior to test
        server.destroy_temp_folder()

        # Step #1: Create some files, store them in ./temp
        create_file_helper(server.dir_path + "/testA")
        create_file_helper(server.dir_path + "/testB")
        create_file_helper(server.dir_path + "/testC")

        # -1 for the .gitkeep file
        directory_size = len(os.listdir(server.dir_path)) - 1
        # Step #2: Assert that X amount of files exist
        self.assertTrue(directory_size == 3)

        # Step #3: Call the method in question.
        server.destroy_temp_folder()

        # Step #4: Assert that 0 files exist
        directory_size = len(os.listdir(server.dir_path)) - 1
        self.assertTrue(directory_size == 0)


def create_file_helper(path):
    with open(path, 'a'):
        os.utime(path, None)


class Test_Message:

    def __init__(self, topic, payload):
        self.topic = topic
        self.payload = payload
        self.encoded_payload = base64.b64encode(bytes(payload, 'utf-8'))

class Test_Client:

    publish_call_count = 0

    def __init__(self, client_id):
        self.client_id = client_id
    
    def publish(self, topic, message):
        self.publish_call_count += 1
