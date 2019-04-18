import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from mpl_toolkits.axes_grid1 import make_axes_locatable

class Canvas(FigureCanvas):

    def __init__(self, parent = None, width =2, height = 2, dpi =100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
    
    def create_figure(self):
        # Create figure (transparent background)
        self.figure = plt.figure()
        # self.figure.patch.set_facecolor('None')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color:transparent;")

        # Adding one subplot for image
        self.axe0 = self.figure.add_subplot(111)
        self.axe0.get_xaxis().set_visible(False)
        self.axe0.get_yaxis().set_visible(False)
        # plt.tight_layout()

        # Data for init image
        self.imageInit = [[255] * 320 for i in range(240)]
        self.imageInit[0][0] = 0

        # Init image and add colorbar
        self.image = self.axe0.imshow(self.imageInit, interpolation='none')
        divider = make_axes_locatable(self.axe0)
        cax = divider.new_vertical(size="5%", pad=0.05, pack_start=True)
        self.colorbar = self.figure.add_axes(cax)
        self.figure.colorbar(self.image, cax=cax, orientation='horizontal')

        plt.subplots_adjust(left=0, bottom=0.05, right=1, top=1, wspace=0, hspace=0)

        self.canvas.draw()
