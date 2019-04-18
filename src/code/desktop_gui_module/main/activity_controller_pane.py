import sys
import threading
import serial
import time

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

from repeated_timer import Repeated_Timer
from tkinter import filedialog
from tkinter import *

sys.path.append('../../')

class Activity_Controller_Pane():

    loading = None

    def __init__(self, frame, layout, logger, display, graph_control):
        super().__init__()
        # Controller has access to display
        self.display = display

        # Controller has access to graph
        self.graph_control = graph_control

        # Logger Initialize
        self.logger = logger

        self.widget_3 = QtWidgets.QWidget(frame)
        self.widget_3.setAutoFillBackground(False)
        self.widget_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_3.setObjectName("widget_3")

        self.build(layout)

    # TODO: Refactor
    def build(self, layout):
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(8.5)

        self.progressBar = QtWidgets.QProgressBar(self.widget_3)
        self.progressBar.setGeometry(QtCore.QRect(30, 80, 212.5, 23))
        self.progressBar.setStyleSheet("background-color: rgb(0, 70, 150); color: white;")
        self.progressBar.setFont(font)
        self.progressBar.setObjectName("progressBar")

        # Playback/Simulate Button
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

        # Cancel Simulation in-progress button
        self.cancel_simulation_button = QtWidgets.QPushButton(self.widget_3)
        self.cancel_simulation_button.setGeometry(QtCore.QRect(30, 120, 180, 23))
        
        self.cancel_simulation_button.setFont(font)
        self.cancel_simulation_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.cancel_simulation_button.setAcceptDrops(False)
        self.cancel_simulation_button.setStyleSheet("background-color: rgb(220, 30, 30); color: white;")
        self.cancel_simulation_button.setIcon(QIcon(QPixmap("../assets/cancel_playback.png")))
        self.cancel_simulation_button.resize(180, 40)

        self.cancel_simulation_button.setObjectName("cancel_simulation_button")
        self.cancel_simulation_button.setText("Cancel Recognition Playback")
        self.cancel_simulation_button.clicked.connect(self.cancel_button_sequence_start)
        self.update_playback_button_state(self.cancel_simulation_button, False, "background-color: rgb(200, 200, 200); color: black;")

        # Real Time Mode Initialize button
        self.real_time_mode_button = QtWidgets.QPushButton(self.widget_3)
        self.real_time_mode_button.setGeometry(QtCore.QRect(260, 200, 180, 23))
        
        self.real_time_mode_button.setFont(font)
        self.real_time_mode_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.real_time_mode_button.setAcceptDrops(False)
        self.real_time_mode_button.setStyleSheet("background-color: rgb(0, 128, 128); color: white;")
        self.real_time_mode_button.setIcon(QIcon(QPixmap("../assets/real_time.png")))
        self.real_time_mode_button.resize(180, 40)

        self.real_time_mode_button.setObjectName("real_time_mode_button")
        self.real_time_mode_button.setText("Real Time Recognition Initialize")

        self.widget_5 = QtWidgets.QWidget(self.widget_3)
        self.widget_5.setGeometry(QtCore.QRect(45, 207, 171, 31))
        self.widget_5.setStyleSheet("color: black;")
        self.widget_5.setObjectName("widget_5")
        self.widget_5.setFont(font)

        self.ppg_connection = QtWidgets.QLabel(self.widget_5)
        self.ppg_connection.setGeometry(QtCore.QRect(15, 5, 161, 20))
        self.ppg_connection.setObjectName("ppg_connection")
        self.ppg_connection.setFont(font)

        self.create_ppg_connection_box_area(self.widget_3, layout)

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

    def create_ppg_connection_box_area(self, widget, layout):
         # Red dot widget container
        self.widget_6 = QtWidgets.QWidget(widget)
        self.widget_6.setGeometry(QtCore.QRect(5, 205, 50, 31))
        self.widget_6.setAutoFillBackground(False)
        self.widget_6.setObjectName("widget_6")

        # Connection Icon
        self.connection_icon = QtWidgets.QLabel(self.widget_6)
        self.connection_icon.setGeometry(QtCore.QRect(5, 8, 40, 40))

        # Call initially for instantaneous UI clarity
        self.is_arduino_connected()

        # Check every X seconds for Arduino connection/disconnection
        self.arduino_connection_timer = Repeated_Timer(5, self.is_arduino_connected) # it auto-starts, no need of arduino_connection_timer.start()

        self.connection_icon.setLayout(QtWidgets.QHBoxLayout())
        layout.addWidget(widget)

    def cancel_button_sequence_start(self):
        if (self.loading != None):
            self.loading.stop()
            self.loader.setMovie(None)

        self.loading = QtGui.QMovie("../assets/loader.gif")
        self.loader.setMovie(self.loading)
        
        self.display.stop_display()
        self.display.reset_display_parameters()
        self.display.connect_to_broker()

        self.update_playback_button_state(self.simulate_button, True, "background-color: rgb(0, 180, 30); color: white;")
        self.update_playback_button_state(self.cancel_simulation_button, False, "background-color: rgb(200, 200, 200); color: black;")

    def resolve(self):
        if (self.arduino_connection_timer.is_running):
            self.arduino_connection_timer.stop()

    def is_arduino_connected(self):
        if self.graph_control.check_arduino_connection():
            green_symbol = QtGui.QMovie("../assets/ppg_connected.gif")
            self.connection_icon.setMovie(green_symbol)
            self.connection_icon.setAlignment(Qt.AlignRight)
            self.ppg_connection.setText("Arduino PPG Connected")
            green_symbol.start()

        else: 
            red_cross = QtGui.QMovie("../assets/red-cross.gif")
            self.connection_icon.setMovie(red_cross)
            self.connection_icon.setAlignment(Qt.AlignRight)
            self.ppg_connection.setText("Arduino PPG Not Connected")
            red_cross.start()

    def submit_ppg_files(self):
        try:
            root = Tk().withdraw()
            file_path = filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = (("timestamp & PPG recordings CSV","*.csv"), ("all files","*.*")))
            if (file_path != ""):
                self.logger.debug("Simulating Activity Recognition for file: {" + str(file_path) + "}")
                self.display.send_activity_string_data_to_broker(file_path)               

                if (self.loading is not None):
                    self.loading.start()
                    self.update_playback_button_state(self.simulate_button, False,"background-color: rgb(200, 200, 200); color: black;")
                    self.update_playback_button_state(self.cancel_simulation_button, True, "background-color: rgb(220, 30, 30); color: white;")
        except Exception as error:
            self.logger.error("Error: " + repr(error))    

    def update_playback_button_state(self, button, enabled=True, stylesheet="background-color: rgb(0, 180, 30); color: white"):
        button.setEnabled(enabled) 
        button.setStyleSheet(stylesheet)