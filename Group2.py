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
      import_button2=QPushButton('Import packets')
      import_button2.clicked.connect(self.import_file)

      #self.check1=QRadioButton('Plot Cycle Times')
      #self.check2=QRadioButton('Calculate Delay of Packets within the Test setup')
      srcLabel=QLabel('Choose Source Filter')
      portA_Label=QLabel('Choose Port A')
      portB_Label=QLabel('Choose Port B')
      self.portA=QComboBox()
      self.portB=QComboBox()
      self.source=QComboBox()


      self.cal=QPushButton('Calculate Packet delay in-between selected ports')
      self.cal.clicked.connect(self.calcAvgDelay)
      self.calcLabel=QLabel('Average Delay: ')
      self.calc=QLabel()
      self.calc.setStyleSheet("background-color: white")
      self.clear=QPushButton('Clear current packets')
      self.addNew=QPushButton('Import New Packets')



      self.main2=QVBoxLayout()
      subMain=QHBoxLayout()
      topLeft=QFormLayout()
      topRight=QFormLayout()
      topLeft.addRow(import_button2)
      topLeft.addRow(srcLabel,self.source)
      topLeft.addRow(portA_Label,self.portA)
      topLeft.addRow(portB_Label,self.portB)
      topRight.addRow(self.cal)
      topRight.addRow(self.calcLabel,self.calc)
      topRight.addRow(self.clear,self.addNew)
      subMain.addLayout(topLeft)
      subMain.addLayout(topRight)
      #self.main2.addWidget(import_button2)
      self.main2.addLayout(subMain)


      window.tab2.setLayout(self.main2)

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

      
      
    def display_csv_table(self,df):
      # Create a new window to display the table
      self.table_window = QWidget()
      self.table_window.setWindowTitle('CSV Table')
      self.table_window.setGeometry(100, 100, 800, 600)

      # Create a layout for the window
      layout = QVBoxLayout()
      screen_geometry = QDesktopWidget().availableGeometry()
      # Create a PandasTable widget
        
      
      arr1=df['Source'].unique()
      arr2=df['Reception Port'].unique()
      for a in arr1:
        self.source.addItem(str(a))
      
      for b in arr2:
        self.portA.addItem(str(b))
        self.portB.addItem(str(b))
      table = PandasTable(df)
      self.main2.addWidget(table)

    def calcAvgDelay(self):
      #def cal(data,portA,portB):
        data=self.df
        data.set_index('No.', inplace=True)
        df=data[data['Protocol'] == 'PNIO']
        src=self.source.currentText()
        prtA=self.portA.currentText()
        prtB=self.portB.currentText()
        data1 = df[(df['Reception Port'] == int(prtA)) & (df['Source']==src) ]
        data2 = df[(df['Reception Port'] == int(prtB)) & (df['Source']==src) ]
        count=data2['Time'].count()
        val1=[]

        for i in range(0,count):
            r1=data1.iloc[[i],[6]].values
            r2=data2.iloc[[i],[6]].values

            x=str(r1)
            x1=x[30:41]
            y=str(r2)
            y1=y[30:41]
            if x1 == y1:
                delta=data1.iloc[[i]]["Time"].values
                delta2=data2.iloc[[i]]["Time"].values
                l=delta2-delta
                val1.append(l[0])
        
        self.avg=sum(val1) / len(val1)
        #print(self.avg)
        self.calc.setText(str(self.avg))