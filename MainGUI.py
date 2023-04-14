from operator import sub
import pandas as pd
import numpy as np
import os
import sys
#import pandastable

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

from Group1 import Page as Group1
from Group2 import Page as Group2
import PyQt5
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *#,QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QTableView, QDialog, QWidget, QLabel, QFrame
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QSizePolicy, QMessageBox
from PyQt5.QtCore import Qt


class MainWindow(QWidget):
    def __init__(self):
      super().__init__()
      self.df = None
      self.setWindowTitle('Netload Distribution in Converged Networks')
      self.setGeometry(200, 200, 1000, 800)
      self.UI()

    def UI(self):
      self.table_window = QWidget()
      self.tab1=QWidget()
      self.page1=Group1()
      self.page1.UI(self)
      self.tab2=QWidget()
      self.page2=Group2()
      self.page2.UI(self)
      self.tabs =QTabWidget()
      self.tabs.addTab(self.tab1,"Group 1 Analysis")
      self.tabs.addTab(self.tab2,"Group 2 Analysis")
      main_layout = QVBoxLayout(self)
      
    # Create the header frame
      header_frame = QtWidgets.QFrame()
      header_frame.setStyleSheet("background-color: #2c3e50;")
      header_frame.setFixedHeight(100)

      # Create the header label
      header_label = QtWidgets.QLabel('Netload Distribution in Converged Networks')
      header_label.setFont(QtGui.QFont('Arial', 24))
      header_label.setStyleSheet("color: white;")
      header_label.setAlignment(QtCore.Qt.AlignCenter)

      # Add the header label to the header frame
      header_layout = QVBoxLayout(header_frame)
      header_layout.addWidget(header_label)

      # Add the header frame to the main layout
      main_layout.addWidget(header_frame)
      
      #self.tab1.setLayout(self.main1)
      main_layout.addWidget(self.tabs)
      self.setLayout(main_layout)
      self.show()


if __name__ == "__main__":
    # Create the application
    app = QApplication(sys.argv)

    # Create the main window
    window = MainWindow()

    # Show the main window
    window.show()

    # Run the event loop
    sys.exit(app.exec_())
