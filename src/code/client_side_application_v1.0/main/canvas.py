import sys
import serial
import numpy
import time

try:
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtCore import *
    from drawnow import *
except:
    pass

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D

import random

import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

class Canvas(QtWidgets.QWidget):

    max_x = 25

    def __init__(self, layout, logger):
        super(Canvas, self).__init__()
        self.logger = logger
        self.samples, self.microvolts = [], []
        self.figure = Figure(figsize=(4,4), dpi=90)
        self.figure.set_size_inches(1, 1, forward=True)
        self.ax1 = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self.figure)

    def reset_graph_axis(self, min_x=0, max_x=25, min_y=1600, max_y=1900):
        self.max_x = max_x
        self.ax1.clear()
        self.samples, self.microvolts = [], []
        self.line = Line2D(self.samples, self.microvolts, linestyle="-", color='teal', lw=1.85)
        self.ax1.add_line(self.line)
        self.ax1.set_ylim(min_y, max_y)
        self.ax1.set_xlim(min_x, max_x)
        self.plot()

    def plot(self):
        try:
            ''' plot Data '''
            self.line.set_data(self.samples, self.microvolts)
            self.ax1.relim()
            self.ax1.autoscale_view()

            self.figure.canvas.draw()
            self.figure.canvas.flush_events()
        except:
            pass