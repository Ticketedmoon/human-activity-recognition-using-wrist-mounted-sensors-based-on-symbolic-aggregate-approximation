import threading
import sys
import serial
import numpy
import time

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

try:
    from PyQt5.Qt import *
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
    from PyQt5.QtGui import *
except:
    pass

from mock_graph_qt import TestWindow    
from canvas import Canvas

class Graph_Pane(QtWidgets.QWidget):

    # Event for concurrency control - wait/set
    update_graph_event = threading.Event()

    canvas_frames = []

    # boolean flags
    stop_real_time_graph = False
    reset_port = False
    is_arduino_connected = False
    playback_graph_active = False
    data_row_sample = 0
    microvolts = []

    def __init__(self, layout, logger):
        super(Graph_Pane, self).__init__()
        QtWidgets.QWidget.__init__(self)
        self.logger = logger

        # Default Port
        self.port = "COM3"

    @pyqtSlot()
    def reset_data_on_graph(self):
        self.playback_graph_active = False
        self.data_row_sample = 0
        self.microvolts = []
        try:
            for canvas in self.canvas_frames:
                # Prevent drawing
                canvas.reset_graph_axis()
        except:
            # Case where the graph is reset with no data points found.
            pass

    def layout_widgets(self, layout):   
        self.graph_frame = Canvas(layout, self.logger) # Widget is added from Canvas
        self.canvas_frames.append(self.graph_frame)  
        layout.addWidget(self.graph_frame.canvas)

    # Trend graph animation Placeholder.
    def build_placeholder(self):
        if self.trend != None:
            movie = QtGui.QMovie("../assets/trend.gif")
            self.trend.setMovie(movie)
            movie.start()
            self.trend.setLayout(QtWidgets.QHBoxLayout())

    # Getter
    def get_samples(self):
        return self.graph_frame.samples

    # Getter
    def get_microvolts(self):
        return self.graph_frame.microvolts

    def get_microvolt_reading(self):
        if len(self.graph_frame.microvolts) > 0:
            return self.graph_frame.microvolts[0]
        return 0

    def start_graph_listener(self):
        self.graph_thread = threading.Thread(target=self.read_from_ppg)
        self.graph_thread.start()

    def stop_graph(self):
        self.logger.warning("Stopping Real Time Graph...")
        self.stop_real_time_graph = True

    def check_arduino_connection(self):
        return self.is_arduino_connected

    def stop_graph_temporarily(self):
        self.reset_port = True
        while(self.graph_thread.is_alive()):
            time.sleep(1)
            
        # Clear Graph Data
        for canvas in self.canvas_frames:
            canvas.reset_graph_axis()

    def update_port(self, port):
        self.port = port
        self.stop_graph_temporarily()

        self.logger.warning("Arduino Port Thread Dead - Restarting...")
        # Start process again with new port
        self.start_graph_listener()

    # Conditions/Locks used here for synchronization.
    def start_playback_graph(self):
        self.playback_graph_active = True
        for canvas in self.canvas_frames:
            canvas.reset_graph_axis(min_x=0, max_x=1600, min_y=0, max_y=3000)

        try:
            while(self.playback_graph_active):
                self.update_graph_event.wait()
                for microvolt in self.microvolts[::-1]:
                    if (self.playback_graph_active):
                        self.data_row_sample += 64
                        self.update_graph(self.data_row_sample, microvolt)
                    else:
                        break
                self.update_graph_event.clear()
        finally:
            self.reset_data_on_graph()
            

    # Method called for each single update that a graph is required to make.
    # NOTE: plot.pause() method available if needed.
    def update_graph(self, sample_x, sample_y):
        for canvas in self.canvas_frames: 
            canvas.samples.append(sample_x)
            canvas.microvolts.append(sample_y)

        for canvas in self.canvas_frames:
            canvas.plot()

        if(self.data_row_sample > self.canvas_frames[0].max_x):
            #If you have 25 or more points, delete the first one from the array
            #This allows us to just see the last 50 data points
            for canvas in self.canvas_frames:
                canvas.samples.pop(0)                       
                canvas.microvolts.pop(0)
                canvas.ax1.set_xlim(min(canvas.samples), max(canvas.samples))

    # Method is extremely important.
    # Method tries to interact and scan for an active arduino connection based on a port value.
    # This port value can be modified in the settings of the application if needed.
    # It is important this method runs in a separate thread to the primary thread and
    # feeds back the results to the primary thread. 
    # This method uses the serial library to check for a arduino connection.
    def read_from_ppg(self, save_path="voltages.csv"):
        try:
            with serial.Serial(self.port, 19200, bytesize=serial.SEVENBITS, timeout=0) as ser, open(save_path, 'w') as text_file:
                text_file.write("{}, {}\n".format("Samples", "Microvolts(mV)"))
                self.is_arduino_connected = True
                self.reset_port = False
                self.logger.info("Arduino Connection found on port {}".format(ser.port))

                for canvas in self.canvas_frames:
                    canvas.reset_graph_axis()

                while not self.stop_real_time_graph and not self.reset_port:
                    voltage_reading = str(ser.readline().decode(encoding='utf-8', errors='strict')).strip("\n").strip("\r\n")
                    if (voltage_reading != "" and voltage_reading.isdigit() and float(voltage_reading) > 1000):
                        text_file.write("{}, {}\n".format(self.data_row_sample, voltage_reading))
                        text_file.flush()
                        self.data_row_sample += 1

                        sample_x = float(self.data_row_sample)
                        sample_y = float(voltage_reading)
                        self.update_graph(sample_x, sample_y)
                        
                        ser.flushInput()
                        ser.flushOutput()
        except:
            if (not self.stop_real_time_graph and not self.reset_port and not self.playback_graph_active):

                # Clear Graph Data
                for canvas in self.canvas_frames:
                    canvas.reset_graph_axis()

                # Ensure boolean flag is not set
                self.is_arduino_connected = False
                self.stop_real_time_graph = False
                self.data_row_sample = 0

                # log to file/console
                self.logger.info("Scanning for active Arduino Connection... {5 Second Delay}")

                # Sleep for X seconds checking for reconnection of Arduino
                time.sleep(5)

                # Try to read again
                self.read_from_ppg()