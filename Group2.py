from PyQt5 import QtWidgets, QtGui, QtCore

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

        # Create a layout for the self.table view
        layout = QVBoxLayout(self)

        # Create a standard item model for the self.table view
        model = QStandardItemModel(self)

        # Set the headers of the self.table view
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

        # Create the self.table view and set its model
        table_view = QTableView(self)
        table_view.setModel(model)
        layout.addWidget(table_view)
        self.setLayout(layout)
class Page(QWidget):

    def UI(self,window:QWidget):
        self.df = None
        import_button2=QPushButton('Import packets')
        import_button2.setStyleSheet('QPushButton {background-color: grey}')
        import_button2.setFixedWidth(500)
        import_button2.clicked.connect(self.import_file)
        button_size = QtCore.QSize(350, 30)
        label_size = QtCore.QSize(140, 30)
        #self.check1=QRadioButton('Plot Cycle Times')
        #self.check2=QRadioButton('Calculate Delay of Packets within the Test setup')
        srcLabel=QLabel('Choose Source Device')
        srcLabel.setFixedSize(label_size)
        srcLabel.setFont(QtGui.QFont('Arial',10,2))
        portA_Label=QLabel('Choose Port A')
        portA_Label.setFixedSize(label_size)
        portA_Label.setFont(QFont('Arial',10,2))
        portB_Label=QLabel('Choose Port B')
        portB_Label.setFixedSize(label_size)
        portB_Label.setFont(QFont('Arial',10,2))

        self.portA=QComboBox()
        self.portA.setFixedSize(button_size)
        self.portA.setFont(QFont('Arial',13,2))

        self.portB=QComboBox()
        self.portB.setFixedSize(button_size)
        self.portB.setFont(QFont('Arial',13,2))

        self.source=QComboBox()
        self.source.setFixedSize(button_size)
        self.source.setFont(QFont('Arial',13,2))

        self.source.currentTextChanged.connect(self.choosePorts)


        self.cal=QPushButton('Calculate Packet delay in-between selected ports')
        self.cal.setStyleSheet('QPushButton {background-color: grey}')

        self.cal.setFixedSize(button_size)
        self.cal.clicked.connect(self.calcAvgDelay)
        self.plot=QPushButton('View Plots')
        self.plot.setFixedSize(button_size)
        self.plot.setStyleSheet('QPushButton {background-color: grey}')
        self.plot.clicked.connect(self.viewPlots)

        
        self.calcLabel=QLabel('Average Delay (s): ')
        self.calcLabel.setFont(QtGui.QFont('Arial',13,2,1))
        self.calc=QLabel()
        self.calc.setFont(QtGui.QFont('Arial', 13,5))
        self.calc.setStyleSheet("background-color: white;")
        #self.label_1.setStyleSheet("")
        self.calcLabel2=QLabel('Average IP traffic (Byte): ')
        self.calcLabel2.setFont(QtGui.QFont('Arial',13,2,1))
        self.calc2=QLabel()
        self.calc2.setFont(QtGui.QFont('Arial', 13,5))
        self.calc2.setStyleSheet("background-color: white;")



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
        topRight.addRow(self.calcLabel2,self.calc2)
        topRight.addRow(self.plot)
        
        subMain.addLayout(topLeft)
        subMain.addLayout(topRight)
        #self.main2.addWidget(import_button2)
        self.main2.addLayout(subMain)

        window.tab2.setLayout(self.main2)

    def import_file(self):
      #global df
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
        # Create a new window to display the self.table
        self.table_window = QWidget()
        self.table_window.setWindowTitle('CSV Table')
        self.table_window.setGeometry(100, 100, 800, 600)

        # Create a layout for the window
        layout = QVBoxLayout()
        screen_geometry = QDesktopWidget().availableGeometry()
        # Create a PandasTable widget
            
        
        arr1=df['Source'].unique()
        self.source.clear()
        self.calc.setText("")
        self.calc2.setText("")
        for a in arr1:
            self.source.addItem(str(a))
        
        
        
        try:
            self.table.setParent(None)
        except:
            pass
        
        self.table = PandasTable(df)
        try:
            self.main2.addWidget(self.table)
            self.choosePorts()
        except Exception as e:
            print(e)
            



    def choosePorts(self):
        try:

            self.portA.clear()
            self.portB.clear()

            df=self.df.copy()
            filtered_df=df[(df['Source']==self.source.currentText())]
            arr=filtered_df['Reception Port'].unique()
            for a in arr:
                self.portA.addItem(str(a))
                self.portB.addItem(str(a))
            self.cal.setEnabled(True)
            self.plot.setEnabled(True)
        except:
            mbox=QMessageBox.warning(self,"Warning ","Imported Packets don't include Reception Port information")
            self.cal.setEnabled(False)
            self.plot.setEnabled(False)
    def calcAvgDelay(self):
      #def cal(data,portA,portB):
        try:
            data=self.df.copy()
            data.set_index('No.', inplace=True)
            df=data[data['Protocol'] == 'PNIO']
            src=self.source.currentText()
            prtA=self.portA.currentText()
            prtB=self.portB.currentText()
            data1 = df[(df['Reception Port'] == int(prtA)) & (df['Source']==src) ]
            data2 = df[(df['Reception Port'] == int(prtB)) & (df['Source']==src) ]
            count=data2['Time'].count()
            val1=[]
            length=[]


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
                    l_abs=abs(l[0])

                    if l[0] < 0:
                        port=prtB
                        s=data2.iloc[[i]].index.values
                        f=data1.iloc[[i]].index.values
                    else:
                        port=prtA
                        s=data1.iloc[[i]].index.values
                        f=data2.iloc[[i]].index.values
                    
                    newFrame=data[s[0]:f[0]]
                    tcpFrame=newFrame[(newFrame['Reception Port'] == int(port)) ]
                    x=tcpFrame['Length'].sum()
                    length.append(x)
                    val1.append(l_abs)
            
            self.avg=sum(val1) / len(val1)
            self.avg2=sum(length) / len(length)
            #print(self.avg)
            self.calc.setText(str(self.avg))
            self.calc2.setText(str(self.avg2))

            self.val=val1
            self.length=length
        except Exception as e:
            print(e)
    
    
    def calcCycleTime(self):
      
        d=self.df.copy()
        d.head(5)
        d.set_index('No.', inplace=True)
        d.head(5)
        prtA=self.portA.currentText()
        datax=d[d['Reception Port'] == int(prtA)]
        datax.head(5)
        count=datax['Time'].count()
        #print(count)
        
        flag=1
        deltas=[]
        
        for i in range(0,count):
            #print(datax.iloc[[i],[3]].values)
            if ((datax.iloc[[i],[3]].values == 'PNIO') & (flag==1)):
                time1=datax.iloc[[i],[0]].values
                flag=0
                #print(time1)
            elif ((datax.iloc[[i],[3]].values == 'PNIO') & (flag==0)):
                time2=datax.iloc[[i],[0]].values
                delta=time2[0]-time1[0]
                #print(time2)
                deltas.append(delta[0])
                flag=1
        
        #print(deltas[0:5])
        avgCycleTime=sum(deltas) / len(deltas)
        self.avgCycleTime.setText(str(avgCycleTime))
        self.deltas=deltas
        #print(self.deltas)
        
    def viewPlots(self):
        fig, ax1 = plt.subplots()

        color = 'tab:red'
        ax1.set_xlabel('Packet')
        ax1.set_ylabel('Delay between Ports-(s)', color=color,fontsize=15)
        ax1.plot(range(0,len(self.val)),self.val, color=color)
        ax1.tick_params(axis='y', labelcolor=color,labelsize=12)
        ax1.set_title('Packet Delays alongside IP traffic')
        ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

        color = 'tab:blue'
        ax2.set_ylabel('TCP Packet lengths-(Bytes)', color=color,fontsize=15)  # we already handled the x-label with ax1
        ax2.plot(range(0,len(self.length)), self.length, color=color, linestyle=':')
        ax2.tick_params(axis='y', labelcolor=color,
                        labelsize=12)

        #fig.tight_layout()  # otherwise the right y-label is slightly clipped
        graph_window = QDialog(self)
        graph_window.setWindowTitle('Graphs')
        # Embed the graph in the Qt window using FigureCanvasQTAgg
        canvas = FigureCanvasQTAgg(fig)


        
        graph_window.setLayout(QVBoxLayout())
        graph_window.layout().addWidget(canvas)
       # graph_window.layout().addWidget(canvas2)
        screen_geometry = QDesktopWidget().availableGeometry()
        graph_window.setGeometry(
            screen_geometry.width() / 2 - 400,
            screen_geometry.height() / 2 - 300,
            1000, 600)

        #graph_window.layout().addWidget(AvgLabel)

        # Show the window
        graph_window.exec_()
        
        # Close the previous figure to avoid displaying it in the Python output
        plt.close(fig)

