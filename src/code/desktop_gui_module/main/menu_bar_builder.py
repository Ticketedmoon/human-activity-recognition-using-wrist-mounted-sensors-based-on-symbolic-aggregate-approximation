import sys

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit

class MenuBar:

    """ Font Properties """
    font = QtGui.QFont()
    font.setFamily("calibri")
    font.setBold(False)
    font.setPointSize(10)

    def __init__(self, PrimaryWindow, application):
        self.application = application
        self.menuBar = PrimaryWindow.menuBar() 
        self.menuBar.setStyleSheet("background-color: rgb(225, 225, 225)")

        self.build_basic_menu_items()
        self.attach_file_options()
        self.attach_settings_options()
        self.attach_help_options()

    def build_basic_menu_items(self):
        self.fileMenu = self.menuBar.addMenu('File')
        self.settingsMenu = self.menuBar.addMenu('Settings')
        self.helpMenu = self.menuBar.addMenu('Help')

    def attach_file_options(self):
        settingsButton = QAction('Settings', self.application)
        settingsButton.setShortcut('Ctrl+S')
        settingsButton.setStatusTip('Open Settings')
        settingsButton.triggered.connect(self.application.open_settings)
        self.fileMenu.addAction(settingsButton)
        
        helpButton = QAction('About', self.application)
        helpButton.setShortcut('Ctrl+A')
        helpButton.setStatusTip('Help Options')
        helpButton.triggered.connect(self.application.open_about)
        self.fileMenu.addAction(helpButton)

        exitButton = QAction('Exit', self.application)
        exitButton.setShortcut('Ctrl+E')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.application.closeEvent)
        self.fileMenu.addAction(exitButton)

    def attach_settings_options(self):
        settingsButton = QAction('Port', self.application)
        settingsButton.setShortcut('Ctrl+P')
        settingsButton.setStatusTip('Open Port Settings')
        settingsButton.triggered.connect(self.application.open_settings)
        self.settingsMenu.addAction(settingsButton)

    def attach_help_options(self):
        helpButton = QAction('Application Guide', self.application)
        helpButton.setShortcut('Ctrl+H')
        helpButton.setStatusTip('Application Guide')
        helpButton.triggered.connect(self.application.open_help_guide)
        self.helpMenu.addAction(helpButton)

    def setup_about_label(self, d):
        label = QLabel(d)
        label.setOpenExternalLinks(True)
        label.setFont(self.font)
        label.setText("Creator: Shane Creedon <br> Supervisor: Tomas Ward <br> \
            Project Website: <a href=\"https://www.projectactivityrecognition.ml\"> https://www.projectactivityrecognition.ml </a> <br> \
            <h2> About the Application </h2> <br>\
            This application was designed to showcase the potential that wearable sensor technology can provide through machine learning practices and \
            techniques. <br> \
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


    def setup_help_label(self, d):
        label = QLabel(d)
        label.setOpenExternalLinks(True)
        label.setFont(self.font)
        label.setText("<h2> Application Functionality Guide</h2><br> \
            1. The application is split into 4 window panes accessible via the tabbed menu bar found at the top of the window. <br> \
            2. The first tabbed window pane labelled: <strong> Overview </strong> has a summarised version of the remaining 3 tabs. <br> \
               - In this tab, you can view each function the application provides. <br> \
            3. The second tab labelled: <strong> Activity Recognition View </strong>, you can test out our playback features which utilise PPG recordings <br> \
               - to display what activity a person was doing. Old PPG recordings can be submitted in the form of a .csv to playback activities from the past <br> \
               - or, you can try out our 'real-time activity recognition feature' which offers, real-time playback of activity recognition with a connected <br> \
               - arduino PPG device. <br> \
            4. The third tab labelled: <strong> 'Real-Time Graph View' </strong> offers a larger more read-able graph than the one visible on the 'overview' tab. <br> \
               - You can view your arduino PPG recordings and notice the motion artefacts distilled within the reading. <br> \
            5. The fourth and final tab, labelled: <strong> 'Research View' </strong>, users can read about the research undergone within this project's life-cycle. <br> \
               - additionally, the techniques used to achieve activity recognition are hyperlinked, in addition to the project blog and project website for more information.")
        label.adjustSize()
        label.move(25, 15)
