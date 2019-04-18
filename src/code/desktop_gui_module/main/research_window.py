from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

class Research_Window:

    # Takes frame_2 -> belongs to lower frame
    def __init__(self, frame, layout, logger):
        self.logger = logger
        self.widget_4 = QtWidgets.QWidget(frame)
        self.widget_4.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.widget_4.setObjectName("widget_4")
        layout.addWidget(self.widget_4)
        self.build()

    # Research Pane
    def build(self):
        self.verticalScrollBar = QtWidgets.QScrollBar(self.widget_4)
        self.verticalScrollBar.setGeometry(QtCore.QRect(425, 40, 20, 200))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")

        self.textEdit = QtWidgets.QTextEdit(self.widget_4)
        self.textEdit.setReadOnly(True)
        self.textEdit.setGeometry(QtCore.QRect(20, 40, 400, 200))
        self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit.setObjectName("textEdit")
        
        self.label = QtWidgets.QLabel(self.widget_4)
        self.label.setGeometry(QtCore.QRect(150, 10, 150, 20))
        self.label.setText("Research and Findings")

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)

        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("color: rgb(255, 255, 255)")
        self.label.setObjectName("label")