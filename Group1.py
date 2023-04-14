from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QStandardItemModel, QStandardItem

import pandas as pd
import numpy as np
import os
import sys

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class PandasTable(QWidget):
    def __init__(self, df):
        super().__init__()

        # Create a layout for the table view
        layout = QVBoxLayout(self)

        # Create a standard item model for the table view
        model = QStandardItemModel(self)

        # Set the headers of the table view
        headers = df.columns.tolist()
        model.setHorizontalHeaderLabels(headers)

        # Populate the model with the data from the DataFrame
        for i, row_data in df.iterrows():
            row = []
            for item in row_data.tolist():
                cell = QStandardItem(str(item))
                cell.setTextAlignment(Qt.AlignCenter)
                row.append(cell)
            model.appendRow(row)

        # Create the table view and set its model
        table_view = QTableView(self)
        table_view.setModel(model)
        layout.addWidget(table_view)
        self.setLayout(layout)

class Page(QWidget):

    def UI(self,window:QWidget):
      self.df = None

       # Create the content frame
      content_frame = QFrame()
      content_frame.setStyleSheet("background-color: white;")
      content_frame.setFixedHeight(200)

      # Create the content label
      content_label = QLabel('Select a directory to import CSV files')
      content_label.setFont(QFont('Arial', 14))
      content_label.setAlignment(Qt.AlignCenter)

      # Create the directory label
      self.directory_label = QLabel()
      self.directory_label.setAlignment(Qt.AlignCenter)

      # Create the import button
      import_button = QPushButton('Import CSV File')
      import_button.clicked.connect(self.import_file)
      # Create the button to display the graphs
      display_button = QPushButton('Display Graphs')
      display_button.clicked.connect(self.display_graphs)
      # Define the body frame
      body_frame = QFrame()
      body_frame.setStyleSheet("background-color: #34495e;")
      body_frame.setFixedHeight(100)
# Add widgets to the content frame
      content_layout = QVBoxLayout(content_frame)
      content_layout.addWidget(content_label)
      content_layout.addWidget(self.directory_label)
      content_layout.addWidget(import_button)
      content_layout.addWidget(display_button)

      label = QLabel('Welcome to Netload Distribution Case Study')
      label.setFont(QFont('Arial', 24))
      label.setStyleSheet("color: white;")
      label.setAlignment(Qt.AlignCenter)
      body_layout = QVBoxLayout(body_frame)
      body_layout.addWidget(label)
      self.main1=QVBoxLayout()
      self.main1.addWidget(content_frame)
      self.main1.addWidget(body_frame)
      window.tab1.setLayout(self.main1)

    def import_file(self):
        global df
        file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "CSV Files (*.csv);; Excel Files (*.xlsx)")
        if file_path.endswith('.csv'):
            self.df = pd.read_csv(file_path)

            # Display the CSV file in a new window using PandasTable
            self.display_csv_table(self.df)

        elif file_path.endswith('.xlsx'):
            self.df = pd.read_excel(file_path)
        else:
            return

        self.directory_label.setText(file_path)
        
    def display_csv_table(self,df):
        # Create a new window to display the table
        self.table_window = QWidget()
        self.table_window.setWindowTitle('CSV Table')
        self.table_window.setGeometry(100, 100, 800, 600)

        # Create a layout for the window
        layout = QVBoxLayout()

        # Create a PandasTable widget
        table = PandasTable(df)

        # Add the PandasTable widget to the layout
        layout.addWidget(table)

        # Set the layout for the window
        self.table_window.setLayout(layout)
        
        # Set the window size and center it on the screen
        screen_geometry = QDesktopWidget().availableGeometry()
        self.table_window.setGeometry(
            screen_geometry.width() / 2 - 400,
            screen_geometry.height() / 2 - 300,
            800, 600)

        # Show the window
        self.table_window.show()

    def display_graphs(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Import File', '', 'CSV Files (*.csv);;Excel Files (*.xlsx)')
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return

        # Create a new window to display the graph
        graph_window = QDialog(self)
        graph_window.setWindowTitle('Netload Graph')

        self.df = self.df.rename(columns={'Length': 'Bytes'})

        #group the data by port number, and calculate the number of packets and bytes sent between each group
        grouped = self.df.groupby(['Reception Port'])
        load = grouped['Bytes'].sum().reset_index()

        fig = plt.figure(figsize=(8, 6))
        plt.bar(load['Reception Port'], load['Bytes'])
        plt.xlabel('Reception Port')
        plt.ylabel('Bytes')
        plt.title('Delay observed in each port of Net Analyzer in Profinet based setup')

        # Embed the graph in the Qt window using FigureCanvasQTAgg
        canvas = FigureCanvasQTAgg(fig)
        graph_window.setLayout(QVBoxLayout())
        graph_window.layout().addWidget(canvas)

        # Show the window
        graph_window.exec_()
        
        # Close the previous figure to avoid displaying it in the Python output
        plt.close(fig)



if __name__=='__main__':
    # st=Page()
    # Page()
    # st.UI()
    pass