# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets

from tkinter import filedialog
from tkinter import *

sys.path.append('../machine_learning_model/')
from mqtt_protocol_module.client_connect import Client

import threading
import bitmap_module
import base64

class Application(Client):

    # Dynamic GUI variable
    exercise_time = 0
    
    def __init__(self, primaryWindow):
        super().__init__()
        self.centralwidget = QtWidgets.QWidget(primaryWindow)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.widget_2 = QtWidgets.QWidget(self.frame)
        self.label_pane_1 = QtWidgets.QLabel(self.widget_2)
        self.label_pane_2 = QtWidgets.QLabel(self.widget_2)
        self.label_pane_3 = QtWidgets.QLabel(self.widget_2)
        app.aboutToQuit.connect(self.closeEvent)
    
        self.download_thread = threading.Thread(target=self.send)
        self.download_thread.start()
    
    # The callback for when a PUBLISH message is received from the server.
    # Used by MQTT Client class
    def on_message(self, client, userdata, msg):
        if (msg.topic == "prediction_receive"):
            print("prediction received")

            encoded_prediction = base64.decodestring(msg.payload)
            decoded_prediction = encoded_prediction.decode("utf-8", "ignore")
            prediction = (self.replaceMultiple(decoded_prediction, ['[', ']', ',', '\''] , "")).split()
            self.exercise_time += 1

            print(prediction)
            # When message received, update UI
            print("Client with ID {} received message: {}".format(self.client_id, decoded_prediction))
            self.update_activity_user_interface(prediction)

    def closeEvent(self):
        #Your desired functionality here
        print('Closing Application...')
        self.prevent_publish_mechanism()
        self.disconnect()
        sys.exit(0)

    def setup_window_framework(self, PrimaryWindow):
        PrimaryWindow.setObjectName("PrimaryWindow")
        PrimaryWindow.setWindowTitle("Arduino Software - Human Activity Recognition via PPG sensor")
        PrimaryWindow.setWindowIcon(QtGui.QIcon("assets/desktop-icon.png"))
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

        self.widget_2.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.widget_2.setObjectName("widget_2")

        self.horizontalLayout.addWidget(self.widget_2)

        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.widget.setObjectName("widget")

    def check_activity_animation(self):
        # Activity Animation 
        self.widget_2.setStyleSheet("background-color: rgb(0, 140, 180);")

        self.status_txt = QtWidgets.QLabel(self.frame)
        self.status_txt.setGeometry(QtCore.QRect(135, 50, 225, 200))
        self.status_txt.setAlignment(Qt.AlignCenter)
        self.status_txt.setStyleSheet("background-color: rgb(0, 140, 180);")
        movie = QtGui.QMovie("assets/cycle.gif")
        self.status_txt.setMovie(movie)
        movie.start()
        self.status_txt.setLayout(QtWidgets.QHBoxLayout())

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
        self.label_pane_1.setText("Activity: Slow Cycle")

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
        self.widget_3.setStyleSheet("background-color: rgb(0, 140, 180);")
        self.widget_3.setObjectName("widget_3")

        self.progressBar = QtWidgets.QProgressBar(self.widget_3)
        self.progressBar.setGeometry(QtCore.QRect(30, 70, 231, 23))

        font = QtGui.QFont()
        font.setFamily("Calibri")

        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.simulate_button = QtWidgets.QPushButton(self.widget_3)
        self.simulate_button.setGeometry(QtCore.QRect(30, 20, 151, 23))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)

        self.simulate_button.setFont(font)
        self.simulate_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.simulate_button.setAcceptDrops(False)
        self.simulate_button.setStyleSheet("background-color: rgb(0, 190, 0); color: white;")
        
        self.simulate_button.setObjectName("simulate_button")
        self.simulate_button.setToolTip("<html><head/><body><p>Select PPG data file via csv</p></body></html>")
        self.simulate_button.setText("Simulate Activity Recognition")
        self.simulate_button.clicked.connect(self.submit_ppg_files)

        self.widget_5 = QtWidgets.QWidget(self.widget_3)
        self.widget_5.setGeometry(QtCore.QRect(30, 160, 171, 31))
        self.widget_5.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.widget_5.setObjectName("widget_5")

        self.radioButton = QtWidgets.QRadioButton(self.widget_5)
        self.radioButton.setGeometry(QtCore.QRect(10, 5, 161, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setText("Is Arduino PPG Connected?")
        
        self.horizontalLayout_2.addWidget(self.widget_3)

    def build_analytical_pane(self):
        # Trend graph animation for now
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.trend = QtWidgets.QLabel(self.widget)
        self.trend.setGeometry(QtCore.QRect(0, 0, 500, 250))
        self.trend.setAlignment(Qt.AlignCenter)
        self.trend.setStyleSheet("background-color: rgb(255, 255, 255);")
        movie = QtGui.QMovie("assets/trend.gif")
        self.trend.setMovie(movie)
        movie.start()
        self.trend.setLayout(QtWidgets.QHBoxLayout())

    def launch(self, primaryWindow):
        self.setup_window_framework(primaryWindow)
        self.setup_menu_bar(primaryWindow)
        self.check_activity_animation()
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

    def update_activity_user_interface(self, prediction_message):
        if (prediction_message[0] == "lowresistancebike"):
            activity_prediction = "Slow Cycle"
        elif (prediction_message[0] == "highresistancebike"):
            activity_prediction = "Fast Cycle"
        else:
            activity_prediction = prediction_message[0]

        prediction_accuracy = (round(float(prediction_message[1]), 4)) * 100
        self.label_pane_1.setText("Activity: {}".format(activity_prediction))
        self.label_pane_2.setText("Exercise Time: {}s".format(self.exercise_time))
        self.label_pane_3.setText("Accuracy: {:.2f}%".format(prediction_accuracy))
        print("Client User Interface Updated")

    def submit_ppg_files(self):
        try:
            root = Tk().withdraw()
            file_path = filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = (("timestamp & PPG recordings CSV","*.csv"), ("all files","*.*")))
            if (file_path != ""):
                print("Simulating Activity Recognition for file: {" + str(file_path) + "}")
                
                # Start thread here - does not freeze up the main thread
                simulate_thread = threading.Thread(target=self.convert_and_send, args=[file_path])
                simulate_thread.start()

        except Exception as error:
            print("Error: " + repr(error))

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