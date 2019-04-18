import sys
import serial
import numpy
import time
import threading

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from drawnow import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D

import random

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

class Canvas():

    stop_real_time_graph = False
    is_arduino_connected = False

    def __init__(self, layout):

        self.figure = Figure(figsize=(4,4), dpi=90)
        self.figure.set_size_inches(1, 1, forward=True)
        self.canvas = FigureCanvas(self.figure)
        self.samples, self.microvolts = [], []

        self.ax1 = self.figure.add_subplot(111)
        self.ax1.set_ylabel('Microvolts(mV)')
        self.line = Line2D(self.samples, self.microvolts, color='blue', lw=1)
        self.ax1.add_line(self.line)
        self.ax1.set_ylim(1700, 1900)
        self.ax1.set_xlim(0, 25)

        layout.addWidget(self.canvas)

        self.graph_thread = threading.Thread(target=self.read_from_ppg)
        self.graph_thread.start()

    def plot(self):
        ''' plot Data '''
        self.line.set_data(self.samples, self.microvolts)
        self.ax1.relim()
        self.ax1.autoscale_view()

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def read_from_ppg(self):
        try:
            with serial.Serial('COM3', 19200, bytesize=serial.SEVENBITS, timeout=0) as ser, open("voltages.csv", 'w') as text_file:
                text_file.write("{}, {}\n".format("Samples", "Microvolts(mV)"))
                data_row_sample = 0
                self.is_arduino_connected = True
                print("Arduino Connection found on port {}".format(ser.port))
                while not self.stop_real_time_graph:
                    voltage_reading = str(ser.readline().decode(encoding='utf-8', errors='strict')).strip("\n").strip("\r\n")
                    if (voltage_reading != "" and voltage_reading.isdigit() and float(voltage_reading) > 1000):
                        data = [str(data_row_sample), voltage_reading]
                        text_file.write("{}, {}\n".format(data_row_sample, voltage_reading))
                        text_file.flush()
                        self.samples.append(float(data_row_sample))
                        self.microvolts.append(float(voltage_reading))
                        
                        self.plot()
                        plt.pause(0.05)
                        data_row_sample += 1

                        if(data_row_sample > 25):                            #If you have 25 or more points, delete the first one from the array
                            self.samples.pop(0)                       #This allows us to just see the last 50 data points
                            self.microvolts.pop(0)
                            self.ax1.set_xlim(min(self.samples), max(self.samples))

                        ser.flushInput()
                        ser.flushOutput()
        except:
            self.is_arduino_connected = False
            print("PPG Not Connected - Sleeping for 5 seconds and retrying...")
            time.sleep(5)
            self.read_from_ppg()