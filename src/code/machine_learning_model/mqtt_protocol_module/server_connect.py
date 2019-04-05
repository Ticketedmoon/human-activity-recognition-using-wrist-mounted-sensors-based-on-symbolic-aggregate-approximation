import socket
import paho.mqtt.client as mqtt
import time
import sys
import base64
import subprocess
import re
import os
import glob
import threading

sys.path.append("../")

from label_image import initialize_prediction_process
from bitmap_generator import BitmapGenerator

client_id = socket.gethostname()

class Server:

    server_bitmap_generator = BitmapGenerator()
    temporary_image_directory = "./temp"

    def on_connect(self, client, userdata, flags, rc):
        topic = "client_connections"
        msg = "Server connected to broker for serving HAR application"

        print("Publish to {} msg {}".format(topic, msg))
        client.publish(topic, msg, qos=2)

    def on_publish(self, client, userdata, mid) :
        print ("Message Published")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        if (msg.topic == "sax_check"):
            print("Server: Prediction Resolve Acknowledged")
            initialize_simulation_loop = threading.Thread(target=self.sax_decode_activity, args=[client, msg.payload])
            initialize_simulation_loop.start()
        else:
            message = str(msg.payload)
            print(message[2:-1])

    # on_connect
    def on_connect(self, client, userdata, flags, rc):
        if (rc == 0):
            print("Server: Broker Connected Successful")
        else:
            print("Bad connection - Returned Code=", rc)

    def on_disconnect(self, client, userdata, flags, rc=0):
        print("Disconnected result code: ", rc)

    def on_subscribe(self, client, userdata, flags, rc):
        # Do nothing
        pass

    def send(self):
        client = mqtt.Client("Server")
        client.on_connect = self.on_connect
        client.on_disconnect = self.on_disconnect
        client.on_message = self.on_message
        client.on_subscribe = self.on_subscribe

        host      = "127.0.0.1"
        port      = 1883
        keepalive = 60

        print ("\nServer: Connect to {}, keepalive {}".format(host, keepalive))
        client.connect(host=host, port=port, keepalive=keepalive)
        
        client.subscribe("client_connections")
        print("Server: Subscribing to topic {client_connections}")

        client.subscribe("sax_check")
        print("Server: Subscribing to topic {sax_check}")

        client.loop_forever()

    def sax_decode_activity(self, client, symbolic_base_64_string_encoded):
        sax_string = base64.decodestring(symbolic_base_64_string_encoded)
        sax_string_decoded = str(sax_string)[2:-1]
        self.image_encode_activity(client, sax_string_decoded)

    # Image sizes are 100 x 100
    # shift 256 is equivalent of shifting 1-second
    def image_encode_activity(self, client, sax_string_decoded):
        print("Server: Starting Image Encoding Process... Symbolic Length: {}".format(len(sax_string_decoded)))
        try:
            shift_position = 256
            bitmap_size = 100 * 100
            limit = len(sax_string_decoded) - bitmap_size
            while(shift_position < limit):
                enum_counter = (shift_position // 256) - 1
                substring = sax_string_decoded[shift_position-256:bitmap_size + shift_position]
                self.server_bitmap_generator.generate_single_bitmap(substring)   
                print("Image Built {} - Shift Value: {}".format(shift_position // 256, shift_position))
                self.real_time_simulate_activity_recognition(client, enum_counter)
                shift_position += 256
            print("Activity classification: Resolved.")

        finally:
            # After Simulation Activity Recognition Function Complete => Destroy Temp Folder
            print("Destroying Temporaries...")
            self.destroy_temp_folder()

    def real_time_simulate_activity_recognition(self, client, count):
        path = "./temp/"
        prediction = self.model_predict(path + "activity-{}.png".format(count))
        print("Prediction Posted: {}".format(prediction))

        encoded_prediction = base64.b64encode(bytes(prediction, 'utf-8'))
        client.publish("prediction_receive", encoded_prediction)

    def model_predict(self, client_image_path):
        p = subprocess.Popen(["python", "../label_image.py", "--graph=C:/tmp/output_graph.pb", "--labels=C:/tmp/output_labels.txt", "--input_layer=Placeholder",
                                    "--output_layer=final_result", "--image={}".format(client_image_path)], stdout=subprocess.PIPE)
        out, err = p.communicate()
        matches = re.findall("[wrlh]\w+ \d+\.\d+", str(out))
        return str(matches[0].split())

    # TODO: Use this function to dissect how to only load the graph one time - drastically speeding up the server side.
    # Additionally, perhaps all bitmap images for the specified csv should be generated first, and then
    # Time.sleep(X seconds) between each activity prediction - also take into account potential network latency.
    def run_graph(src, labels, input_layer_name, output_layer_name, num_top_predictions):
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
                    print('%s, %s' % (test[i], human_string))
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
