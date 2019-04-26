import sys
from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

from PyQt5.Qt import QApplication, QClipboard
from PyQt5.QtWidgets import QWidget, QPlainTextEdit
from PyQt5.QtCore import QSize

class Research_Window(QtWidgets.QWidget):

    # Takes frame_2 -> belongs to lower frame
    def __init__(self, frame, layout, logger):
        super(Research_Window, self).__init__()
        QtWidgets.QWidget.__init__(self)
        self.layout = layout
        self.frame = frame
        self.logger = logger

    def build_overview_research_pane(self, layout, frame):
        self.widget_4 = QtWidgets.QLabel(frame)
        self.widget_4.setAlignment(Qt.AlignCenter)
        self.widget_4.setOpenExternalLinks(True)

        font = QtGui.QFont()
        font.setFamily("calibri")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)

        self.widget_4.setFont(font)

        self.widget_4.setText("<span style=\"color: darkgreen;\">Project Research Areas</span>" + '<br><br>' +

                              "Follow my Progress: - <a href=\"https://www.projectactivityrecognition.ml/blog\">https://www.projectactivityrecognition.ml/blog</a>" + '<br><br>' +

                              "What is Human Activity Recognition? <a href=\"http://doras.dcu.ie/22433/\">http://doras.dcu.ie/22433/</a>" + '<br>' +
                              "What is Symbolic Aggregate Approximation? - <a href=\"http://doras.dcu.ie/22433/\">http://doras.dcu.ie/22433/</a>" + '<br>' +
                              "What are Convolutional Neural Networks? - <a href=\"http://doras.dcu.ie/22433/\">http://doras.dcu.ie/22433/</a>" + '<br>' +
                              "What is Transfer Learning? - <a href=\"http://doras.dcu.ie/22433/\">http://doras.dcu.ie/22433/</a>" + '<br><br>' +

                              "Developed By: Shane Creedon (<a href=\"https://www.skybreak.cf\">https://www.skybreak.cf</a>)" + '<br>' +
                              "Supervised By: Tomas Ward (<a href=\"https://www.insight-centre.org/users/tomas-ward\">https://www.insight-centre.org/users/tomas-ward</a>)" + '<br>')
        self.widget_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_4.setObjectName("widget_4")
        layout.addWidget(self.widget_4)

    def build_research_pane(self, layout, frame):
        self.widget_4 = QtWidgets.QLabel(frame)
        self.widget_4.setAlignment(Qt.AlignCenter)
        self.widget_4.setOpenExternalLinks(True)

        font = QtGui.QFont()
        font.setFamily("calibri")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(30)

        self.widget_4.setFont(font)

        self.widget_4.setText("<span style=\"color: darkgreen;\">Project Research Areas</span>" + '<br><br>' +

                              "Follow my Progress: - <a href=\"https://www.projectactivityrecognition.ml/blog\">https://www.projectactivityrecognition.ml/blog</a>" + '<br><br>' +

                              "What is Human Activity Recognition? <a href=\"http://doras.dcu.ie/22433/\">http://doras.dcu.ie/22433/</a>" + '<br>' +
                              "What is Symbolic Aggregate Approximation? - <a href=\"http://doras.dcu.ie/22433/\">http://doras.dcu.ie/22433/</a>" + '<br>' +
                              "What are Convolutional Neural Networks? - <a href=\"http://doras.dcu.ie/22433/\">http://doras.dcu.ie/22433/</a>" + '<br>' +
                              "What is Transfer Learning? - <a href=\"http://doras.dcu.ie/22433/\">http://doras.dcu.ie/22433/</a>" + '<br><br>' +

                              "Developed By: Shane Creedon (<a href=\"https://www.skybreak.cf\">https://www.skybreak.cf</a>)" + '<br>' +
                              "Supervised By: Tomas Ward (<a href=\"https://www.insight-centre.org/users/tomas-ward\">https://www.insight-centre.org/users/tomas-ward</a>)" + '<br>')
        self.widget_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_4.setObjectName("widget_4")
        layout.addWidget(self.widget_4)