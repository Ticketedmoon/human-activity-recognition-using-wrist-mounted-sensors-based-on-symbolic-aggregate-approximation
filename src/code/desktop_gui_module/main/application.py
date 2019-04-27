import sys

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

from tkinter import filedialog
from tkinter import *

from tab_bar_plus import TabBarPlus
from activity_controller_pane import Activity_Controller_Pane
from activity_display_pane import Activity_Display_Pane
from research_window import Research_Window
from graph_pane import Graph_Pane

sys.path.append('../../')

from logger_module.Logger import Logger

class Application(QMainWindow):

    logger = Logger("../../", "logs/DesktopGUI")

    def __init__(self, primaryWindow):
        super(Application, self).__init__()

        # Build default window properties
        self.build_default_window_properties(primaryWindow)
        self.setup_window_framework(primaryWindow)
        self.build_frames(self.centralwidget)

        # Build Tab View
        self.view = TabBarPlus(self.layout_a, self.layout_b, self.layout_c, self.layout_d, self.logger)
        self.view.currentChanged.connect(self.onChange) #changed!
        primaryWindow.setCentralWidget(self.view) 

        # Set up menu bar
        self.setup_menu_bar(primaryWindow)
        
        # Close Event
        app.aboutToQuit.connect(self.closeEvent)

        # Connect slots, default for primary window
        QtCore.QMetaObject.connectSlotsByName(primaryWindow)

    def build_default_window_properties(self, primaryWindow):
        # Frame setup / widgets -> refactor
        self.centralwidget = QtWidgets.QWidget(primaryWindow)

        self.build_frames(self.centralwidget)

        # Layouts
        self.layout_a = QGridLayout(self.tab_frame_a)
        self.layout_a.setColumnStretch(1, 0)

        self.layout_b = QGridLayout(self.tab_frame_b)
        self.layout_b.setColumnStretch(1, 0)
        self.layout_b.setRowStretch(0, 1)

        self.layout_c = QtWidgets.QHBoxLayout(self.tab_frame_c)

        self.layout_d = QtWidgets.QHBoxLayout(self.tab_frame_d)

        self.layout_a.setObjectName("layout_a")
        self.layout_b.setObjectName("layout_b")
        self.layout_c.setObjectName("layout_c")
        self.layout_d.setObjectName("layout_d")
    
    def onChange(self, tab_index): # Changed Tab Listener
        pass
    
    def build_frames(self, centralwidget):
        self.tab_frame_a = QtWidgets.QFrame(centralwidget)
        self.tab_frame_a.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tab_frame_a.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tab_frame_a.setObjectName("tab_frame_a")

        self.tab_frame_b = QtWidgets.QFrame(centralwidget)
        self.tab_frame_b.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tab_frame_b.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tab_frame_b.setObjectName("tab_frame_b")

        self.tab_frame_c = QtWidgets.QFrame(centralwidget)
        self.tab_frame_c.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tab_frame_c.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tab_frame_c.setObjectName("tab_frame_c")
        
        self.tab_frame_d = QtWidgets.QFrame(centralwidget)
        self.tab_frame_d.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.tab_frame_d.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tab_frame_d.setObjectName("tab_frame_d")

    def closeEvent(self):
        #Your desired functionality here
        self.logger.warning('Application Closing...')
        self.view.shut_down()
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
        self.menuBar.setStyleSheet("background-color: rgb(225, 225, 225)")       
        file_menu = self.menuBar.addMenu('&File')
        file_menu = self.menuBar.addMenu('&Edit')
        file_menu = self.menuBar.addMenu('&Settings')
        file_menu = self.menuBar.addMenu('&Help')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    primaryWindow = QtWidgets.QMainWindow()
    application = Application(primaryWindow)
    primaryWindow.show()
    sys.exit(app.exec_())