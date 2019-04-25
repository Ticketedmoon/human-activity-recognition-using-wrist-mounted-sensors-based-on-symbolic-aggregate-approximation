from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

from test_graph_qt import FenetrePrincipale
from canvas import Canvas

class Graph_Pane(QtWidgets.QWidget):

    canvas = None

    def __init__(self, frame, layout, logger):
        super(Graph_Pane, self).__init__()
        QtWidgets.QWidget.__init__(self)

        # Set up logger for this class
        print("creating graph")
        self.logger = logger

        # !Important for access
        self.layout = layout
        self.frame = frame
        
        # Build graph layout
        if self.canvas is None:
            print("creating canvas")
            self.canvas = Canvas(layout, logger)

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

    def check_arduino_connection(self):
        return self.canvas.is_arduino_connected