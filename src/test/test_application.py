from unittest.mock import MagicMock
from unittest import mock

import unittest 
import sys
import os
from mock import patch

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

sys.path.append('code/mqtt_protocol_module/')
sys.path.append('code/machine_learning_module/')
sys.path.append('code/desktop_gui_module/main/')

from application import Application
import time
import threading

class Test_Application(unittest.TestCase):

    @mock.patch("tab_bar_plus.TabBarPlus")
    def test_build_default_window_properties(self, mock):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        application = Application(primaryWindow=test_window, logger_path="./code/")

        application.build_frames = MagicMock()
        application.build_default_window_properties(test_window)

        self.assertTrue(application.build_frames.call_count == 1)

    def test_closeEvent(self):
        with patch('sys.exit') as exit_mock:
            app = QtWidgets.QApplication(sys.argv)
            test_window = QtWidgets.QMainWindow()
            application = Application(primaryWindow=test_window, logger_path="./code/", testMode=True)
            application.view = Test_Tab_Bar_View()
            application.view.shut_down = MagicMock()
            application.closeEvent()
            self.assertTrue(application.view.shut_down.call_count == 1)
            assert exit_mock.called

    def test_setup_window_framework(self):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        application = Application(primaryWindow=test_window, logger_path="./code/")

        test_window.setObjectName = MagicMock()
        test_window.setWindowTitle = MagicMock()
        test_window.setWindowIcon = MagicMock()
        test_window.resize = MagicMock()
        test_window.setstyleSheet = MagicMock()

        self.assertTrue(test_window.setObjectName.call_count == 0)
        self.assertTrue(test_window.setWindowTitle.call_count == 0)
        self.assertTrue(test_window.setWindowIcon.call_count == 0)
        self.assertTrue(test_window.resize.call_count == 0)
        self.assertTrue(test_window.setstyleSheet.call_count == 0)

        application.setup_window_framework(test_window)

        self.assertTrue(test_window.setObjectName.call_count == 1)
        self.assertTrue(test_window.setWindowTitle.call_count == 1)
        self.assertTrue(test_window.setWindowIcon.call_count == 1)
        self.assertTrue(test_window.resize.call_count == 1)

    def test_open_settings(self):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        application = Application(primaryWindow=test_window, logger_path="./code/")

        application.setWindowIcon = MagicMock()
        application.view = Test_Tab_Bar_View()
        application.view.graph_pane.update_port = MagicMock()
        QInputDialog.getItem = MagicMock(return_value=(3, True))

        application.open_settings()
        assert application.view.graph_pane.update_port.call_count == 1

        # No change in call of function
        application.view.graph_pane.port = 3
        assert application.view.graph_pane.update_port.call_count == 1

    def test_open_about(self):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        application = Application(primaryWindow=test_window, logger_path="./code/")

        application.setup_menu_bar(test_window)
        application.menu.setup_about_label = MagicMock()
        QDialog.exec_ = MagicMock()
        application.open_about()
        self.assertTrue(application.menu.setup_about_label.call_count == 1)
        self.assertTrue(QDialog.exec_.call_count == 1)

    def test_open_help_guide(self):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        application = Application(primaryWindow=test_window, logger_path="./code/")

        application.setup_menu_bar(test_window)
        application.menu.setup_help_label = MagicMock()
        QDialog.exec_ = MagicMock()
        application.open_help_guide()
        self.assertTrue(application.menu.setup_help_label.call_count == 1)
        self.assertTrue(QDialog.exec_.call_count == 1)


class Test_Tab_Bar_View:

    def __init__(self):
        self.graph_pane = Test_Graph_Pane()

    def shut_down(self):
        pass

class Test_Graph_Pane:

    port = 0

    def update_port(self):
        pass

class Test_QInputDialog:
    def getItem(self, title, port, items, amount, bool):
        return (port, bool)