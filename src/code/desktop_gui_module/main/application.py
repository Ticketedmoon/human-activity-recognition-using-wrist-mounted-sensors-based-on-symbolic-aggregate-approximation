import sys

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *
from test_graph_qt import FenetrePrincipale

from tkinter import filedialog
from tkinter import *

sys.path.append('../../')

from activity_controller_pane import Activity_Controller_Pane
from research_window import Research_Window
from graph_pane import Graph_Pane

from mqtt_protocol_module.client_connect import Client
from movie_player import Movie_Player
from canvas import Canvas

import threading
import bitmap_module
import base64
import time

class Application(Client, QObject):

    def __init__(self, primaryWindow):
        super().__init__()
        QtWidgets.QMainWindow.__init__(self)

        # Frame setup / widgets -> refactor
        self.centralwidget = QtWidgets.QWidget(primaryWindow)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        # Layouts
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        # Close Event
        app.aboutToQuit.connect(self.closeEvent)

    def closeEvent(self):
        #Your desired functionality here
        self.logger.warning('Application Closing...')
        self.client.publish("disconnections", str(self.client_id))
        self.prevent_publish_mechanism()
        self.disconnect()
        sys.exit(0)

    def setup_window_framework(self, PrimaryWindow):
        PrimaryWindow.setObjectName("PrimaryWindow")
        PrimaryWindow.setWindowTitle("Arduino Software - Human Activity Recognition via PPG sensor")
        PrimaryWindow.setWindowIcon(QtGui.QIcon("../assets/desktop-icon.png"))
        PrimaryWindow.resize(1000, 600)
        PrimaryWindow.setStyleSheet("background-color: rgb(235, 235, 235);")

    def setup_menu_bar(self, PrimaryWindow):
        # Menu Bar
        self.menuBar = PrimaryWindow.menuBar() 
        self.menuBar.setStyleSheet("background-color: rgb(255, 255, 255)")       
        file_menu = self.menuBar.addMenu('&File')
        file_menu = self.menuBar.addMenu('&Edit')
        file_menu = self.menuBar.addMenu('&Settings')
        file_menu = self.menuBar.addMenu('&Help')

    def setup_content_panes(self, PrimaryWindow):

        self.centralwidget = QtWidgets.QWidget(PrimaryWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

    def launch(self, primaryWindow):
        # TODO: Refactor these
        self.setup_window_framework(primaryWindow)
        self.setup_menu_bar(primaryWindow)
        self.setup_content_panes(primaryWindow)

        self.verticalLayout.addWidget(self.frame)
        
        # Refactored Code
        self.graph_pane = Graph_Pane(self.frame, self.horizontalLayout, self.logger)
        self.activity_controller_pane = Activity_Controller_Pane(self.frame, self.horizontalLayout, self.logger)
        self.research_pane = Research_Window(self.frame_2, self.horizontalLayout_2, self.logger)

        # Display all
        self.verticalLayout.addWidget(self.frame_2)
        primaryWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(primaryWindow)

if __name__ == "__main__":

    # Set up Window
    app = QtWidgets.QApplication(sys.argv)
    primaryWindow = QtWidgets.QMainWindow()
    application = Application(primaryWindow)
    application.launch(primaryWindow)    
    primaryWindow.show()

    # TODO: Ensure all threads have ended when program closes.
    sys.exit(app.exec_())