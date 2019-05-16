from unittest.mock import MagicMock
import unittest 

import sys
import serial
import numpy
import time
import io

try:
    import tensorflow as tf
except ModuleNotFoundError:
    pass

sys.path.append('code/mqtt_protocol_module/')
sys.path.append('code/machine_learning_module/')

from label_image import Classify_Image

import base64
import time
import threading

class Test_Label_Image(unittest.TestCase):

    def test_load_graph(self):

        test_classify_image_obj = Classify_Image(logger_path="./code/")
        test_path = test_classify_image_obj.graph_path

        test_graph = test_classify_image_obj.load_graph(test_path)
        assert type(test_graph) == tf.Graph

    def test_read_tensor_from_image_file(self):
        test_classify_image_obj = Classify_Image(logger_path="./code/")
        test_file_name = "test.jpeg"

        # Mocks
        tf.read_file = MagicMock()
        tf.image.decode_jpeg = MagicMock()
        tf.image.decode_png = MagicMock()
        tf.image.decode_bmp = MagicMock()

        res = test_classify_image_obj.read_tensor_from_image_file(test_file_name)
        
        self.assertTrue(tf.read_file.call_count == 1)
        self.assertTrue(tf.image.decode_jpeg.call_count == 1)

        test_file_name = "test.png"
        res = test_classify_image_obj.read_tensor_from_image_file(test_file_name)

        self.assertTrue(tf.read_file.call_count == 2)
        self.assertTrue(tf.image.decode_jpeg.call_count == 1)
        self.assertTrue(tf.image.decode_png.call_count == 1)

        test_file_name = "test.bmp"
        res = test_classify_image_obj.read_tensor_from_image_file(test_file_name)

        self.assertTrue(tf.read_file.call_count == 3)
        self.assertTrue(tf.image.decode_jpeg.call_count == 1)
        self.assertTrue(tf.image.decode_png.call_count == 1)
        self.assertTrue(tf.image.decode_bmp.call_count == 1)

        # Due to MagicMocks
        self.assertTrue(res == None)

    def test_load_labels(self):
        test_output_labels = "highresistancebike\n" + "lowresistancebike\n" + "run\n" + "walk\n"
        test_classify_image_obj = Classify_Image(logger_path="./code/")
        label_file = io.StringIO(test_output_labels)

        tf.gfile.GFile = MagicMock(return_value=label_file)

        test_result = test_classify_image_obj.load_labels(test_output_labels)
        assert len(test_result) == 4

    def test_initialize_prediction_process(self):
        test_classify_image_obj = Classify_Image(logger_path="./code/")
        test_amount = 20
        test_classify_image_obj.publish_simulation_prediction_to_client = MagicMock()
        test_classify_image_obj.initialize_prediction_process(test_amount)
        self.assertTrue(test_classify_image_obj.publish_simulation_prediction_to_client.call_count == 1)

    def test_real_time_prediction_setup(self):
        test_classify_image_obj = Classify_Image(logger_path="./code/", test_mode=True)
        test_client = Test_Client("test_client")

        self.assertFalse(test_classify_image_obj.real_time_playback_mode)

        # Mocks
        test_classify_image_obj.read_tensor_from_image_file = MagicMock()
        tf.Session.run = MagicMock()

        # Execute test
        try:
            test_thread = threading.Thread(target=test_classify_image_obj.real_time_prediction_setup, args=[test_client])
            test_thread.start()

            time.sleep(10)
        finally:
            test_classify_image_obj.real_time_playback_mode = False
            self.assertTrue(test_classify_image_obj.read_tensor_from_image_file.call_count == 4)

    def test_predict_single_image(self):
        test_classify_image_obj = Classify_Image(logger_path="./code/", test_mode=True)
        test_client = Test_Client("test_client")
        test_output_labels = "highresistancebike\n" + "lowresistancebike\n" + "run\n" + "walk\n"
        test_results = numpy.array([255, 200, 150, 100, 100])
        label_file = io.StringIO(test_output_labels)

        tf.gfile.GFile = MagicMock(return_value=label_file)
        self.assertTrue(test_client.publish_call_count == 0)
        test_classify_image_obj.predict_single_image(test_results, test_client)
        self.assertTrue(test_client.publish_call_count == 1)

    def test_publish_simulation_prediction_to_client(self):
        test_classify_image_obj = Classify_Image(logger_path="./code/", test_mode=True)
        test_results = numpy.array([255, 200, 150, 100, 100])
        test_output_labels = "highresistancebike\n" + "lowresistancebike\n" + "run\n" + "walk\n"
        label_file = io.StringIO(test_output_labels)
        input_name = "import/" + test_classify_image_obj.input_layer
        output_name = "import/" + test_classify_image_obj.output_layer
        test_input_operation = test_classify_image_obj.graph.get_operation_by_name(input_name)
        test_output_operation = test_classify_image_obj.graph.get_operation_by_name(output_name)

        # Mocks
        test_classify_image_obj.client = Test_Client("test_client")

        test_classify_image_obj.load_labels = MagicMock(return_value=test_results)
        test_classify_image_obj.build_tensors_in_range = MagicMock(return_value=test_results)
        tf.Session.run = MagicMock(return_value=test_results)

        # Test Execution
        test_classify_image_obj.publish_simulation_prediction_to_client(None, test_input_operation, test_output_operation)
        self.assertTrue(test_classify_image_obj.client.publish_call_count == 5)

    def test_build_tensors_in_range(self):
        test_classify_image_obj = Classify_Image(logger_path="./code/", test_mode=True)
        test_tensor_range = 20

        # Mock
        test_classify_image_obj.read_tensor_from_image_file = MagicMock(return_value=None)

        # Test Execution
        tensors = test_classify_image_obj.build_tensors_in_range(test_classify_image_obj.test_dir, test_tensor_range, 
                            test_classify_image_obj.input_height, 
                            test_classify_image_obj.input_width, 
                            test_classify_image_obj.input_mean, 
                            test_classify_image_obj.input_std)

        self.assertTrue(test_classify_image_obj.read_tensor_from_image_file.call_count == 20)
        self.assertTrue(len(tensors) == 20)

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