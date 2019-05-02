import sys

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QWidget, QInputDialog, QLineEdit

class MenuBar:

    def __init__(self, PrimaryWindow, application):
        self.application = application
        self.menuBar = PrimaryWindow.menuBar() 
        self.menuBar.setStyleSheet("background-color: rgb(225, 225, 225)")

        self.build_basic_menu_items()
        self.attach_file_options()

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
