# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

import numpy as np
import tensorflow as tf
import time, os, re, base64
import threading
import sys

sys.path.append("../../")
from logger_module.Logger import Logger

class Classify_Image:

    logger = Logger("../../", "logs/Classify_Image")

    def __init__(self, default_image="tensorflow/examples/label_image/data/grace_hopper.jpg",
        graph_path="C:/tmp/output_graph.pb", 
        label_path="C:/tmp/output_labels.txt",
        test_dir="./pixel_bitmaps/test/Walk", input_layer="Placeholder", 
        output_layer="final_result"):
        
        self.graph_path = graph_path
        self.test_dir = test_dir
        self.label_path = label_path
        self.input_height = 299
        self.input_width = 299
        self.input_mean = 0
        self.input_std = 255
        self.input_layer = input_layer
        self.output_layer = output_layer

        self.graph = self.load_graph(self.graph_path)

    def load_graph(self, model_file):
        graph = tf.Graph()
        graph_def = tf.GraphDef()

        with open(model_file, "rb") as f:
          graph_def.ParseFromString(f.read())

        with graph.as_default():
          tf.import_graph_def(graph_def)

        return graph

    def read_tensor_from_image_file(self, file_name,
                                    input_height=299,
                                    input_width=299,
                                    input_mean=0,
                                    input_std=255):
        try:
          input_name = "file_reader"
          output_name = "normalized"
          file_reader = tf.read_file(file_name, input_name)
          if file_name.endswith(".png"):
            image_reader = tf.image.decode_png(
                file_reader, channels=3, name="png_reader")
          elif file_name.endswith(".gif"):
            image_reader = tf.squeeze(
                tf.image.decode_gif(file_reader, name="gif_reader"))
          elif file_name.endswith(".bmp"):
            image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
          else:
            image_reader = tf.image.decode_jpeg(
                file_reader, channels=3, name="jpeg_reader")
          float_caster = tf.cast(image_reader, tf.float32)
          dims_expander = tf.expand_dims(float_caster, 0)
          resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
          normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
          sess = tf.Session()
          result = sess.run(normalized)

          return result
        except:
          pass

    def load_labels(self, label_file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
          label.append(l.rstrip())
        return label

    def initialize_prediction_process(self, tensorRange, client=None):
        input_name = "import/" + self.input_layer
        output_name = "import/" + self.output_layer
        input_operation = self.graph.get_operation_by_name(input_name)
        output_operation = self.graph.get_operation_by_name(output_name)
        self.publish_simulation_prediction_to_client(tensorRange, input_operation, output_operation, client)

  #        client.publish("clock_reset", "Reset")

    def publish_simulation_prediction_to_client(self, tensorRange, input_operation, output_operation, client):
        if self.test_dir != None:
          tensors = self.build_tensors_in_range(self.test_dir, tensorRange, self.input_height, self.input_width, self.input_mean, self.input_std)
        
        with tf.Session(graph=self.graph) as sess:
          for tensor in tensors:
            results = sess.run(output_operation.outputs[0], {
                input_operation.outputs[0]: tensor
            })
            results = np.squeeze(results)

            top_k = results.argsort()[-5:][::-1]
            labels = self.load_labels(self.label_path)
            prediction_label, prediction_accuracy = labels[top_k[0]], results[top_k[0]]

            if (client != None):
              prediction = str([prediction_label, prediction_accuracy])
              encoded_prediction = base64.b64encode(bytes(prediction, 'utf-8'))
              client.publish("prediction_receive", encoded_prediction)
              time.sleep(1)


    # TODO: make this more flexible via the file_name formatting.
    def build_tensors_in_range(self, test_image_dir, tensorRange, input_height, input_width, input_mean, input_std):
        tensors = []

        try:
          for i in range(tensorRange):
              file_name = "{}/activity-{}.jpeg".format(test_image_dir, i)
              t = self.read_tensor_from_image_file(
                  file_name,
                  input_height=input_height,
                  input_width=input_width,
                  input_mean=input_mean,
                  input_std=input_std)
              tensors.append(t)
        except:
            pass

        finally:
          self.logger.info("Tensor Creation Complete for Simulation Range {}".format(tensorRange))
          return tensors

def main():
    classifier = Classify_Image()
    classifier.initialize_prediction_process()

if __name__ == "__main__":
  main()