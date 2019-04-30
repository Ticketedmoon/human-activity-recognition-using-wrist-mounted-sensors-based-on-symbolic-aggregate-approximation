from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

from test_graph_qt import FenetrePrincipale
from canvas import Canvas

class Graph_Pane(QtWidgets.QWidget):

    def __init__(self, layout, logger):
        super(Graph_Pane, self).__init__()
        QtWidgets.QWidget.__init__(self)
        self.logger = logger
        self.graph = Canvas(layout, self.logger) # Widget is added from Canvas

    # TODO: Fix
    def layout_widgets(self, layout):
        pass
        #self.graph.layout_widgets(layout)

    # Trend graph animation Placeholder.
    def build_placeholder(self):
        if self.trend != None:
            movie = QtGui.QMovie("../assets/trend.gif")
            self.trend.setMovie(movie)
            movie.start()
            self.trend.setLayout(QtWidgets.QHBoxLayout())

    def get_samples(self):
        return self.graph.samples

    def get_microvolts(self):
        return self.graph.microvolts

    def get_microvolt_reading(self):
        if len(self.graph.microvolts) > 0:
            return self.graph.microvolts[0]
        return 0

    def stop_graph(self):
        self.logger.warning("Stopping Real Time Graph...")
        self.graph.stop_real_time_graph = True

    def check_arduino_connection(self):
        return self.graph.is_arduino_connected