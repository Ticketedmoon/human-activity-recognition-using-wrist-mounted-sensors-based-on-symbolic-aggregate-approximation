from unittest.mock import MagicMock
import unittest 

import sys
import serial
import numpy
import time

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

sys.path.append('code/mqtt_protocol_module/')
sys.path.append('code/machine_learning_module/')
sys.path.append('code/desktop_gui_module/main/')

sys.path.append('code/')
from application import Application
from menu_bar_builder import MenuBar

import base64
import time
import threading

class Test_Menu_Bar_Builder(unittest.TestCase):

    def test_build_basic_menu_items(self):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        test_application = Application(primaryWindow=test_window, logger_path="./code/")

        test_menu_bar = MenuBar(test_window, test_application)

        # Mocks
        test_menu_bar.menuBar.addMenu = MagicMock()

        test_menu_bar.build_basic_menu_items()
        self.assertTrue(test_menu_bar.menuBar.addMenu.call_count == 3)

    def test_attach_file_options(self):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        test_application = Application(primaryWindow=test_window, logger_path="./code/")

        test_menu_bar = MenuBar(test_window, test_application)

        # Mocks
        test_menu_bar.fileMenu.addAction = MagicMock()

        test_menu_bar.attach_file_options()
        self.assertTrue(test_menu_bar.fileMenu.addAction.call_count == 3)        


    def test_attach_settings_options(self):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        test_application = Application(primaryWindow=test_window, logger_path="./code/")

        test_menu_bar = MenuBar(test_window, test_application)

        # Mocks
        test_menu_bar.settingsMenu.addAction = MagicMock()

        test_menu_bar.attach_settings_options()
        self.assertTrue(test_menu_bar.settingsMenu.addAction.call_count == 1)

    def test_attach_help_options(self):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        test_application = Application(primaryWindow=test_window, logger_path="./code/")

        test_menu_bar = MenuBar(test_window, test_application)

        # Mocks
        test_menu_bar.helpMenu.addAction = MagicMock()

        test_menu_bar.attach_help_options()
        self.assertTrue(test_menu_bar.helpMenu.addAction.call_count == 1)