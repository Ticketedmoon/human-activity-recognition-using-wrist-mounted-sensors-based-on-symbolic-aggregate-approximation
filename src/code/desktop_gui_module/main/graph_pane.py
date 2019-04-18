from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

from test_graph_qt import FenetrePrincipale
from canvas import Canvas

class Graph_Pane:

    def __init__(self, frame, layout, logger):
        # Set up logger for this class
        self.logger = logger
        
        # Build graph layout
        self.canvas = Canvas(layout)

    def build(self, layout):
        pass
        # self.canvas.read_from_ppg()
        # self.trend.move(125, 0)
        # self.trend.setAlignment(Qt.AlignCenter)
        # self.build_placeholder()
        
    # Trend graph animation Placeholder.
    def build_placeholder(self):
        if self.trend != None:
            movie = QtGui.QMovie("../assets/trend.gif")
            self.trend.setMovie(movie)
            movie.start()
            self.trend.setLayout(QtWidgets.QHBoxLayout())

    def stop_graph(self):
        self.logger.warning("Stopping Real Time Graph...")
        self.canvas.stop_real_time_graph = True