# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

from tkinter import filedialog
from tkinter import *

sys.path.append('../../machine_learning_module/')

from mqtt_protocol_module.client_connect import Client
from movie_player import Movie_Player

import threading
import bitmap_module
import base64
import time

class Application(Client, QObject):

    # Dynamic GUI variables
    exercise_time = 0
    activity_shift = 0

    # Animations
    movie_screen = None
    loading = None

    # Define a new signal called 'trigger' that has no arguments.
    # Slots and Signals
    trigger = pyqtSignal(str)

    # Current activity performed
    activity = "Idle"

    def __init__(self, primaryWindow):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)
        self.client.on_message = self.on_message
        self.centralwidget = QtWidgets.QWidget(primaryWindow)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.widget_2 = QtWidgets.QWidget(self.frame)
        self.label_pane_1 = QtWidgets.QLabel(self.widget_2)
        self.label_pane_2 = QtWidgets.QLabel(self.widget_2)
        self.label_pane_3 = QtWidgets.QLabel(self.widget_2)  
        app.aboutToQuit.connect(self.closeEvent)    

        # Put default movie here
        self.movie_screen = Movie_Player(self.frame)

        # Connect the trigger signal to a slot.
        self.trigger.connect(self.movie_screen.set_animation)
    
        self.download_thread = threading.Thread(target=self.send)
        self.download_thread.start()
    
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

    def closeEvent(self):
        #Your desired functionality here
        self.logger.warning('Application Closing...')
        self.client.publish("disconnections", str(self.client_id))
        self.prevent_publish_mechanism()
        self.disconnect()
        sys.exit(0)

    def setup_window_framework(self, PrimaryWindow):
        PrimaryWindow.setObjectName("PrimaryWindow")
        PrimaryWindow.setWindowTitle("Arduino Software - Human Activity Recognition via PPG sensor")
        PrimaryWindow.setWindowIcon(QtGui.QIcon("../assets/desktop-icon.png"))
        PrimaryWindow.resize(1000, 600)
        PrimaryWindow.setStyleSheet("background-color: rgb(235, 235, 235);")

    def setup_menu_bar(self, PrimaryWindow):
        # Menu Bar
        self.menuBar = PrimaryWindow.menuBar() 
        self.menuBar.setStyleSheet("background-color: rgb(255, 255, 255)")       
        file_menu = self.menuBar.addMenu('&File')
        file_menu = self.menuBar.addMenu('&Edit')
        file_menu = self.menuBar.addMenu('&Settings')
        file_menu = self.menuBar.addMenu('&Help')

    def setup_content_panes(self, PrimaryWindow):

        self.centralwidget = QtWidgets.QWidget(PrimaryWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.widget_2.setStyleSheet("background-color: rgb(0, 140, 180);")
        self.widget_2.setObjectName("widget_2")

        self.horizontalLayout.addWidget(self.widget_2)

        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.widget.setObjectName("widget")

    def display_activity_animation(self, activity):
        self.logger.info("Activity Detected {} - sending to animation player...".format(activity))
        
        # Emit the signal.
        self.trigger.emit(activity)

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

    # Research Pane
    def build_research_pane(self):
        self.widget_4 = QtWidgets.QWidget(self.frame_2)
        self.widget_4.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.widget_4.setObjectName("widget_4")

        self.verticalScrollBar = QtWidgets.QScrollBar(self.widget_4)
        self.verticalScrollBar.setGeometry(QtCore.QRect(425, 40, 20, 200))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")

        self.textEdit = QtWidgets.QTextEdit(self.widget_4)
        self.textEdit.setReadOnly(True)
        self.textEdit.setGeometry(QtCore.QRect(20, 40, 400, 200))
        self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        
        self.label = QtWidgets.QLabel(self.widget_4)
        self.label.setGeometry(QtCore.QRect(150, 10, 150, 20))
        self.label.setText("Research and Findings")

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)

        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("color: rgb(255, 255, 255)")
        self.label.setObjectName("label")

    def build_simulation_pane(self):
        self.horizontalLayout_2.addWidget(self.widget_4)

        self.widget_3 = QtWidgets.QWidget(self.frame_2)
        self.widget_3.setAutoFillBackground(False)
        self.widget_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_3.setObjectName("widget_3")

        self.progressBar = QtWidgets.QProgressBar(self.widget_3)
        self.progressBar.setGeometry(QtCore.QRect(30, 80, 231, 23))
        self.progressBar.setStyleSheet("background-color: rgb(0, 70, 150); color: white;")

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(8.5)

        self.progressBar.setFont(font)
        self.progressBar.setObjectName("progressBar")

        self.simulate_button = QtWidgets.QPushButton(self.widget_3)
        self.simulate_button.setGeometry(QtCore.QRect(30, 20, 180, 23))

        self.simulate_button.setFont(font)
        self.simulate_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.simulate_button.setAcceptDrops(False)
        self.simulate_button.setStyleSheet("background-color: rgb(0, 180, 30); color: white;")
        self.simulate_button.setIcon(QIcon(QPixmap("../assets/playback-2.png")))
        self.simulate_button.resize(180, 40)

        self.simulate_button.setObjectName("simulate_button")
        self.simulate_button.setText("Activity Recognition Playback")
        self.simulate_button.clicked.connect(self.submit_ppg_files)

        self.widget_5 = QtWidgets.QWidget(self.widget_3)
        self.widget_5.setGeometry(QtCore.QRect(45, 207, 171, 31))
        self.widget_5.setStyleSheet("color: black;")
        self.widget_5.setObjectName("widget_5")
        self.widget_5.setFont(font)

        self.ppg_connection = QtWidgets.QLabel(self.widget_5)
        self.ppg_connection.setGeometry(QtCore.QRect(15, 5, 161, 20))
        self.ppg_connection.setObjectName("ppg_connection")
        self.ppg_connection.setText("Arduino PPG Connected?")
        self.ppg_connection.setFont(font)

        # Red dot widget container
        self.widget_6 = QtWidgets.QWidget(self.widget_3)
        self.widget_6.setGeometry(QtCore.QRect(5, 205, 50, 31))
        self.widget_6.setAutoFillBackground(False)
        self.widget_6.setObjectName("widget_6")

        # red dot
        self.red_dot = QtWidgets.QLabel(self.widget_6)
        self.red_dot.setGeometry(QtCore.QRect(5, 8, 40, 40))
        
        red_cross = QtGui.QMovie("../assets/red-cross.gif")
        self.red_dot.setMovie(red_cross)
        red_cross.start()
        self.red_dot.setAlignment(Qt.AlignRight)

        self.red_dot.setLayout(QtWidgets.QHBoxLayout())
        self.horizontalLayout_2.addWidget(self.widget_3)

        # loading icon widget container
        self.widget_7 = QtWidgets.QWidget(self.widget_3)
        self.widget_7.setGeometry(QtCore.QRect(215, 0, 100, 65))
        self.widget_7.setAutoFillBackground(False)
        self.widget_7.setObjectName("widget_7")

        self.loader = QtWidgets.QLabel(self.widget_7)
        self.loader.setGeometry(QtCore.QRect(0, 0, 100, 75))
        self.loader.setAlignment(Qt.AlignCenter)

        self.loading = QtGui.QMovie("../assets/loader.gif")
        self.loader.setMovie(self.loading)
        self.loader.setLayout(QtWidgets.QHBoxLayout())

    def build_analytical_pane(self):
        # Trend graph animation for now
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.trend = QtWidgets.QLabel(self.widget)
        self.trend.setGeometry(QtCore.QRect(0, 0, 500, 250))
        self.trend.setAlignment(Qt.AlignCenter)
        self.trend.setStyleSheet("background-color: rgb(255, 255, 255);")
        movie = QtGui.QMovie("../assets/trend.gif")
        self.trend.setMovie(movie)
        movie.start()
        self.trend.setLayout(QtWidgets.QHBoxLayout())

    def launch(self, primaryWindow):
        self.setup_window_framework(primaryWindow)
        self.setup_menu_bar(primaryWindow)
        self.setup_content_panes(primaryWindow)
        self.draw_activity_text()

        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout.addWidget(self.frame)

        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.build_research_pane()
        self.build_simulation_pane()
        self.build_analytical_pane()

        # Display all
        self.verticalLayout.addWidget(self.frame_2)
        primaryWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(primaryWindow)

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
        self.progressBar.setValue((intprogress))
        self.progressBar.setFormat('{:.2f}%'.format(float(progress)))
        print(progress)

    def submit_ppg_files(self):
        try:
            root = Tk().withdraw()
            file_path = filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = (("timestamp & PPG recordings CSV","*.csv"), ("all files","*.*")))
            if (file_path != ""):
                self.logger.debug("Simulating Activity Recognition for file: {" + str(file_path) + "}")
                simulate_thread = threading.Thread(target=self.convert_and_send, args=[file_path])
                simulate_thread.start()

                if (self.loading is not None):
                    self.loading.start()
                    self.update_playback_button_state(False, "background-color: rgb(200, 200, 200); color: black;")
        except Exception as error:
            self.logger.error("Error: " + repr(error))    

    def update_playback_button_state(self, enabled=True, stylesheet="background-color: rgb(0, 180, 30); color: white"):
        self.simulate_button.setEnabled(enabled) 
        self.simulate_button.setStyleSheet(stylesheet)

    # Helper Function - Maybe move to new class (Helper)
    def replaceMultiple(self, mainString, toBeReplaces, newString):
        # Iterate over the strings to be replaced
        for elem in toBeReplaces:
            # Check if string is in the main string
            if elem in mainString:
                # Replace the string
                mainString = mainString.replace(elem, newString)
        
        return  mainString

if __name__ == "__main__":

    # Set up Window
    app = QtWidgets.QApplication(sys.argv)
    primaryWindow = QtWidgets.QMainWindow()
    application = Application(primaryWindow)
    application.launch(primaryWindow)    
    primaryWindow.show()

    # TODO: Ensure all threads have ended when program closes.
    sys.exit(app.exec_())