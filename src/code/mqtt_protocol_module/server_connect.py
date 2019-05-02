import glob
import socket
import subprocess
import sys
import threading

import base64
import os
import paho.mqtt.client as mqtt
import re
import tensorflow as tf
import time

sys.path.append("../")
from logger_module.Logger import Logger

sys.path.append("../machine_learning_module")
from label_image import Classify_Image
from bitmap_generator import BitmapGenerator

class Server:

    # Logger
    logger = Logger("../", "logs/Server")

    # Bitmap Generator
    server_bitmap_generator = BitmapGenerator()

    # Temporary directory for image storage
    temporary_image_directory = "./temp"

    # Flag for simulation playback
    is_exercise_simulation_active = False
    real_time_playback_is_active = False

    # Dictionary / Hashmap of client Objects to Client Names
    client_objects = {} 

    # Client to Image mapping
    client_input_buffer = {}

    def on_publish(self, client, userdata, mid) :
         self.logger.info("Server: Message Published")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        if (msg.topic == "sax_check"):
            self.logger.info("Server: Human Activity Simulation by CSV received...")
            self.is_exercise_simulation_active = True
            sax_string = base64.decodestring(msg.payload)
            sax_string_decoded = str(sax_string)[2:-1]
            initialize_simulation_loop = threading.Thread(target=self.start_playback_mode_loop, args=[client, sax_string_decoded])
            initialize_simulation_loop.start()
        elif (msg.topic == "real_time_check"):
            # Start the thread that will loop and take from the buffer
            message = msg.payload.decode('utf-8')
            if (message == "start_real_time_recognition_for_client"):
                self.real_time_playback_is_active = True
                initialize_real_time_loop = threading.Thread(target=self.start_real_time_mode_loop, args=[client])
                start_tensorflow_loop = threading.Thread(target=self.classifier.real_time_prediction_setup, args=[client])
                initialize_real_time_loop.start()
                start_tensorflow_loop.start()
            elif (message == "stop_real_time_recognition_for_client"):
                self.real_time_playback_is_active = False
        elif (msg.topic == "real_time_input_feed"):
            # Simply add the message data/payload to the buffer
            sax_string = base64.decodestring(msg.payload)
            sax_string_decoded = str(sax_string)[2:-1]
            if client not in self.client_input_buffer.keys():
                self.client_input_buffer[client] = []
            self.client_input_buffer[client].insert(0, sax_string_decoded)
        elif(msg.topic == "disconnections"):
            self.logger.info("Server: Client With ID {} Disconnected - Stoping Simulation if active... {}".format(self.client_objects[client], self.is_exercise_simulation_active))
            self.is_exercise_simulation_active = False
            self.real_time_playback_is_active = False
            self.classifier.discontinue_client_connection()
        elif(msg.topic == "client_connections"):
            client_connection_id = msg.payload.decode('utf-8')
            self.client_objects[client] = client_connection_id
            self.logger.info("Server: Client with ID {} Connected...".format(client_connection_id))
        else:
            self.logger.warning("Non-specific topic published to...")

    def on_disconnect(self, client, userdata, flags, rc=0):
        self.logger.info("Disconnected result code: ", rc)

    def on_subscribe(self, client, userdata, flags, rc):
        # Do nothing
        pass

    def send(self):
        server = mqtt.Client("Server")
        server.on_disconnect = self.on_disconnect
        server.on_message = self.on_message
        server.on_subscribe = self.on_subscribe
        
        # Build Classifier all cases will use
        self.dir_path = "./temp"
        self.classifier = Classify_Image(test_dir=self.dir_path)

        host      = "127.0.0.1"
        port      = 1883
        keepalive = 60

        self.logger.info("\nServer: Connect to {}, keepalive {}".format(host, keepalive))
        server.connect(host=host, port=port, keepalive=keepalive)
        
        server.subscribe("client_connections")
        self.logger.info("Server: Subscribing to topic {client_connections}")

        server.subscribe("disconnections")
        self.logger.info("Server: Subscribing to topic {disconnections}")

        server.subscribe("sax_check")
        self.logger.info("Server: Subscribing to topic {sax_check}")

        server.subscribe("real_time_check")
        self.logger.info("Server: Subscribing to topic {real_time_check}")

        server.subscribe("real_time_input_feed")
        self.logger.info("Server: Subscribing to topic {real_time_input_feed}")

        server.loop_forever()

    # Playback Mode
    def start_playback_mode_loop(self, client, decoded_sax_string):
        startLetterIndex, endLetterIndex = 0, 20
        batch_size = endLetterIndex - startLetterIndex

        while(self.is_exercise_simulation_active):
            self.logger.info("Loading next batch of {} simulation images...".format(batch_size))
            self.image_encode_activity(client, decoded_sax_string, startLetterIndex, endLetterIndex)
            startLetterIndex += 20
            endLetterIndex += 20
            
        self.logger.info("Human Activity Simulation Playback complete for client with ID {}".format(str(self.client_objects[client])))
        # Reset clock
        client.publish("clock_reset", "notify")

    # Real Time Mode
    def start_real_time_mode_loop(self, client):
        try:
            while len(self.client_input_buffer.keys()) == 0:
                self.logger.warning("Waiting for client buffer to append...")
                time.sleep(3)

            while self.real_time_playback_is_active:
                # 1. Pop first item from buffer
                if len(self.client_input_buffer[client]) > 0:
                    activity_item = self.client_input_buffer[client].pop(0)
                    # 2. Build image from it
                    self.server_bitmap_generator.generate_single_bitmap_real_time(activity_item)
        finally:
            # Clear buffer after usage to save memory
            self.logger.warning("clearing client real-time buffer cache")
            self.client_input_buffer[client].clear()
            self.destroy_temp_folder()

    # Image sizes are 100 x 100
    # shift 256 is equivalent of shifting 1-second
    # TODO: Create Loading Pane for this
    def image_encode_activity(self, client, sax_string_decoded, startRange, endRange):
        initialRange = startRange
        try:
            shift_position = startRange
            bitmap_size = 32 * 32
            while(startRange < endRange):
                substring = sax_string_decoded[startRange:bitmap_size + shift_position]
                self.server_bitmap_generator.generate_single_bitmap(substring)   
                shift_position += 256
                startRange += 1
            self.logger.info("Simulation Images Resolved for range [{} - {}]".format(initialRange, endRange))

        finally:
            # Perform activity recognition
            tensorRange = endRange - initialRange
            self.simulate_activity_recognition(client, tensorRange)

    def simulate_activity_recognition(self, client, tensorRange):
        total_files = len(os.listdir(self.dir_path))
        try:
            self.logger.info("Starting Model Prediction with Images in {}".format(self.dir_path))
            self.model_predict(client, tensorRange)
        finally:
            # After Simulation Activity Recognition Function Complete => Destroy Temp Folder
            self.logger.warning("Destroying Temporaries...")
            self.destroy_temp_folder()

    def model_predict(self, client, tensorRange):
        self.classifier.initialize_prediction_process(tensorRange, client)

    # TODO: Use this function to dissect how to only load the graph one time - drastically speeding up the server side.
    # Additionally, perhaps all bitmap images for the specified csv should be generated first, and then
    # Time.sleep(X seconds) between each activity prediction - also take into account potential network latency.
    def run_graph(self, src, labels, input_layer_name, output_layer_name, num_top_predictions):
        with tf.Session() as sess:
            i=0
            #outfile=open('submit.txt','w')
            #outfile.write('image_id, label \n')
            for f in os.listdir(dest):
                image_data=load_image(os.path.join(dest,test[i]+'.jpg'))
                #image_data=load_image(os.path.join(src,f))
                softmax_tensor = sess.graph.get_tensor_by_name(output_layer_name)
                predictions, = sess.run(softmax_tensor, {input_layer_name: image_data})

                # Sort to show labels in order of confidence
                top_k = predictions.argsort()[-num_top_predictions:][::-1]
                for node_id in top_k:
                    human_string = labels[node_id]
                    score = predictions[node_id]
                    #print('%s (score = %.5f) %s , %s' % (test[i], human_string))
                    self.logger.info('%s, %s' % (test[i], human_string))
                    #outfile.write(test[i]+', '+human_string+'\n')
                i+=1
        return 0

    def destroy_temp_folder(self):
        files = glob.glob('./temp/*')
        for f in files:
            os.remove(f)

        # Also reset counter
        self.server_bitmap_generator.reset_activity_counter()

if __name__ == "__main__":
    server = Server()
    server.send()
