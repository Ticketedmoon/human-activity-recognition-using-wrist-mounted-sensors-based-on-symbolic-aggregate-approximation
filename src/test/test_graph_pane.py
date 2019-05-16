from unittest.mock import MagicMock
import unittest 
import sys
import os
from mock import patch
import numpy as np

sys.path.append('code/mqtt_protocol_module/')
sys.path.append('code/machine_learning_module/')
sys.path.append('code/desktop_gui_module/main/')

from tab_bar_plus import TabBarPlus
from application import Application

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTabBar
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from graph_pane import Graph_Pane
from canvas import Canvas
from logger_module.Logger import Logger

import base64
import time
import threading

class Test_Graph_Pane(unittest.TestCase):

    def test__init__(self):
        test_app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        test_application = Application(primaryWindow=test_window, logger_path="./code/")

        test_layout = QGridLayout()
        test_logger = Logger("code/", "test", testMode=True)
        test_graph = Graph_Pane(test_layout, test_logger)
        self.assertTrue(test_graph.port == "COM3")

    def test_reset_data_on_graph(self):
        # Test set up
        test_app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        test_application = Application(primaryWindow=test_window, logger_path="./code/")

        test_layout_a = QGridLayout()
        test_layout_b = QGridLayout()
        test_logger = Logger("code/", "test", testMode=True)
        test_graph = Graph_Pane(test_layout_a, test_logger)

        # Test A
        test_graph.microvolts = [1000, 2000, 3000, 1004, 1400]
        test_graph.data_row_sample = 750
        test_graph.reset_data_on_graph()

        self.assertTrue(test_graph.data_row_sample == 0)
        self.assertTrue(len(test_graph.microvolts) == 0)

        # Test B
        test_graph.layout_widgets(test_layout_a)
        test_graph.layout_widgets(test_layout_b)

        # Mock
        test_graph.canvas_frames[0].reset_graph_axis = MagicMock()
        test_graph.canvas_frames[1].reset_graph_axis = MagicMock()

        # Test Execution
        test_graph.reset_data_on_graph()
        self.assertTrue(test_graph.canvas_frames[0].reset_graph_axis.call_count == 1)
        self.assertTrue(test_graph.canvas_frames[1].reset_graph_axis.call_count == 1)

    def test_layout_widgets(self):
        # Test set up
        test_app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        test_application = Application(primaryWindow=test_window, logger_path="./code/")

        test_layout_a = QGridLayout(None)
        test_layout_b = QGridLayout(None)
        test_logger = Logger("code/", "test", testMode=True)
        test_graph = Graph_Pane(test_layout_a, test_logger)

        test_graph.layout_widgets(test_layout_a)
        test_graph.layout_widgets(test_layout_b)

        self.assertTrue(len(test_graph.canvas_frames) == 2)

    def test_get_microvolt_reading(self):
         # Test set up
        test_app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        test_application = Application(primaryWindow=test_window, logger_path="./code/")

        test_layout_a = QGridLayout()
        test_logger = Logger("code/", "test", testMode=True)
        test_graph = Graph_Pane(test_layout_a, test_logger)

        test_graph.graph_frame = Canvas(test_layout_a, test_logger)

        test_graph.graph_frame.microvolts = [1000, 1500, 2000]
        test_result = test_graph.get_microvolt_reading()
        self.assertTrue(test_result == 1000)
        
        test_graph.graph_frame.microvolts = []
        test_result = test_graph.get_microvolt_reading()
        self.assertTrue(test_result == 0)

    def test_stop_graph_temporarily(self):
        # Test set up
        test_app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        test_application = Application(primaryWindow=test_window, logger_path="./code/")

        test_layout_a = QGridLayout()
        test_logger = Logger("code/", "test", testMode=True)
        test_graph = Graph_Pane(test_layout_a, test_logger)

        test_graph.graph_thread = MagicMock()
        test_graph.graph_thread.is_alive = MagicMock(return_value=True)
        test_graph.canvas_frames[0].reset_graph_axis = MagicMock()
        test_graph.canvas_frames[1].reset_graph_axis = MagicMock()

        test_thread = threading.Thread(target=test_graph.stop_graph_temporarily)
        test_thread.start()

        # Wait 3 seconds
        time.sleep(3)
        self.assertTrue(test_graph.canvas_frames[0].reset_graph_axis.call_count == 0)
        self.assertTrue(test_graph.canvas_frames[1].reset_graph_axis.call_count == 0)
        test_graph.graph_thread.is_alive = MagicMock(return_value=False)
        
        time.sleep(1)
        self.assertTrue(test_graph.canvas_frames[0].reset_graph_axis.call_count == 1)
        self.assertTrue(test_graph.canvas_frames[1].reset_graph_axis.call_count == 1)


    def test_start_playback_graph(self):
        # Test set up
        test_app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        test_application = Application(primaryWindow=test_window, logger_path="./code/")

        test_layout_a = QGridLayout()
        test_logger = Logger("code/", "test", testMode=True)
        test_graph = Graph_Pane(test_layout_a, test_logger)
        test_graph.canvas_frames[0].reset_graph_axis = MagicMock()
        test_graph.canvas_frames[1].reset_graph_axis = MagicMock()
        test_graph.update_graph = MagicMock()
        test_graph.reset_data_on_graph = MagicMock()
        test_graph.microvolts = [1700, 1800, 1900, 1500, 1600]

        # Test Execution (Thread)

        test_thread = threading.Thread(target=test_graph.start_playback_graph)
        test_thread.start()
        time.sleep(3)

        # Assert Reset graph twice
        self.assertTrue(test_graph.canvas_frames[0].reset_graph_axis.call_count == 1)
        self.assertTrue(test_graph.canvas_frames[1].reset_graph_axis.call_count == 1)

        # Check waiting condition
        self.assertTrue(test_graph.update_graph.call_count == 0)

        # Change lock state
        test_graph.update_graph_event.set()

        time.sleep(1)

        # Change Loop state
        test_graph.playback_graph_active = False
        test_graph.update_graph_event.set()

        time.sleep(3)

        self.assertTrue(test_graph.update_graph.call_count > 0)
        self.assertTrue(test_graph.data_row_sample > 64)
        self.assertTrue(test_graph.reset_data_on_graph.call_count == 1)
        


    def test_update_graph(self):
        # Test set up
        test_app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        test_application = Application(primaryWindow=test_window, logger_path="./code/")

        test_layout_a = QGridLayout()
        test_layout_b = QGridLayout()
        test_logger = Logger("code/", "test", testMode=True)
        test_graph = Graph_Pane(test_layout_a, test_logger)
        test_graph.reset_data_on_graph = MagicMock()
        test_graph.canvas_frames[0].plot = MagicMock()
        test_graph.canvas_frames[1].plot = MagicMock()
        test_graph.canvas_frames[0].ax1.set_xlim = MagicMock()
        test_graph.canvas_frames[1].ax1.set_xlim = MagicMock()

        test_graph.graph_frame = Canvas(test_layout_a, test_logger) # Widget is added from Canvas
        test_graph.canvas_frames.append(test_graph.graph_frame)

        test_graph.graph_frame = Canvas(test_layout_b, test_logger) # Widget is added from Canvas
        test_graph.canvas_frames.append(test_graph.graph_frame)

        test_sample_x = 25
        test_sample_y = 1700

        self.assertTrue(len(test_graph.canvas_frames[0].samples) ==0)
        self.assertTrue(len(test_graph.canvas_frames[0].microvolts) == 0)
        self.assertTrue(len(test_graph.canvas_frames[1].samples) == 0)
        self.assertTrue(len(test_graph.canvas_frames[1].microvolts) == 0)

        test_graph.update_graph(test_sample_x, test_sample_y)

        self.assertTrue(len(test_graph.canvas_frames[0].samples) == 1)
        self.assertTrue(len(test_graph.canvas_frames[0].microvolts) == 1)
        self.assertTrue(len(test_graph.canvas_frames[1].samples) == 1)
        self.assertTrue(len(test_graph.canvas_frames[1].microvolts) == 1)

        self.assertTrue(test_graph.canvas_frames[0].plot.call_count == 1)
        self.assertTrue(test_graph.canvas_frames[1].plot.call_count == 1)

    # TODO
    def test_read_from_ppg(self):
        pass