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

try:
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
except:
    pass

from movie_player import Movie_Player

import base64
import time
import threading

# NOTE: Movie_Player is a small object, not a lot to test.
class Test_Movie_Player(unittest.TestCase):

    def test_set_animation(self):
        app = QtWidgets.QApplication(sys.argv)
        test_window = QtWidgets.QMainWindow()
        application = Application(primaryWindow=test_window, logger_path="./code/")

        test_player = Movie_Player()
        self.assertTrue(test_player.currentActivity == "idle")

        # Mocks
        test_player.movie.stop = MagicMock()
        test_player.movie.start = MagicMock()

        # Testing
        test_player.set_animation("idle")
        # Nothing happens since activity is the same
        self.assertTrue(test_player.movie.speed() == 75)
        self.assertTrue(test_player.currentActivity == "idle")

        test_player.set_animation("walk")
        self.assertTrue(test_player.movie.speed() == 75)
        self.assertTrue(test_player.movie.stop.call_count == 1)
        self.assertTrue(test_player.movie.start.call_count == 1)
        self.assertTrue(test_player.currentActivity == "walk")

        test_player.set_animation("run")
        self.assertTrue(test_player.movie.speed() == 75)
        self.assertTrue(test_player.movie.stop.call_count == 2)
        self.assertTrue(test_player.movie.start.call_count == 2)
        self.assertTrue(test_player.currentActivity == "run")
        
        test_player.set_animation("lowresistancebike")
        self.assertTrue(test_player.movie.speed() == 75)
        self.assertTrue(test_player.movie.stop.call_count == 3)
        self.assertTrue(test_player.movie.start.call_count == 3)
        self.assertTrue(test_player.currentActivity == "lowresistancebike")
        
        test_player.set_animation("highresistancebike")
        self.assertTrue(test_player.movie.speed() == 125)
        self.assertTrue(test_player.movie.stop.call_count == 4)
        self.assertTrue(test_player.movie.start.call_count == 4)
        self.assertTrue(test_player.currentActivity == "highresistancebike")
        