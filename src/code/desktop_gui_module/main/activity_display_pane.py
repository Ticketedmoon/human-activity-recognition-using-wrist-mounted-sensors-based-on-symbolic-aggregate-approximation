import sys
import threading

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

from mqtt_protocol_module.client_connect import Client
from tkinter import filedialog
from tkinter import *
from movie_player import Movie_Player
import base64

class Activity_Display_Pane(Client, QObject):

    # Dynamic GUI variables
    activity_shift = 0
    exercise_time = 0

    # Current activity performed
    activity = "Idle"

    # Animations
    movie_screen = None

    # Define a new signal called 'trigger' that has no arguments.
    # Trigger can only signal via strings
    # Slots and Signals
    trigger = pyqtSignal(str)

    def __init__(self, frame, layout, logger):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)

        self.logger = logger
    
        # Join Client topic
        self.client.on_message = self.on_message

        # Widget Adds
        self.widget_2 = QtWidgets.QWidget(frame)
        self.widget_2.setStyleSheet("background-color: rgb(0, 140, 180);")
        self.widget_2.setObjectName("widget_2")

        layout.addWidget(self.widget_2)

        # Accuracy, Exercise Time, Activity Class
        self.label_pane_1 = QtWidgets.QLabel(self.widget_2)
        self.label_pane_2 = QtWidgets.QLabel(self.widget_2)
        self.label_pane_3 = QtWidgets.QLabel(self.widget_2)  

        # Put default movie here
        self.movie_screen = Movie_Player(frame)

        # Connect the trigger signal to a slot.
        self.trigger.connect(self.movie_screen.set_animation)

        # TODO: Fix Later - These need to be stopped somehow
        self.download_thread = threading.Thread(target=self.send)
        # self.download_thread.start()

        self.draw_activity_text()

    def stop_display(self):
        self.client.publish("disconnections", str(self.client_id))
        self.prevent_publish_mechanism()
        self.disconnect()
        sys.exit(0)

    def display_activity_animation(self, activity):
        self.logger.info("Activity Detected {} - sending to animation player...".format(activity))
        
        # Emit the signal.
        self.trigger.emit(activity)


    # The callback for when a PUBLISH message is received from the server.
    # Used by MQTT Client class
    def on_message(self, client, userdata, msg):
        if (msg.topic == "prediction_receive"):
            encoded_prediction = base64.decodestring(msg.payload)
            decoded_prediction = encoded_prediction.decode("utf-8", "ignore")
            prediction = (self.replaceMultiple(decoded_prediction, ['[', ']', ',', '\''] , "")).split()
            self.exercise_time += 1
            self.activity_shift += 256

            # When message received, update UI
            self.logger.info("Client with ID {} received message: {}".format(self.client_id, decoded_prediction))
            
            # Update UI Here
            self.update_activity_user_interface(prediction)

        elif(msg.topic == "clock_reset"):
            self.logger.info("Received Clock Reset Notification...")
            self.exercise_time = 0
            self.label_pane_2.setText("Exercise Time: {}s".format(self.exercise_time))
            self.update_activity_user_interface(("idle", 0))
            self.update_playback_button_state()

    # Helper Function - Maybe move to new class (Helper)
    def replaceMultiple(self, mainString, toBeReplaces, newString):
        # Iterate over the strings to be replaced
        for elem in toBeReplaces:
            # Check if string is in the main string
            if elem in mainString:
                # Replace the string
                mainString = mainString.replace(elem, newString)
        return  mainString

    # @Function - Used for Simulating Activity Recognition implementation.
    # Update UI to adjust for results - Avatar + predictive data. 
    def update_activity_user_interface(self, prediction_message):
        if (prediction_message[0] == "walk"):
            activity_prediction = prediction_message[0]            
        elif (prediction_message[0] == "run"):
            activity_prediction = prediction_message[0]
        elif (prediction_message[0] == "lowresistancebike"):
            activity_prediction = "Slow Cycle"
        elif (prediction_message[0] == "highresistancebike"):
            activity_prediction = "Fast Cycle"
        else:
            activity_prediction = "idle"

        self.display_activity_animation(prediction_message[0])
        prediction_accuracy = (round(float(prediction_message[1]), 4)) * 100
        self.label_pane_1.setText("Activity: {}".format(activity_prediction))
        self.label_pane_2.setText("Exercise Time: {}s".format(self.exercise_time))
        self.label_pane_3.setText("Accuracy: {:.2f}%".format(prediction_accuracy))

        progress = self.activity_shift / self.document_length_for_playback
        self.progressBar.setValue(int(progress))
        self.progressBar.setFormat('{:.2f}%'.format(float(progress)))
        self.logger.info(progress)

    def draw_activity_text(self):
        self.label_pane_1.setGeometry(QtCore.QRect(15, 10, 125, 15))
        self.label_pane_2.setGeometry(QtCore.QRect(15, 35, 125, 15))
        self.label_pane_3.setGeometry(QtCore.QRect(15, 60, 125, 15))

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(30)

        self.label_pane_1.setFont(font)
        self.label_pane_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_pane_1.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_pane_1.setObjectName("label")
        self.label_pane_1.setText("Activity: {}".format(self.activity))

        self.label_pane_2.setFont(font)
        self.label_pane_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_pane_2.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_pane_2.setObjectName("label")
        self.label_pane_2.setText("Exercise Time: {}".format(self.exercise_time))

        self.label_pane_3.setFont(font)
        self.label_pane_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_pane_3.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_pane_3.setObjectName("label")
        self.label_pane_3.setText("Accuracy: {}%".format("???"))