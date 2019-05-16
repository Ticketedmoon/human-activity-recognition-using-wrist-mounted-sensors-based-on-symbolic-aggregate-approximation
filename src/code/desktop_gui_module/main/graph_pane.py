import threading
import sys
import serial
import numpy
import time

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

from test_graph_qt import FenetrePrincipale
from canvas import Canvas

class Graph_Pane(QtWidgets.QWidget):

    update_graph_event = threading.Event()

    canvas_frames = []

    stop_real_time_graph = False
    reset_port = False
    is_arduino_connected = False
    playback_graph_active = False
    data_row_sample = 0
    microvolts = 0

    def __init__(self, layout, logger):
        super(Graph_Pane, self).__init__()
        QtWidgets.QWidget.__init__(self)
        self.logger = logger

        # Default Port
        self.port = "COM3"

    def reset_data_on_graph(self):
        self.playback_graph_active = False
        self.data_row_sample = 0
        for canvas in self.canvas_frames:
            # Prevent drawing
            canvas.is_plottable = False
            canvas.reset_graph_axis()

    # TODO: Fix
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

    def get_samples(self):
        return self.graph_frame.samples

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
            canvas.reset_graph_axis(750, 2250)

        try:
            while(self.playback_graph_active):
                self.update_graph_event.wait()
                for microvolt in self.microvolts:
                    self.data_row_sample += 1
                    self.update_graph(self.data_row_sample, microvolt)
                self.update_graph_event.clear()
        finally:
            for canvas in self.canvas_frames:
                canvas.reset_graph_axis()
                canvas.is_plottable = True
                self.data_row_sample = 0
            

    # plot.pause() method available if needed.
    def update_graph(self, sample_x, sample_y):
        for canvas in self.canvas_frames: 
            canvas.samples.append(sample_x)
            canvas.microvolts.append(sample_y)

        for canvas in self.canvas_frames:
            canvas.plot()

        if(self.data_row_sample > 25):                            
            #If you have 25 or more points, delete the first one from the array
            #This allows us to just see the last 50 data points
            for canvas in self.canvas_frames:
                canvas.samples.pop(0)                       
                canvas.microvolts.pop(0)
                canvas.ax1.set_xlim(min(canvas.samples), max(canvas.samples))

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
                # log to file/console
                self.logger.info("Scanning for active Arduino Connection... {5 Second Delay}")
                # Sleep for X seconds checking for reconnection of Arduino
                time.sleep(5)
                # Try to read again
                self.read_from_ppg()