# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
import sys

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from auto_resizing_text_edit import AutoResizingTextEdit

class Ui_PrimaryWindow(object):

    def setupUi(self, PrimaryWindow):

        PrimaryWindow.setObjectName("PrimaryWindow")
        PrimaryWindow.resize(1000, 600)
        PrimaryWindow.setStyleSheet("background-color: rgb(235, 235, 235);")

        # Keyboard shortcuts
        action = QAction("Quit Application", PrimaryWindow)
        action.setShortcut("Ctrl+Q")
        action.setStatusTip('Quit Application')
        # action.triggered.connect(sys.exit())

        # Menu Bar
        self.menuBar = PrimaryWindow.menuBar() 
        self.menuBar.setStyleSheet("background-color: rgb(255, 255, 255)")       
        file_menu = self.menuBar.addMenu('&File')
        file_menu = self.menuBar.addMenu('&Edit')
        file_menu = self.menuBar.addMenu('&Settings')
        file_menu = self.menuBar.addMenu('&Help')


        self.centralwidget = QtWidgets.QWidget(PrimaryWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.widget_2 = QtWidgets.QWidget(self.frame)
        self.widget_2.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.widget_2.setObjectName("widget_2")

        self.horizontalLayout.addWidget(self.widget_2)

        self.widget = QtWidgets.QWidget(self.frame)
        self.widget.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.widget.setObjectName("widget")

        # Gif Animation 
        self.widget_2.setStyleSheet("background-color: rgb(0, 140, 180);")

        self.status_txt = QtWidgets.QLabel(self.frame)
        self.status_txt.setGeometry(QtCore.QRect(100, 10, 300, 230))
        self.status_txt.setAlignment(Qt.AlignCenter)
        self.status_txt.setStyleSheet("background-color: rgb(0, 140, 180);")
        movie = QtGui.QMovie("assets/cycle.gif")
        self.status_txt.setMovie(movie)
        movie.start()
        self.status_txt.setLayout(QtWidgets.QHBoxLayout())

        # Set label in pane-1
        self.label_pane_1 = QtWidgets.QLabel(self.widget_2)
        self.label_pane_1.setGeometry(QtCore.QRect(175, 195, 230, 100))

        font = QtGui.QFont()
        font.setFamily("Dubai Light")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)

        self.label_pane_1.setFont(font)
        self.label_pane_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_pane_1.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_pane_1.setObjectName("label")
        # Set label in pane-1 End

        self.horizontalLayout.addWidget(self.widget)
        self.verticalLayout.addWidget(self.frame)

        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # Research Pane
        self.widget_4 = QtWidgets.QWidget(self.frame_2)
        self.widget_4.setStyleSheet("background-color: rgb(100, 100, 100);")
        self.widget_4.setObjectName("widget_4")

        self.verticalScrollBar = QtWidgets.QScrollBar(self.widget_4)
        self.verticalScrollBar.setGeometry(QtCore.QRect(425, 40, 20, 200))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")

        # editor = AutoResizingTextEdit()
        # editor.setMinimumLines(1)
        # editor.setParent(self.widget_4)

        self.textEdit = QtWidgets.QTextEdit(self.widget_4)
        self.textEdit.setReadOnly(True)
        self.textEdit.setGeometry(QtCore.QRect(20, 40, 400, 200))
        self.textEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit.setObjectName("textEdit")

        # self.horizontalLayout_2.addWidget(editor)
        # self.horizontalLayout_2.addStretch()

        self.label = QtWidgets.QLabel(self.widget_4)
        self.label.setGeometry(QtCore.QRect(150, 10, 150, 20))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)

        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setStyleSheet("color: rgb(255, 255, 255)")
        self.label.setObjectName("label")

        self.horizontalLayout_2.addWidget(self.widget_4)

        self.widget_3 = QtWidgets.QWidget(self.frame_2)
        self.widget_3.setAutoFillBackground(False)
        self.widget_3.setStyleSheet("background-color: rgb(0, 140, 180);")
        self.widget_3.setObjectName("widget_3")

        self.progressBar = QtWidgets.QProgressBar(self.widget_3)
        self.progressBar.setGeometry(QtCore.QRect(30, 70, 231, 23))

        font = QtGui.QFont()
        font.setFamily("Calibri")

        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")

        self.simulate_button = QtWidgets.QPushButton(self.widget_3)
        self.simulate_button.setGeometry(QtCore.QRect(30, 20, 151, 23))

        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(7)

        self.simulate_button.setFont(font)
        self.simulate_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.simulate_button.setAcceptDrops(False)
        self.simulate_button.setStyleSheet("background-color: rgb(0, 190, 0); color: white;")
        self.simulate_button.setObjectName("simulate_button")

        self.widget_5 = QtWidgets.QWidget(self.widget_3)
        self.widget_5.setGeometry(QtCore.QRect(30, 160, 171, 31))
        self.widget_5.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.widget_5.setObjectName("widget_5")

        self.radioButton = QtWidgets.QRadioButton(self.widget_5)
        self.radioButton.setGeometry(QtCore.QRect(10, 5, 161, 20))
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout_2.addWidget(self.widget_3)

        # Trend graph animation for now
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.trend = QtWidgets.QLabel(self.widget)
        self.trend.setGeometry(QtCore.QRect(0, 0, 500, 250))
        self.trend.setAlignment(Qt.AlignCenter)
        self.trend.setStyleSheet("background-color: rgb(255, 255, 255);")
        movie = QtGui.QMovie("assets/trend.gif")
        self.trend.setMovie(movie)
        movie.start()
        self.trend.setLayout(QtWidgets.QHBoxLayout())

        # Display all
        self.verticalLayout.addWidget(self.frame_2)
        PrimaryWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(PrimaryWindow)
        QtCore.QMetaObject.connectSlotsByName(PrimaryWindow)

    def retranslateUi(self, PrimaryWindow):
        _translate = QtCore.QCoreApplication.translate
        PrimaryWindow.setWindowTitle(_translate("PrimaryWindow", "Arduino Software - Human Activity Recognition via PPG sensor"))
        PrimaryWindow.setWindowIcon(QtGui.QIcon("assets/desktop-icon.png"))
        self.label.setText(_translate("PrimaryWindow", "Research and Findings"))
        self.label_pane_1.setText(_translate("PrimaryWindow", "Activity: Slow Cycle"))
        self.simulate_button.setToolTip(_translate("PrimaryWindow", "<html><head/><body><p>Select PPG data file via csv</p></body></html>"))
        self.simulate_button.setText(_translate("PrimaryWindow", "Simulate Activity Recognition"))
        self.radioButton.setText(_translate("PrimaryWindow", "Is Arduino PPG Connected?"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    PrimaryWindow = QtWidgets.QMainWindow()
    ui = Ui_PrimaryWindow()
    ui.setupUi(PrimaryWindow)
    PrimaryWindow.show()
    sys.exit(app.exec_())

