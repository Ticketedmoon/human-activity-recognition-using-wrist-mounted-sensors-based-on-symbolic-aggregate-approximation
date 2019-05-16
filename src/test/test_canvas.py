from unittest.mock import MagicMock
import unittest 

import sys
import serial
import numpy
import time

try:
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtCore import *
except:
    pass

sys.path.append('code/mqtt_protocol_module/')
sys.path.append('code/machine_learning_module/')
sys.path.append('code/desktop_gui_module/main/')

sys.path.append('code/')
from logger_module.Logger import Logger
from mqtt_protocol_module import client_controller
from canvas import Canvas
from application import Application

import base64
import time
import threading

# NOTE: Canvas is a small object, not a lot to test.
class Test_Canvas(unittest.TestCase):

    def test_reset_graph_axis(self):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        application = Application(primaryWindow=test_window, logger_path="./code/")

        test_layout = QGridLayout()
        test_logger = Logger("code/", "test", testMode=True)
        canvas = Canvas(test_layout, test_logger)

        # Fill up samples / microvolts array
        canvas.samples = [1, 2, 3, 4, 5]
        canvas.microvolts = [1700, 1800, 1900, 2000, 2100]

        # Mocks
        canvas.plot = MagicMock()
        
        # Call
        canvas.reset_graph_axis()

        self.assertTrue(canvas.plot.call_count == 1)
        self.assertTrue(len(canvas.samples) == len(canvas.microvolts))
        self.assertTrue(len(canvas.samples) == 0)
        self.assertTrue(len(canvas.microvolts) == 0)