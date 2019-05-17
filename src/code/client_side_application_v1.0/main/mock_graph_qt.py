import sys
try:
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
except:
    pass
    
import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

class TestWindow(QWidget):
    def __init__(self, Qwidget, parent=None):
        super(FenetrePrincipale, self).__init__(parent)
        self.qwidget = Qwidget
        self.setupUi(self)

    # Fonction de configuration de la classe
    def setupUi(self, Form):
        self.Form = Form

        Form.setMaximumSize(320, 200)

        self.creation_GUI()
        self.creation_figure()
        self.creation_layout()

        self.tabWidget.setCurrentIndex(0)
        self.Bouton_quitter.clicked.connect(self.close)

    def resizeEvent(self, QResizeEvent):
        self.tabWidget.setMaximumSize(QSize(self.width() - 20, self.height() - 60))

    def creation_GUI(self):
        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.qwidget, "  Tab1  ")

        self.Widget_choixPalette_Label = QLabel(self.qwidget)
        self.Widget_choixPalette_Label.setText("Text1")
        self.Widget_choixPalette_ComboBox = QComboBox(self.qwidget)
        self.Widget_choixPalette_ComboBox.addItem("Try1")
        self.Widget_choixPalette_ComboBox.addItem("Try2")

        self.Bouton_quitter = QPushButton(self.qwidget)
        self.Bouton_quitter.setText("Quit")

    def creation_layout(self):
        LayoutForm = QGridLayout(self)
        LayoutForm.addWidget(self.qwidget, 0, 0, 1, 1)

        LayoutTab1 = QGridLayout(self.qwidget)

        LayoutTab1.addWidget(self.Widget_choixPalette_Label, 0, 1, 1, 1)
        LayoutTab1.addWidget(self.Widget_choixPalette_ComboBox, 1, 1, 1, 1)
        self.Widget_choixPalette_ComboBox.setMinimumWidth(200)

        LayoutTab1.addWidget(self.canvas, 2, 0, 1, 3)
        LayoutTab1.addWidget(self.Bouton_quitter, 2, 3, 1, 1, Qt.AlignRight | Qt.AlignBottom)

        LayoutTab1.setRowStretch(2, 1)
        LayoutTab1.setColumnStretch(0, 1)
        LayoutTab1.setColumnStretch(2, 1)

    def creation_figure(self):
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # QApplication.setStyle(QStyleFactory.create("plastique"))
    form = FenetrePrincipale()
    form.show()
    sys.exit(app.exec_())