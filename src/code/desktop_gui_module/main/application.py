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

from menu_bar_builder import MenuBar
from tab_bar_plus import TabBarPlus
from activity_controller_pane import Activity_Controller_Pane
from activity_display_pane import Activity_Display_Pane
from research_window import Research_Window
from graph_pane import Graph_Pane

sys.path.append('../../')

from logger_module.Logger import Logger

class Application(QMainWindow):

    logger = Logger("../../", "logs/DesktopGUI")
    
    """ Font Properties """
    font = QtGui.QFont()
    font.setFamily("calibri")
    font.setBold(False)
    font.setPointSize(10)

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
        menu = MenuBar(PrimaryWindow, self)

    def open_settings(self):
        items = ("COM1","COM2","COM3", "COM4", "COM5")
        self.setWindowIcon(QtGui.QIcon('/path/to/icon.png'))

        port, isPressed = QInputDialog.getItem(self, "Application Settings", "Arduino Port:", items, 0, False)
        if isPressed and port:
            if port != self.view.graph_pane.port:
                self.view.graph_pane.update_port(port)            

    def open_about(self):
        d = QDialog()
        d.setWindowTitle("About the Application")
        d.setWindowIcon(QtGui.QIcon("../assets/desktop-icon.png"))
        d.setWindowModality(Qt.ApplicationModal)

        label = QLabel(d)
        label.setOpenExternalLinks(True)
        label.setFont(self.font)
        label.setText("Creator: Shane Creedon <br> Supervisor: Tomas Ward <br> \
            Project Website: <a href=\"https://www.projectactivityrecognition.ml\"> https://www.projectactivityrecognition.ml </a> <br><br> \
            This application was designed to showcase the potential that wearable sensor technology can provide through machine learning practices and \
            techniques. <br><br> \
            Human activity recognition (HAR) is an active area of research concerned with the classification of human motion. <br> \
            Cameras are the gold standard used in this area, but they are proven to have scalability and privacy issues. <br> \
            HAR studies have also been conducted with wearable devices consisting of inertial sensors. Perhaps the most common wearable, <br> \
            smart watches, comprising of inertial and optical sensors, allow for scalable, non-obtrusive studies. We are seeking to simplify this <br> \
            wearable approach further by determining if wrist-mounted optical sensing, usually used for heart rate determination, <br> \
            can also provide useful data for relevant activity recognition. <br><br> \
            If successful, this could eliminate the need for the inertial sensor, and so simplify the technological requirements in wearable HAR. <br> \
            We adopt a machine vision approach for activity recognition using optical signals combined with Symbolic Aggregate Approximation (SAX) and <br> \
            machine vision, so as to produce classifications that are easily explainable and interpretable by non-technical users. <br> \
            Specifically, time-series images of photoplethysmography (PPG) signals are used to retrain the penultimate layer of a pretrained <br> \
            convolutional neural network leveraging the concept of transfer learning. <br><br> \
            To use this application to its fullest potential, users are required to obtain an arduino PPG kit which is normally used for heart-rate determination. <br> \
            The application can be used to view your heart-rate in terms of microvolts on the real-time graph built using Matplotlib and Seaborn. <br> \
            Additionally, one can read about my research in the different areas of the project. <br> \
            The bulk of the project lies in the core functionality offered in terms of <span style=\"color: red;\"> activity recognition playback and real-time activity recognition playback. </span> <br> \
            With the playback function, you can select a past recording of a PPG signal in the form of a csv and submit it to our system. Activity recognition will be played back <br> \
            to you in semi-real-time. This is done using MQTT and cloud processing. The client-side application is a <strong> thin-client </strong>, meaning the bulk of the processing is done server-side. <br> \
            With the real-time playback function, the process is similar to the above in that the bulk of the intense CPU processing is done in the cloud. The client <br> \
            feeds a stream of PPG microvolt signals to the server where they are processed and a prediction returned to the user, in quasi-real-time.")
        label.adjustSize()
        label.move(25, 15)
        d.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    primaryWindow = QtWidgets.QMainWindow()
    application = Application(primaryWindow)
    primaryWindow.show()
    sys.exit(app.exec_())