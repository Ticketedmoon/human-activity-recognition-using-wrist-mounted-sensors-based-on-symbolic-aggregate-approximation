import sys
from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
import functools

class Movie_Player(QtWidgets.QLabel):

    currentActivity = None

    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(QtCore.QRect(135, 50, 225, 200))
        self.setAlignment(Qt.AlignCenter)

        # Default activity to display
        self.movie = QtGui.QMovie("../assets/idle.gif", QtCore.QByteArray(), self)
        self.setMovie(self.movie)
        self.set_animation("idle")

    @pyqtSlot('QString')
    def set_animation(self, activity):
        if (activity != self.currentActivity):
            try:
                if (activity != "highresistancebike"):
                    self.movie.setSpeed(50)
                else:
                    self.movie.setSpeed(100)
            finally:
                self.movie.stop()
                self.movie.setFileName("../assets/{}.gif".format(activity))
                self.movie.start()
                self.currentActivity = activity
