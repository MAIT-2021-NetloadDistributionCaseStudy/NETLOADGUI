import os
import sys
import pandas as pd
#import pandastable
from tabulate import tabulate

import matplotlib
matplotlib.use('Qt5Agg') # Import the backend
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import PyQt5
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QTableView, QDialog, QWidget, QLabel, QFrame
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QSizePolicy, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem, QFormLayout, QHeaderView, QTextEdit
from PyQt5.QtCore import Qt
from pyqtgraph import PlotWidget

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
      self.resultTextEdit = QTextEdit()
      self.resultTextEdit.setFixedSize(1000, 300)

      # Create the content frame
      content_frame = QtWidgets.QFrame()
      content_frame.setStyleSheet("background-color: white;")
      content_frame.setFixedHeight(500)

      # Create the content label
      content_label = QtWidgets.QLabel('Select a directory to import CSV files')
      content_label.setFont(QtGui.QFont('Arial', 14))
      content_label.setAlignment(QtCore.Qt.AlignCenter)       
        
      # Create the directory label
      self.directory_label = QtWidgets.QLabel()
      self.directory_label.setAlignment(QtCore.Qt.AlignCenter)
       
      button_size = QtCore.QSize(300, 30)
      switch_size = QtCore.QSize(150, 30)

      # Create the import button
      import_button = QtWidgets.QPushButton('Import CSV File')
      import_button.setFixedSize(button_size)
      import_button.setStyleSheet('QPushButton {background-color: grey}')
      import_button.clicked.connect(self.import_file)

      # Create the buttons for displaying the graphs
      protocol_button = QPushButton('Protocol Based')
      protocol_button.setFixedSize(button_size)
      protocol_button.setStyleSheet('QPushButton {background-color: grey}')
      protocol_button.clicked.connect(self.display_protocol_graphs)

      port_button = QPushButton('Port Based')
      port_button.setFixedSize(button_size)
      port_button.setStyleSheet('QPushButton {background-color: grey}')
      port_button.clicked.connect(self.display_port_graphs)
       
      # graph_layout = QtWidgets.QVBoxLayout()
      graph_label = QLabel('Choose the analysis method to display the trend')
      graph_label.setFont(QtGui.QFont('Arial', 13))
      graph_label.setAlignment(QtCore.Qt.AlignCenter)
        
      source_dest_label = QLabel('On the basis of Source and Destination')
      source_dest_label.setFont(QtGui.QFont('Arial', 11))
      source_dest_label.setAlignment(QtCore.Qt.AlignCenter)
      

      # Define the body frame
      body_frame = QtWidgets.QFrame()
      body_frame.setStyleSheet("background-color: #34495e;")
      body_frame.setFixedHeight(100)
        
      # Add widgets to the content frame
      content_layout = QVBoxLayout(content_frame)
      content_layout.addWidget(content_label)
      content_layout.addWidget(self.directory_label)
      content_layout.addWidget(import_button, alignment=QtCore.Qt.AlignCenter)
      content_layout.addSpacing(20)
      content_layout.addWidget(graph_label)
      content_layout.addSpacing(20)
      content_layout.addWidget(protocol_button, alignment=QtCore.Qt.AlignCenter)
      content_layout.addWidget(port_button, alignment=QtCore.Qt.AlignCenter)

        
      # Create a QHBoxLayout for the ip and mac buttons
      mac_ip_layout = QHBoxLayout()
      mac_button = QPushButton('mac address')
      mac_button.setFixedSize(switch_size)
      mac_button.setStyleSheet('QPushButton {background-color: grey}')
      mac_button.clicked.connect(self.display_source_dest_mac_graphs)
       
      Ip_button = QPushButton('Ip address')
      Ip_button.setFixedSize(switch_size)
      Ip_button.setStyleSheet('QPushButton {background-color: grey}')
      Ip_button.clicked.connect(self.display_source_dest_ip_graphs)
        
      mac_ip_layout.addWidget(mac_button)
      mac_ip_layout.addWidget(Ip_button)
        
      # content_layout.addWidget(source_dest_button, alignment=QtCore.Qt.AlignCenter)
      content_layout.addWidget(source_dest_label)
      content_layout.addLayout(mac_ip_layout)
      content_layout.addWidget(self.resultTextEdit)

      # Add widgets to the body frame
      label = QtWidgets.QLabel('Welcome to Netload Distribution Case Study')
      label.setFont(QtGui.QFont('Arial', 24))
      label.setStyleSheet("color: white;")
      label.setAlignment(QtCore.Qt.AlignCenter)
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
        
        from PyQt5.QtWidgets import QDesktopWidget

        # Set the window size and center it on the screen
        screen_geometry = QDesktopWidget().availableGeometry()
        self.table_window.setGeometry(
            screen_geometry.width() / 2 - 400,
            screen_geometry.height() / 2 - 300,
            800, 600)

        # Show the window
        self.table_window.show()

    def display_graphs(self):
        # Display the protocol, port, and source-destination graphs
        self.display_protocol_graphs()
        self.display_port_graphs()
        self.display_source_dest_mac_graphs()
        self.display_source_dest_ip_graphs()

    def display_protocol_graphs(self):
        
        file_path, _ = QFileDialog.getOpenFileName(self, 'Import File', '', 'CSV Files (*.csv);;Excel Files (*.xlsx)')
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return
        
        # Count protocol
        protocol_counts = df.groupby('Protocol').size().reset_index(name='count')
        # The mean time taken by each protocol in the dataframe
        protocol_time = df.groupby(['Protocol'])['Time'].mean().reset_index(name='mean_time')
        protocol_time = protocol_time.sort_values(by='mean_time', ascending=False)
        # Merge the two dataframes based on 'Protocol' column
        result = pd.merge(protocol_counts, protocol_time, on='Protocol')
        
        result_text = tabulate(result, headers='keys', tablefmt='orgtbl')
        self.resultTextEdit.setPlainText(result_text)
      
        import matplotlib.pyplot as plt
        
        # Define the figure and axis objects
        fig, ax1 = plt.subplots()
          
        # Plot the count data on the first axis
        ax1.bar(result['Protocol'], result['count'], color='b')
        ax1.set_ylabel('Count', color='b')
        ax1.tick_params(axis='y', labelcolor='b')
        
        # Create a second axis that shares the same x-axis as the first axis
        ax2 = ax1.twinx()
        
        # Plot the mean time data on the second axis
        ax2.plot(result['Protocol'], result['mean_time'], color='r', marker='o')
        ax2.set_ylabel('Mean Time', color='r')
        ax2.tick_params(axis='y', labelcolor='r')

        # Set the x-axis tick labels vertically
        plt.xticks(rotation=90)
        
         # Create a new window to display the graph
        graph_window = QDialog(self)
        graph_window.setWindowTitle('Netload Graph')
        graph_window.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        # Embed the graph in the Qt window using FigureCanvasQTAgg
        canvas = FigureCanvasQTAgg(fig)
        graph_window.setLayout(QVBoxLayout())
        graph_window.layout().addWidget(canvas)

        # Show the window
        graph_window.exec_()
        # Close the previous figure to avoid displaying it in the Python output
        plt.close(fig)
        

    def display_port_graphs(self):
        
        import matplotlib.pyplot as plt
        
        file_path, _ = QFileDialog.getOpenFileName(self, 'Import File', '', 'CSV Files (*.csv);;Excel Files (*.xlsx)')
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return

        # Group the data by Reception Port and calculate the number of packets and bytes sent between each group
        grouped = df.groupby(['Reception Port'])
        load = grouped.agg({'Length': 'mean', 'Protocol': 'count'}).reset_index()
        load = load.rename(columns={'Protocol': 'Packets', 'Length': 'Bytes'})

        # Group the DataFrame by Reception Port and calculate the mean of the Time column
        time_delay_Port = df.groupby('Reception Port')['Time'].mean()

        # Find the port with the highest netload and time delay
        highest_netload_port = load.loc[load['Bytes'].idxmax()]['Reception Port']
        highest_time_delay_port = time_delay_Port.idxmax()

        # Print the information for the highest netload and time delay
        netload_rate_text = f"Highest netload on port {highest_netload_port}: {load['Bytes'].mean()} bytes"
        time_delay_text = f"Highest time delay on port {highest_time_delay_port}: {time_delay_Port.mean()} seconds"
        
        # Set the result text in the GUI
        result_text = f"{netload_rate_text}\n{time_delay_text}"
        self.resultTextEdit.setPlainText(result_text)

        # create subplots for netload and time delay
        fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

        # create bar chart for netload
        ax1.bar(load['Reception Port'], load['Bytes'])
        ax1.set_xlabel('Port Number')
        ax1.set_ylabel('Netload')
        ax1.set_title('Netload on the basis of port')
        ax1.set_xticks(range(0, 4))  # set the xticks to range from 1 to 4

        # create bar chart for time delay
        ax2.bar(time_delay_Port.index, time_delay_Port.values)
        ax2.set_xlabel('Port Number')
        ax2.set_ylabel('Time Delay')
        ax2.set_title('Time Delay on the basis of port')
        ax2.set_xticks(range(0, 4))  # set the xticks to range from 1 to 4

        # Create a new window to display the graph
        graph_window = QDialog(self)
        graph_window.setWindowTitle('Netload Graph')
        graph_window.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        # Embed the graph in the Qt window using FigureCanvasQTAgg
        canvas = FigureCanvasQTAgg(fig)
        graph_window.setLayout(QVBoxLayout())
        graph_window.layout().addWidget(canvas)

        # Show the window
        graph_window.exec_()
        # Close the previous figure to avoid displaying it in the Python output
        plt.close(fig)
        
    def display_source_dest_mac_graphs(self):
        
        import pandas as pd
        import matplotlib.pyplot as plt
        
        file_path, _ = QFileDialog.getOpenFileName(self, 'Import File', '', 'CSV Files (*.csv);;Excel Files (*.xlsx)')
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return

        # Filter the DataFrame to only include source-destination pairs starting with "Siemens_"
        df_siemens = df[df['Source'].str.startswith('Siemens_')]

        # Group the filtered DataFrame by source and destination, and aggregate by mean
        gb = df_siemens.groupby(["Source", "Destination"]).agg({"Length": "mean", "Time": "mean"})

        # Calculate the source-destination pair with the highest netload rate
        highest_netload_rate_pair = gb.loc[gb["Length"].idxmax()]
        netload_rate_text = f"Highest netload rate pair: {highest_netload_rate_pair.name}, Netload rate: {highest_netload_rate_pair['Length']:.2f} bytes/s"

        # Calculate the source-destination pair with the highest time delay
        highest_time_delay_pair = gb.loc[gb["Time"].idxmax()]
        time_delay_text = f"Highest time delay pair: {highest_time_delay_pair.name}, Time delay: {highest_time_delay_pair['Time']:.6f} s"

         # Set the result text in the GUI
        result_text = f"{netload_rate_text}\n{time_delay_text}"
        self.resultTextEdit.setPlainText(result_text)
        
        # Create a figure with 1 row and 2 columns
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,5))
        fig.subplots_adjust(bottom=0.3)

        # Plot the bytes transferred on the first subplot
        gb["Length"].plot(kind="bar", ax=ax1)
        ax1.set_ylabel("Bytes Transferred")

        # Plot the total time on the second subplot
        gb["Time"].plot(kind="bar", ax=ax2)
        ax2.set_ylabel("Total Time (s)")

        # Set the title for the figure
        fig.suptitle('Data capture at two different points without external load')

        # Create a new window to display the graph
        graph_window = QDialog(self)
        graph_window.setWindowTitle('Netload Graph')
        graph_window.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        # Embed the graph in the Qt window using FigureCanvasQTAgg
        canvas = FigureCanvasQTAgg(fig)
        graph_window.setLayout(QVBoxLayout())
        graph_window.layout().addWidget(canvas)

        # Show the window
        graph_window.exec_()
        # Close the previous figure to avoid displaying it in the Python output
        plt.close(fig)
    
    def display_source_dest_ip_graphs(self):
        
        import pandas as pd
        import matplotlib.pyplot as plt
        
        file_path, _ = QFileDialog.getOpenFileName(self, 'Import File', '', 'CSV Files (*.csv);;Excel Files (*.xlsx)')
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return
        # Filter the DataFrame to only include source-destination pairs that don't start with Siemens_
        filtered_df = df[~df["Source"].str.startswith("Siemens_")]

        # Group the filtered DataFrame by source and destination, and aggregate by mean
        gb = filtered_df.groupby(["Source", "Destination"]).agg({"Length": "mean", "Time": "mean"})

        # Calculate the source-destination pair with the highest netload rate
        highest_netload_rate_pair = gb.loc[gb["Length"].idxmax()]
        netload_rate_text = f"Highest netload rate pair: {highest_netload_rate_pair.name}, Netload rate: {highest_netload_rate_pair['Length']:.2f} bytes/s"

        # Calculate the source-destination pair with the highest time delay
        highest_time_delay_pair = gb.loc[gb["Time"].idxmax()]
        time_delay_text = f"Highest time delay pair: {highest_time_delay_pair.name}, Time delay: {highest_time_delay_pair['Time']:.6f} s"

        # Set the result text in the GUI
        result_text = f"{netload_rate_text}\n{time_delay_text}"
        self.resultTextEdit.setPlainText(result_text)
        
        # Create a figure with 1 row and 2 columns
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,5))
        fig.subplots_adjust(bottom=0.3)

        # Plot the bytes transferred on the first subplot
        gb["Length"].plot(kind="bar", ax=ax1)
        ax1.set_ylabel("Bytes Transferred")

        # Plot the total time on the second subplot
        gb["Time"].plot(kind="bar", ax=ax2)
        ax2.set_ylabel("Total Time (s)")

        # Set the title for the figure
        fig.suptitle('Data capture at two different points without external load')
        
        # Create a new window to display the graph
        graph_window = QDialog(self)
        graph_window.setWindowTitle('Netload Graph')
        graph_window.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowMaximizeButtonHint)

        # Embed the graph in the Qt window using FigureCanvasQTAgg
        canvas = FigureCanvasQTAgg(fig)
        graph_window.setLayout(QVBoxLayout())
        graph_window.layout().addWidget(canvas)

        # Show the window
        graph_window.exec_()
        # Close the previous figure to avoid displaying it in the Python output
        plt.close(fig)

