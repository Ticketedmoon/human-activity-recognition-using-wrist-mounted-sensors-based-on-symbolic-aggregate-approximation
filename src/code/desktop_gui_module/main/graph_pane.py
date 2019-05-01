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

    canvas_frames = []

    stop_real_time_graph = False
    is_arduino_connected = False

    def __init__(self, layout, logger):
        super(Graph_Pane, self).__init__()
        QtWidgets.QWidget.__init__(self)
        self.logger = logger

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
        if len(self.graph.microvolts) > 0:
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

    def read_from_ppg(self):
        try:
            with serial.Serial('COM3', 19200, bytesize=serial.SEVENBITS, timeout=0) as ser, open("voltages.csv", 'w') as text_file:
                text_file.write("{}, {}\n".format("Samples", "Microvolts(mV)"))
                data_row_sample = 0
                self.is_arduino_connected = True
                self.logger.info("Arduino Connection found on port {}".format(ser.port))

                for canvas in self.canvas_frames:
                    canvas.reset_graph_axis()

                while not self.stop_real_time_graph:
                    voltage_reading = str(ser.readline().decode(encoding='utf-8', errors='strict')).strip("\n").strip("\r\n")
                    if (voltage_reading != "" and voltage_reading.isdigit() and float(voltage_reading) > 1000):
                        data = [str(data_row_sample), voltage_reading]
                        text_file.write("{}, {}\n".format(data_row_sample, voltage_reading))
                        text_file.flush()

                        for canvas in self.canvas_frames:
                            canvas.samples.append(float(data_row_sample))
                            canvas.microvolts.append(float(voltage_reading))
                        
                        for canvas in self.canvas_frames:
                            canvas.plot()

                        plt.pause(0.01)
                        data_row_sample += 1

                        if(data_row_sample > 25):                            
                            #If you have 25 or more points, delete the first one from the array
                            #This allows us to just see the last 50 data points
                            for canvas in self.canvas_frames:
                                canvas.samples.pop(0)                       
                                canvas.microvolts.pop(0)
                                canvas.ax1.set_xlim(min(canvas.samples), max(canvas.samples))

                        ser.flushInput()
                        ser.flushOutput()
        except:
            if (not self.stop_real_time_graph):
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