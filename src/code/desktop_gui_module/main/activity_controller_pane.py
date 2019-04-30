import sys
import threading
import serial
import time
import numpy as np

from functools import partial
from PyQt5.Qt import *
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

from repeated_timer import Repeated_Timer
from tkinter import filedialog
from tkinter import *

sys.path.append('../../')

class Activity_Controller_Pane(QtWidgets.QWidget):

    display = None
    real_time_recognition_alive = False
    image_size = 32 * 32

    loading_widgets = []
    playback_buttons = []
    stop_play_back_buttons = []
    real_time_playback_buttons = []
    ppg_connection_widgets = []
    ppg_connection_icons = []
    loaders = []

    def __init__(self, logger, graph_control):
        super(Activity_Controller_Pane, self).__init__()
        QtWidgets.QWidget.__init__(self)

        # Logger Initialize
        self.logger = logger

        # Controller has access to graph
        self.graph_control = graph_control

        # Warning Message box
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.setWindowIcon(QtGui.QIcon("../assets/desktop-icon.png"))

        self.msg.setText("Arduino PPG has not been connected - An active connection stream is required for real-time activity recognition")
        self.msg.setWindowTitle("Arduino PPG Connection Warning")
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Retry | QtWidgets.QMessageBox.Cancel)
        
    def layout_widgets(self, layout):

        self.widget_3 = QtWidgets.QWidget()
        self.widget_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_3.setObjectName("widget_controller")
        layout.addWidget(self.widget_3)

        self.build()

    def set_display(self, display):
        # Controller has access to display
        self.display = display

    # TODO: Refactor
    def build(self):
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
        self.playback_buttons.append(self.simulate_button)

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

        self.stop_play_back_buttons.append(self.cancel_simulation_button)
        self.update_playback_button_state(self.stop_play_back_buttons, False, "background-color: rgb(200, 200, 200); color: black;")

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
        self.real_time_mode_button.clicked.connect(partial(self.engage_real_time_activity_recognition))
        self.real_time_playback_buttons.append(self.real_time_mode_button)

        self.widget_5 = QtWidgets.QWidget(self.widget_3)
        self.widget_5.setGeometry(QtCore.QRect(45, 207, 171, 31))
        self.widget_5.setStyleSheet("color: black;")
        self.widget_5.setObjectName("widget_5")
        self.widget_5.setFont(font)

        self.ppg_connection = QtWidgets.QLabel(self.widget_5)
        self.ppg_connection.setGeometry(QtCore.QRect(15, 5, 161, 20))
        self.ppg_connection.setObjectName("ppg_connection")
        self.ppg_connection.setFont(font)
        self.ppg_connection_widgets.append(self.ppg_connection)

        self.create_ppg_connection_box_area(self.widget_3)

        # loading icon widget container
        self.widget_7 = QtWidgets.QWidget(self.widget_3)
        self.widget_7.setGeometry(QtCore.QRect(215, 0, 100, 65))
        self.widget_7.setAutoFillBackground(False)
        self.widget_7.setObjectName("widget_7")

        self.loading = QtGui.QMovie("../assets/loader.gif")
        self.loader = QtWidgets.QLabel(self.widget_7)
        self.loader.setGeometry(QtCore.QRect(0, 0, 100, 75))
        self.loader.setAlignment(Qt.AlignCenter)
        self.loader.setMovie(self.loading)
        self.loader.setLayout(QtWidgets.QHBoxLayout())
        self.loaders.append(self.loader)

        self.loading_widgets.append(self.loading)

    def create_ppg_connection_box_area(self, widget):
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
        self.ppg_connection_icons.append(self.connection_icon)

    def cancel_button_sequence_start(self):
        if (self.loading != None):
            for loading_widget in self.loading_widgets:
                loading_widget.stop()            
            for loader in self.loaders:
                loader.setMovie(None)

        for i in range(len(self.loaders)):
            loading_widget = QtGui.QMovie("../assets/loader.gif")
            self.loading_widgets[i] = loading_widget
            self.loaders[i].setMovie(loading_widget)

        self.display.stop_display()
        self.display.reset_display_parameters()
        self.display.connect_to_broker()

        self.update_playback_button_state(self.playback_buttons, True, "background-color: rgb(0, 180, 30); color: white;")
        self.update_playback_button_state(self.stop_play_back_buttons, False, "background-color: rgb(200, 200, 200); color: black;")

    def engage_real_time_activity_recognition(self, debug_mode_active=False):
        if self.graph_control.check_arduino_connection() or debug_mode_active:
            # If PPG is connected via Arduino port on COM3
            # Change button state colour to be 'active' as opposed to the blue inactive state
            # Disable all other buttons 
            # Start real-time activity recognition
            if not self.real_time_recognition_alive:
                self.real_time_recognition_alive = True
                self.update_playback_button_state(self.playback_buttons, False, "background-color: rgb(200, 200, 200); color: black;")
                self.update_playback_button_state(self.stop_play_back_buttons, False, "background-color: rgb(200, 200, 200); color: black;")
                self.update_playback_button_state(self.real_time_playback_buttons, True, "background-color: rgb(220, 30, 30); color: white;")

                self.real_time_recognition_thread = threading.Thread(target=self.read_from_ppg_with_double_buffer)
                self.real_time_recognition_thread.start()
            else:
                self.real_time_recognition_alive = False
        else:
            # Pop up dialog box that the Arduino PPG is not connected
            choice = self.msg.exec_()
            if choice == QtWidgets.QMessageBox.Retry:
                # Try to engage real time activity recognition again.
                self.engage_real_time_activity_recognition()

    def read_from_ppg_with_double_buffer(self):
        # Step #1: Read from active PPG device
        try:
            image_properties = []
            while(self.real_time_recognition_alive):
                if len(image_properties) == self.image_size:
                    data_read_from_ppg = np.array(image_properties)
                    image_properties.pop(0)
                    # Convert data to Pandas series object
                    self.display.convert_and_send_real_time(data_read_from_ppg)
                else:
                    image_properties.append(self.graph_control.get_microvolt_reading())                
                time.sleep(0.001)
        finally:
            # Stop Real Time Recognition
            self.real_time_recognition_alive = False
            # Update button states
            self.update_playback_button_state(self.playback_buttons, True, "background-color: rgb(0, 180, 30); color: white;")
            self.update_playback_button_state(self.stop_play_back_buttons, False, "background-color: rgb(200, 200, 200); color: black;")
            self.update_playback_button_state(self.real_time_playback_buttons, True, "background-color: rgb(0, 128, 128); color: white;")
            # log to file/console
            self.logger.warning("Real-Time Activity Recognition Function Active Finished...")
            

        # Step #2: Send each individual microvolt sample over in a stream, perhaps some arbitrary amount per second, IE 256 samples/s
        # - MQTT will require a unique topic for real-time recognition as the processing is different in texture.

        # Step #3: Store data in an unbounded buffer server-side (double buffering?)

        # step #4: Once buffer contains enough data to build an image (1024 - 3x32), build the image and then predict
        # After each image creation, remove previous image and remove 1 character from the buffer such that we shift along it. (Similar to the window sliding idea)

        # Step #5: Return prediction to client, client should automatically update if published to correct topic.
        # Note: Some of the parameters will need to be changed IE The exercise time
        pass

    def resolve(self):
        if (self.arduino_connection_timer.is_running):
            self.arduino_connection_timer.stop()
        self.real_time_recognition_alive = False

    def is_arduino_connected(self):
        if self.graph_control.check_arduino_connection():
            for connection_icon in self.ppg_connection_icons:
                green_symbol = QtGui.QMovie("../assets/ppg_connected.gif")
                connection_icon.setMovie(green_symbol)
                connection_icon.setAlignment(Qt.AlignRight)
                green_symbol.start()
            for connection_widget in self.ppg_connection_widgets:
                connection_widget.setText("Arduino PPG Connected")
        else: 
            for connection_icon in self.ppg_connection_icons:
                red_cross = QtGui.QMovie("../assets/red-cross.gif")
                connection_icon.setMovie(red_cross)
                connection_icon.setAlignment(Qt.AlignRight)
                red_cross.start()
            for connection_widget in self.ppg_connection_widgets:
                connection_widget.setText("Arduino PPG Not Connected")

    def submit_ppg_files(self):
        try:
            root = Tk().withdraw()
            file_path = filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = (("timestamp & PPG recordings CSV","*.csv"), ("all files","*.*")))
            if (file_path != ""):
                self.logger.debug("Simulating Activity Recognition for file: {" + str(file_path) + "}")
                self.display.send_activity_string_data_to_broker(file_path)               

                if (len(self.loaders) > 0):
                    for loading_widget in self.loading_widgets:
                        loading_widget.start()
                    self.update_playback_button_state(self.playback_buttons, False,"background-color: rgb(200, 200, 200); color: black;")
                    self.update_playback_button_state(self.stop_play_back_buttons, True, "background-color: rgb(220, 30, 30); color: white;")
        except Exception as error:
            self.logger.error("Error: " + repr(error))    

    def update_playback_button_state(self, buttons, enabled=True, stylesheet="background-color: rgb(0, 180, 30); color: white"):
        for button in buttons:
            button.setEnabled(enabled) 
            button.setStyleSheet(stylesheet)