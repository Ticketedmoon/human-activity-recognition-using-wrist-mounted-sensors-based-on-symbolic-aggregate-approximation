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

from research_window import Research_Window
from logger_module.Logger import Logger

import base64
import time
import threading


# NOTE: Research_Window is a small object, not a lot to test.
class Test_Research_Window(unittest.TestCase):

    def test__init__(self):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        application = Application(primaryWindow=test_window, logger_path="./code/")

        test_logger = Logger("code/", "test", testMode=True)
        obj = Research_Window(test_logger)
        
        test_value_widget_4 = len(obj.widget_4.text())
        test_value_widget_5 = len(obj.widget_5.text())

        self.assertTrue(test_value_widget_4 > 800 and test_value_widget_4 < 900)
        self.assertTrue(test_value_widget_5 > 3250 and test_value_widget_5 < 3500)