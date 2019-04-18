from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

class Graph_Pane:

    def __init__(self, frame, layout, logger):
        self.logger = logger
        self.widget = QtWidgets.QWidget(frame)
        self.widget.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.widget.setObjectName("widget")
        layout.addWidget(self.widget)
        self.build()

    def build(self):
        # Trend graph animation for now
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.trend = QtWidgets.QLabel(self.widget)
        self.trend.setGeometry(QtCore.QRect(0, 0, 500, 250))
        self.trend.setAlignment(Qt.AlignCenter)
        self.trend.setStyleSheet("background-color: rgb(255, 255, 255);")
        # self.canvas = FenetrePrincipale(self.widget)
        movie = QtGui.QMovie("../assets/trend.gif")
        self.trend.setMovie(movie)
        movie.start()
        self.trend.setLayout(QtWidgets.QHBoxLayout())