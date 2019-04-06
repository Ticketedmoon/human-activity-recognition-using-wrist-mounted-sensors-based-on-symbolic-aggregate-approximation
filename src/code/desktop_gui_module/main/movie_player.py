import sys
from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
import functools

class Movie_Player(QtWidgets.QLabel):

    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(QtCore.QRect(135, 50, 225, 200))
        self.setAlignment(Qt.AlignCenter)

        # Default activity to display
        self.movie = QtGui.QMovie("../assets/walk.gif", QtCore.QByteArray(), self)
        self.movie.setSpeed(150)
        self.setMovie(self.movie)

        self.set_animation("walk")

    @pyqtSlot('QString')
    def set_animation(self, activity):
        try:
            self.movie.stop()
            self.movie.setFileName("../assets/{}.gif".format(activity))
        finally:
            self.movie.start()
