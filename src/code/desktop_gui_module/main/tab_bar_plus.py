import sys

from PyQt5.Qt import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import *

from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QInputDialog
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QTabBar
from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

from activity_controller_pane import Activity_Controller_Pane
from activity_display_pane import Activity_Display_Pane
from research_window import Research_Window
from graph_pane import Graph_Pane

# self.activity_display_pane = Activity_Display_Pane(self.frame, self.horizontalLayout, self.logger)
# self.graph_pane = Graph_Pane(self.frame, self.horizontalLayout, self.logger)
# self.activity_controller_pane = Activity_Controller_Pane(self.frame_2, self.horizontalLayout_2, self.logger, self.activity_display_pane, self.graph_pane)
class TabBarPlus(QTabWidget):

    def __init__(self, tab_frame_a, tab_frame_b, tab_frame_c, tab_frame_d, layout_a, layout_b, layout_c, layout_d, logger):
        super(TabBarPlus, self).__init__()
        self.logger = logger

        # Overview
        self.activity_display_pane = Activity_Display_Pane(logger, tab_frame_a, layout_a)
        self.graph_pane = Graph_Pane(tab_frame_a, layout_a, logger)
        self.activity_controller_pane = Activity_Controller_Pane(tab_frame_a, layout_a, logger, self.graph_pane)
        self.activity_controller_pane.set_display(self.activity_display_pane)

        self.research_pane = Research_Window(tab_frame_a, layout_a, logger)
        self.research_pane.build_overview_research_pane(layout_a, tab_frame_a)
        # Overview (End)

        # Tab 2, Tab 3, Tab 4
        self.graph_pane_2 = Graph_Pane(tab_frame_c, layout_c, logger)
        self.activity_controller_pane_2 = Activity_Controller_Pane(tab_frame_b, layout_b, logger, self.graph_pane_2)
        self.activity_display_pane_2 = Activity_Display_Pane(logger, tab_frame_b, layout_b, self.activity_display_pane)
        self.activity_controller_pane_2.set_display(self.activity_display_pane_2)

        self.research_pane_2 = Research_Window(tab_frame_d, layout_d, logger)
        self.research_pane_2.build_research_pane(layout_d, tab_frame_d)
        # Tab 2, Tab 3, Tab 4 (End)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        self.addTab(self.tab1,"Tab 1")
        self.addTab(self.tab2,"Tab 2")
        self.addTab(self.tab3,"Tab 3")
        self.addTab(self.tab4,"Tab 4")

        self.tab1UI(layout_a)
        self.tab2UI(layout_b)
        self.tab3UI(layout_c)
        self.tab4UI(layout_d)

    def tab1UI(self, layout):
        # Overview Tab?
        # layout.addWidget(self.graph_pane, 0, 0)
        # layout.addWidget(self.research_pane, 0, 1)
        # layout.addWidget(self.activity_display_pane, 1, 0)
        # layout.addWidget(self.activity_controller_pane, 1, 1)
        self.setTabText(0, "Overview")
        self.tab1.setLayout(layout)

    def tab2UI(self, layout):
        #layout.addWidget(self.activity_controller_pane, 0, 0)
        #layout.addWidget(self.activity_display_pane, 0, 1)
        self.setTabText(1, "Activity Recognition View")
        self.tab2.setLayout(layout)

    def tab3UI(self, layout):
        self.setTabText(2, "Real-Time Graph View")
        self.tab3.setLayout(layout)
            
    def tab4UI(self, layout):
        # layout.addStretch()
        self.setTabText(3, "Research View")
        self.tab4.setLayout(layout)

    def shut_down(self):
        self.activity_controller_pane.resolve()
        self.activity_controller_pane_2.resolve()
        self.activity_display_pane.stop_display()
        self.activity_display_pane_2.stop_display()
        self.graph_pane.stop_graph()
        self.graph_pane_2.stop_graph()

    def build_overview_layout(self):
        self.top_frame_overview = QtWidgets.QFrame(self)
        self.top_frame_overview.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.top_frame_overview.setFrameShadow(QtWidgets.QFrame.Raised)
        self.top_frame_overview.setObjectName("top_frame_overview")

        self.bottom_frame_overview = QtWidgets.QFrame(self)
        self.bottom_frame_overview.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bottom_frame_overview.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bottom_frame_overview.setObjectName("bottom_frame_overview")

        # Layouts
        self.layout_top_overview = QtWidgets.QHBoxLayout(self.top_frame_overview)        
        self.layout_bottom_overview = QtWidgets.QHBoxLayout(self.bottom_frame_overview)
        self.layout_top_overview.setObjectName("layout_top_overview")
        self.layout_bottom_overview.setObjectName("layout_bottom_overview")