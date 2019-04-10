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

    # Dictionary / Hashmap of client Objects to Client Names
    client_objects = {} 

    def on_publish(self, client, userdata, mid) :
         self.logger.info("Server: Message Published")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        if (msg.topic == "sax_check"):
            self.logger.info("Server: Human Activity Simulation by CSV received...")
            # TODO: Move this simulation to client-side for concurrency control 
            self.is_exercise_simulation_active = True
            initialize_simulation_loop = threading.Thread(target=self.sax_decode_activity, args=[client, msg.payload])
            initialize_simulation_loop.start()
        elif(msg.topic == "disconnections"):
            self.logger.info("Server: Client With ID {} Disconnected - Stoping Simulation if active... {}".format(self.client_objects[client], self.is_exercise_simulation_active))
            self.is_exercise_simulation_active = False
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

        server.loop_forever()

    def sax_decode_activity(self, client, symbolic_base_64_string_encoded):
        sax_string = base64.decodestring(symbolic_base_64_string_encoded)
        sax_string_decoded = str(sax_string)[2:-1]
        startLetterIndex, endLetterIndex = 0, 20
        batch_size = endLetterIndex - startLetterIndex

        while(self.is_exercise_simulation_active):
            self.logger.info("Loading next batch of {} simulation images...".format(batch_size))
            self.image_encode_activity(client, sax_string_decoded, startLetterIndex, endLetterIndex)
            startLetterIndex += 20
            endLetterIndex += 20
            
        self.logger.info("Human Activity Simulation Playback complete for client with ID {}".format(self.client_objects[client]))
        # Reset clock
        client.publish("clock_reset", "notify")

    # Image sizes are 100 x 100
    # shift 256 is equivalent of shifting 1-second
    # TODO: Create Loading Pane for this
    def image_encode_activity(self, client, sax_string_decoded, startRange, endRange):
        initialRange = startRange
        try:
            shift_position = startRange
            bitmap_size = 100 * 100
            while(startRange < endRange):
                substring = sax_string_decoded[startRange:bitmap_size + shift_position]
                self.server_bitmap_generator.generate_single_bitmap(substring)   
                shift_position += 256
                startRange += 1
            self.logger.info("Simulation Images Resolved for range [{} - {}]".format(initialRange, endRange))

        finally:
            # Perform activity recognition
            tensorRange = endRange - initialRange
            self.real_time_simulate_activity_recognition(client, tensorRange)

    def real_time_simulate_activity_recognition(self, client, tensorRange):
        path = "./temp/"
        total_files = len(os.listdir(path))
        try:
            self.logger.info("Starting Model Prediction with Images in /Temp")
            self.model_predict(path, client, tensorRange)
        finally:
            # After Simulation Activity Recognition Function Complete => Destroy Temp Folder
            self.logger.warning("Destroying Temporaries...")
            self.destroy_temp_folder()

    def model_predict(self, dir_path, client, tensorRange):
        classifier = Classify_Image(test_dir=dir_path)
        classifier.initialize_prediction_process(tensorRange, client)

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
