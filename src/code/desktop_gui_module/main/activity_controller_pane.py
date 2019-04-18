import sys
import threading

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

from tkinter import filedialog
from tkinter import *

sys.path.append('../../')

class Activity_Controller_Pane():

    loading = None

    def __init__(self, frame, layout, logger, display):
        # Controller has access to display
        self.display = display

        # Logger Initialize
        self.logger = logger

        self.widget_3 = QtWidgets.QWidget(frame)
        self.widget_3.setAutoFillBackground(False)
        self.widget_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_3.setObjectName("widget_3")

        self.build(layout)

    # TODO: Refactor
    def build(self, layout):
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(8.5)

        self.progressBar = QtWidgets.QProgressBar(self.widget_3)
        self.progressBar.setGeometry(QtCore.QRect(30, 80, 231, 23))
        self.progressBar.setStyleSheet("background-color: rgb(0, 70, 150); color: white;")
        self.progressBar.setFont(font)
        self.progressBar.setObjectName("progressBar")

        self.simulate_button = QtWidgets.QPushButton(self.widget_3)
        self.simulate_button.setGeometry(QtCore.QRect(30, 20, 180, 23))

        self.simulate_button.setFont(font)
        self.simulate_button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.simulate_button.setAcceptDrops(False)
        self.simulate_button.setStyleSheet("background-color: rgb(0, 180, 30); color: white;")
        self.simulate_button.setIcon(QIcon(QPixmap("../assets/playback-2.png")))
        self.simulate_button.resize(180, 40)

        self.simulate_button.setObjectName("simulate_button")
        self.simulate_button.setText("Activity Recognition Playback")
        self.simulate_button.clicked.connect(self.submit_ppg_files)

        self.widget_5 = QtWidgets.QWidget(self.widget_3)
        self.widget_5.setGeometry(QtCore.QRect(45, 207, 171, 31))
        self.widget_5.setStyleSheet("color: black;")
        self.widget_5.setObjectName("widget_5")
        self.widget_5.setFont(font)

        self.ppg_connection = QtWidgets.QLabel(self.widget_5)
        self.ppg_connection.setGeometry(QtCore.QRect(15, 5, 161, 20))
        self.ppg_connection.setObjectName("ppg_connection")
        self.ppg_connection.setText("Arduino PPG Connected?")
        self.ppg_connection.setFont(font)

        # Red dot widget container
        self.widget_6 = QtWidgets.QWidget(self.widget_3)
        self.widget_6.setGeometry(QtCore.QRect(5, 205, 50, 31))
        self.widget_6.setAutoFillBackground(False)
        self.widget_6.setObjectName("widget_6")

        # red dot
        self.red_dot = QtWidgets.QLabel(self.widget_6)
        self.red_dot.setGeometry(QtCore.QRect(5, 8, 40, 40))
        
        red_cross = QtGui.QMovie("../assets/red-cross.gif")
        self.red_dot.setMovie(red_cross)
        self.red_dot.setAlignment(Qt.AlignRight)
        red_cross.start()

        self.red_dot.setLayout(QtWidgets.QHBoxLayout())
        layout.addWidget(self.widget_3)

        # loading icon widget container
        self.widget_7 = QtWidgets.QWidget(self.widget_3)
        self.widget_7.setGeometry(QtCore.QRect(215, 0, 100, 65))
        self.widget_7.setAutoFillBackground(False)
        self.widget_7.setObjectName("widget_7")

        self.loader = QtWidgets.QLabel(self.widget_7)
        self.loader.setGeometry(QtCore.QRect(0, 0, 100, 75))
        self.loader.setAlignment(Qt.AlignCenter)

        self.loading = QtGui.QMovie("../assets/loader.gif")
        self.loader.setMovie(self.loading)
        self.loader.setLayout(QtWidgets.QHBoxLayout())

    def submit_ppg_files(self):
        try:
            root = Tk().withdraw()
            file_path = filedialog.askopenfilename(initialdir = "/",title = "Select file", filetypes = (("timestamp & PPG recordings CSV","*.csv"), ("all files","*.*")))
            if (file_path != ""):
                self.logger.debug("Simulating Activity Recognition for file: {" + str(file_path) + "}")
                simulate_thread = threading.Thread(target=self.display.convert_and_send, args=[file_path])
                simulate_thread.start()

                if (self.loading is not None):
                    self.loading.start()
                    self.update_playback_button_state(False, "background-color: rgb(200, 200, 200); color: black;")
        except Exception as error:
            self.logger.error("Error: " + repr(error))    

    def update_playback_button_state(self, enabled=True, stylesheet="background-color: rgb(0, 180, 30); color: white"):
        self.simulate_button.setEnabled(enabled) 
        self.simulate_button.setStyleSheet(stylesheet)