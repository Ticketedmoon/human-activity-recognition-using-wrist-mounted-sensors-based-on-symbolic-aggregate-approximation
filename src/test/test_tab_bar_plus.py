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

import base64
import time
import threading

class Test_Tab_Bar_Plus(unittest.TestCase):

    def test_instantiate_all_window_panes(self):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        application = Application(primaryWindow=test_window, logger_path="./code/")
        tab_bar_plus = TabBarPlus(QGridLayout(), QGridLayout(), QHBoxLayout(), QHBoxLayout(), application.logger)

        tab_bar_plus.activity_display_pane.layout_widgets = MagicMock()
        tab_bar_plus.activity_display_pane.connect_to_broker = MagicMock()
        tab_bar_plus.activity_display_pane.set_graph = MagicMock()

        tab_bar_plus.graph_pane.layout_widgets = MagicMock()
        tab_bar_plus.graph_pane.start_graph_listener = MagicMock()
        tab_bar_plus.activity_controller_pane.set_display = MagicMock()
        tab_bar_plus.activity_controller_pane.layout_widgets = MagicMock()
        tab_bar_plus.research_pane.build_overview_research_pane = MagicMock()

        tab_bar_plus.build_activity_display = MagicMock()
        tab_bar_plus.build_graph = MagicMock()
        tab_bar_plus.build_research_pane = MagicMock()

        tab_bar_plus.instantiate_all_window_panes(tab_bar_plus.logger)

        self.assertTrue(tab_bar_plus.activity_display_pane.layout_widgets.call_count == 1)
        self.assertTrue(tab_bar_plus.activity_display_pane.connect_to_broker.call_count == 1)
        self.assertTrue(tab_bar_plus.graph_pane.layout_widgets.call_count == 1)
        self.assertTrue(tab_bar_plus.activity_display_pane.set_graph.call_count == 1)
        self.assertTrue(tab_bar_plus.activity_controller_pane.set_display.call_count == 1)
        self.assertTrue(tab_bar_plus.activity_controller_pane.layout_widgets.call_count == 1)
        self.assertTrue(tab_bar_plus.research_pane.build_overview_research_pane.call_count == 1)

        self.assertTrue(tab_bar_plus.build_activity_display.call_count == 1)
        self.assertTrue(tab_bar_plus.build_graph.call_count == 1)
        self.assertTrue(tab_bar_plus.build_research_pane.call_count == 1)
        self.assertTrue(tab_bar_plus.graph_pane.start_graph_listener.call_count == 1)
