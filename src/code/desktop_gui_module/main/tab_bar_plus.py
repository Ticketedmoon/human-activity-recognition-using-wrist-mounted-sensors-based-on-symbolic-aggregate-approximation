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

class TabBarPlus(QTabWidget):

    def __init__(self, layout_a, layout_b, layout_c, layout_d, logger):
        super(TabBarPlus, self).__init__()
        self.logger = logger

        # Build all pane objects
        self.activity_display_pane = Activity_Display_Pane(logger)
        self.activity_display_pane.layout_widgets(layout_a)
        
        self.graph_pane = Graph_Pane(layout_a, logger)
        self.graph_pane.layout_widgets(layout_a)

        self.activity_controller_pane = Activity_Controller_Pane(logger, self.graph_pane)
        self.activity_controller_pane.set_display(self.activity_display_pane)
        self.activity_controller_pane.layout_widgets(layout_a)

        self.research_pane = Research_Window(logger)
        self.research_pane.build_overview_research_pane(layout_a)

        # Tab B, C, D
        self.build_activity_display(layout_b)
        self.build_graph(layout_c)
        self.build_research_pane(layout_d)

        # Start graph listener
        self.graph_pane.start_graph_listener()

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

    # Overview Tab
    def tab1UI(self, layout):
        self.setTabText(0, "Overview")
        self.tab1.setLayout(layout)

    # Display Recognition Tab
    def tab2UI(self, layout):
        self.setTabText(1, "Activity Recognition View")
        self.tab2.setLayout(layout)

    # Graph View Time
    def tab3UI(self, layout):
        self.setTabText(2, "Real-Time Graph View")
        self.tab3.setLayout(layout)
            
    # Research Tab
    def tab4UI(self, layout):
        # layout.addStretch()
        self.setTabText(3, "Research View")
        self.tab4.setLayout(layout)

    # Overview widgets
    def build_overview(self, layout):
        # Display Pane
        self.activity_display_pane.layout_widgets(layout)

        # Graph Pane
        self.graph_pane.layout_widgets(layout)
        
        # Controller
        self.activity_controller_pane.layout_widgets(layout)        

        # Research Pane
        self.research_pane.build_overview_research_pane(layout)

    # Tab 2, Tab 3, Tab 4
    def build_activity_display(self, layout):
        self.activity_controller_pane.layout_widgets(layout)
        self.activity_display_pane.layout_widgets(layout)

    def build_graph(self, layout):
        self.graph_pane.layout_widgets(layout)

    def build_research_pane(self, layout):
        self.research_pane.build_research_pane(layout)

    def shut_down(self):
        self.activity_controller_pane.resolve()
        self.activity_display_pane.stop_display()
        self.graph_pane.stop_graph()

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