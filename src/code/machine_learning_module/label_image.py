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

class Classify_Image:

    tensor_shift = 50

    def __init__(self, default_image="tensorflow/examples/label_image/data/grace_hopper.jpg",
        graph_path="tensorflow/examples/label_image/data/inception_v3_2016_08_28_frozen.pb", 
        label_path="tensorflow/examples/label_image/data/imagenet_slim_labels.txt",
         test_dir=None, input_layer="input", output_layer="InceptionV3/Predictions/Reshape_1"):
      self.graph_path = graph_path
      self.test_dir = test_dir
      self.label_path = label_path
      self.input_height = 299
      self.input_width = 299
      self.input_mean = 0
      self.input_std = 255
      self.input_layer = input_layer
      self.output_layer = output_layer

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

    def load_labels(self, label_file):
      label = []
      proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
      for l in proto_as_ascii_lines:
        label.append(l.rstrip())
      return label

    def initialize_prediction_process(self):

      graph = self.load_graph(self.graph_path)

      input_name = "import/" + self.input_layer
      output_name = "import/" + self.output_layer
      input_operation = graph.get_operation_by_name(input_name)
      output_operation = graph.get_operation_by_name(output_name)

      if self.test_dir != None:
        tensors = self.build_tensors_in_range(self.test_dir, self.input_height, self.input_width, self.input_mean, self.input_std)

        with tf.Session(graph=graph) as sess:
          for tensor in tensors:
            results = sess.run(output_operation.outputs[0], {
                input_operation.outputs[0]: tensor
            })
            results = np.squeeze(results)

            top_k = results.argsort()[-5:][::-1]
            labels = self.load_labels(self.label_path)
            for i in top_k:
              print(labels[i], results[i])

            prediction = str([top_k[0], labels[0]])
            encoded_prediction = base64.b64encode(bytes(prediction, 'utf-8'))
            client.publish("prediction_receive", encoded_prediction)

      # return results, label_file

    def build_tensors_in_range(self, test_image_dir, input_height, input_width, input_mean, input_std):

      tensors = []

      for i in range(self.tensor_shift - 50, self.tensor_shift):
        try:
          file_name = "{}/{}-test-{}.jpeg".format(test_image_dir, "Walk", i)
          t = self.read_tensor_from_image_file(
              file_name,
              input_height=input_height,
              input_width=input_width,
              input_mean=input_mean,
              input_std=input_std)

          tensors.append(t)
          print(file_name + " - Tensor Stored")
        except:
          print("problem in tensor creation (probably while loop out of range)")

      self.tensor_shift += 50
      return tensors;      

def main():
  graph_path = "C:/tmp/output_graph.pb"
  label_path = "C:/tmp/output_labels.txt"
  test_dir = "./pixel_bitmaps/test/Walk"
  input_layer = "Placeholder"
  output_layer = "final_result"

  classifier = Classify_Image(graph_path=graph_path, label_path=label_path, test_dir=test_dir,
          input_layer=input_layer, output_layer=output_layer)
  classifier.initialize_prediction_process()

if __name__ == "__main__":
  main()