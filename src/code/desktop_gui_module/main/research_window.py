import sys

try:
    from PyQt5.Qt import *
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
    from PyQt5.QtGui import *

    from PyQt5.Qt import QApplication, QClipboard
    from PyQt5.QtWidgets import QWidget, QPlainTextEdit
    from PyQt5.QtCore import QSize
except:
    pass

class Research_Window(QtWidgets.QWidget):

    """ Font Properties """
    font = QtGui.QFont()
    font.setFamily("calibri")
    font.setBold(False)

    # Takes frame_2 -> belongs to lower frame
    def __init__(self, logger):
        super(Research_Window, self).__init__()
        QtWidgets.QWidget.__init__(self)
        self.logger = logger

        self.widget_4 = QtWidgets.QLabel()
        self.widget_4.setAlignment(Qt.AlignCenter)
        self.widget_4.setOpenExternalLinks(True)

        self.font.setPointSize(10)
        self.font.setWeight(50)

        self.widget_4.setFont(self.font)
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

        self.widget_5 = QtWidgets.QLabel()
        self.widget_5.setAlignment(Qt.AlignCenter)
        self.widget_5.setOpenExternalLinks(True)
        self.widget_5.adjustSize()

        self.font.setPointSize(10)
        self.font.setWeight(30)
        self.widget_5.setFont(self.font)
        self.widget_5.setText("<span style=\"color: darkgreen;\">Project Research Areas</span>" + '<br><br>' +

                              "Follow my Progress: - <a href=\"https://www.projectactivityrecognition.ml/blog\">https://www.projectactivityrecognition.ml/blog</a>" + '<br><br>' +

                              "What is Human Activity Recognition? <a href=\"http://doras.dcu.ie/22433/\">http://doras.dcu.ie/22433/</a>" + '<br>' +
                              "What is Symbolic Aggregate Approximation? - <a href=\"http://doras.dcu.ie/22433/\">http://doras.dcu.ie/22433/</a>" + '<br>' +
                              "What are Convolutional Neural Networks? - <a href=\"http://doras.dcu.ie/22433/\">http://doras.dcu.ie/22433/</a>" + '<br>' +
                              "What is Transfer Learning? - <a href=\"http://doras.dcu.ie/22433/\">http://doras.dcu.ie/22433/</a>" + '<br><br>' +

                            "Human activity recognition (HAR) is an active area of research concerned with the classification of human motion. <br>" +
                            "Cameras are the gold standard used in this area, but they are proven to have scalability and privacy issues. <br>" +
                            "HAR studies have also been conducted with wearable devices consisting of inertial sensors. Perhaps the most common wearable, <br>" +
                            "smart watches, comprising of inertial and optical sensors, allow for scalable, non-obtrusive studies. We are seeking to simplify this <br>" + 
                            "wearable approach further by determining if wrist-mounted optical sensing, usually used for heart rate determination, <br>" +
                            "can also provide useful data for relevant activity recognition. <br><br>" +
                            "If successful, this could eliminate the need for the inertial sensor, and so simplify the technological requirements in wearable HAR. <br>" +
                            "We adopt a machine vision approach for activity recognition using optical signals combined with Symbolic Aggregate Approximation (SAX) and <br>" +
                            "machine vision, so as to produce classifications that are easily explainable and interpretable by non-technical users. <br>" +
                            "Specifically, time-series images of photoplethysmography (PPG) signals are used to retrain the penultimate layer of a pretrained <br>" +
                            "convolutional neural network leveraging the concept of transfer learning. <br><br>" +
                            "To use this application to its fullest potential, users are required to obtain an arduino PPG kit which is normally used for heart-rate determination. <br>" +
                            "The application can be used to view your heart-rate in terms of microvolts on the real-time graph built using Matplotlib and Seaborn. <br>" +
                            "Additionally, one can read about my research in the different areas of the project. <br>" +
                            "The bulk of the project lies in the core functionality offered in terms of <span style=\"color: red;\"> activity recognition playback and real-time activity recognition playback. </span> <br>" +
                            "With the playback function, you can select a past recording of a PPG signal in the form of a csv and submit it to our system. Activity recognition will be played back <br>" +
                            "to you in semi-real-time. This is done using MQTT and cloud processing. The client-side application is a <strong> thin-client </strong>, meaning the bulk of the processing is done server-side. <br>" + 
                            "With the real-time playback function, the process is similar to the above in that the bulk of the intense CPU processing is done in the cloud. The client <br>" + 
                            "feeds a stream of PPG microvolt signals to the server where they are processed and a prediction returned to the user, in quasi-real-time. <br><br>" +  

                              "Developed By: Shane Creedon (<a href=\"https://www.skybreak.cf\">https://www.skybreak.cf</a>)" + '<br>' +
                              "Supervised By: Tomas Ward (<a href=\"https://www.insight-centre.org/users/tomas-ward\">https://www.insight-centre.org/users/tomas-ward</a>)" + '<br>')
        self.widget_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_5.setObjectName("widget_4")

    def build_overview_research_pane(self, layout):
        layout.addWidget(self.widget_4)

    def build_research_pane(self, layout):
        layout.addWidget(self.widget_5)