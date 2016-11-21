#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import sqlite3
#from sqlalchemy import create_engine
from pathlib import Path
import shutil
import pandas as PD
import numpy
from PySide import QtCore
from PySide import QtGui
import AppProject

class CDUModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super(CDUModel, self).__init__()
        self.tableHeaderNames = ['Name','Name in Unisim','Active?','Simulation Order']
        self.cduData = PD.DataFrame(columns= self.tableHeaderNames )
        
    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.cduData)

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.tableHeaderNames)
    
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if index.isValid() == False:
            return None #QVariant()
        if role == QtCore.Qt.DisplayRole:
            if index.column() != 2:
                return str(self.cduData.iloc[index.row(),index.column()] )
        elif role == QtCore.Qt.EditRole:
            return ( self.cduData.iloc[index.row(),index.column()] )
        elif role == QtCore.Qt.CheckStateRole:
            if index.column() == 2:
                return QtCore.Qt.Checked if self.cduData.iloc[index.row(),index.column()] ==1 else QtCore.Qt.Unchecked
        elif role == QtCore.Qt.ForegroundRole:
            if self.flags(index) & QtCore.Qt.ItemIsEditable :             
                return QtGui.QBrush( QtGui.QColor('#0000FF') )
        else:
            return None #QVariant()

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.CheckStateRole :
            self.cduData.iloc[index.row(),index.column()] = 1 if value == QtCore.Qt.Checked else 0
        if role == QtCore.Qt.EditRole :
            if index.column() == 0:
                self.cduData.iloc[index.row(),index.column()] = value
            elif index.column() == 3:
                self.cduData.iloc[index.row(),index.column()] = value
        return True

    def flags(self, index):
        if index.column() == 1:
            flag = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled 
        elif index.column() == 2:
            flag = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable
        else:
            flag = QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        return flag
    
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal :
            if role == QtCore.Qt.DisplayRole :
                return self.tableHeaderNames[section]
        else:
            if role == QtCore.Qt.DisplayRole :
                return section+1
        return None
    
    def loadData(self, data ):
        self.beginResetModel()
        self.cduData = data      
        self.endResetModel()
        
class SimSpecWidget(QtGui.QWidget):

    def __init__(self):
        super(SimSpecWidget, self).__init__()     
        self.initUI()

    def initUI(self): 
                  
        #self.spbNColum = QtGui.QSpinBox()
        #self.spbNColum.setRange(1,10)
        #self.spbNColum.setValue(5) 
        self.ckShowSimtor = QtGui.QCheckBox(self.tr("Show simulator window during sampling"))
        self.btnBroseSimFile = QtGui.QPushButton(self.tr("Select Unisim case file"))

        hl1 =  QtGui.QHBoxLayout()
        #hl1.addWidget(QtGui.QLabel(self.tr("Number of distillation columns:")) )
        #hl1.addWidget(self.spbNColum)
        hl1.addWidget(self.btnBroseSimFile)
        hl1.addWidget(self.ckShowSimtor)

        self.tvCDUName = QtGui.QTableView()
        
        self.smCDUName = CDUModel()
        
        self.tvCDUName.setModel(self.smCDUName)
        self.tvCDUDepd = QtGui.QTableView()
        self.smCDUDepd = QtGui.QStandardItemModel(self.tvCDUDepd)
        self.tvCDUDepd.setModel(self.smCDUDepd)

        saveBtn = QtGui.QPushButton(self.tr("Save"))      
        importExcelBtn = QtGui.QPushButton(self.tr("Import from Excel"))
        exportExcelBtn = QtGui.QPushButton(self.tr("Export to Excel"))
        exportUnisimBtn = QtGui.QPushButton(self.tr("Export to Unisim"))

        buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        buttonBox.addButton(saveBtn, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(importExcelBtn, QtGui.QDialogButtonBox.ActionRole) 
        buttonBox.addButton(exportExcelBtn, QtGui.QDialogButtonBox.ActionRole) 
        buttonBox.addButton(exportUnisimBtn, QtGui.QDialogButtonBox.ActionRole) 

        layout =  QtGui.QVBoxLayout()        
        layout.addLayout(hl1)
        layout.addWidget(QtGui.QLabel(self.tr("CDU Names:")) )
        layout.addWidget(self.tvCDUName)
        layout.addWidget(QtGui.QLabel(self.tr("CDU sequence(dependency):")) )
        layout.addWidget(self.tvCDUDepd)
        layout.addStretch()
        layout.addWidget(buttonBox)
        self.setLayout(layout)      
        
        self.btnBroseSimFile.clicked.connect(self.copyUnisimFile) 
        saveBtn.clicked.connect(self.save)
        self.loadData()
        self.tvCDUName.setColumnWidth(0,200)
        self.tvCDUName.setColumnWidth(1,200)
        self.tvCDUName.setColumnWidth(2,100)
        self.tvCDUName.setColumnWidth(3,150)
    def loadData(self):
        
        appPro = AppProject.AppProject()        
        dbFile =  appPro.getPath('DB','CDUSpec.db')  

        if not Path( dbFile ).exists():           
            return
        
        conn = sqlite3.connect(dbFile)
        try:              
            data = PD.read_sql_query('SELECT Name,UnisimName,Acitive,SimNo FROM CUDNAMES ORDER BY SimNo', conn)    
            self.smCDUName.loadData(data)
        except:
            pass       
        conn.close() 
        
    @QtCore.Slot()
    def save(self):

        appPro = AppProject.AppProject()        
        dbFile =  appPro.getPath('DB','CDUSpec.db')       
        conn = sqlite3.connect(dbFile)
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS CUDNAMES')
        cursor.execute("""
        CREATE TABLE  CUDNAMES (
            Name text NOT NULL,
            UnisimName text,
            Acitive INTEGER,
            SimNo INTEGER
            )
        """)        
    
        self.smCDUName.cduData.to_sql('CUDNAMES', conn, index=False, if_exists='append')

        conn.commit()			
        conn.close()   

        msgBox = QtGui.QMessageBox()
        msgBox.setText("The document has been Saved.")
        msgBox.exec_()        
        pass
    
    @QtCore.Slot()
    def copyUnisimFile(self):
        # Get Unisim case file path
        fileName = QtGui.QFileDialog.getOpenFileName( self, self.tr("Select Unisim Case Flei"), "", ("Unisim case Files (*.usc)") ) [0]
        if fileName == '':   # No file selected
            return         
        appPro = AppProject.AppProject()
        simFile =  appPro.getPath('Sim','UnisimCaseFile.usc')
        if simFile == '':    # Project not createed
            return
        shutil.copyfile(fileName, simFile)  # Copy to Sim 
        
        
        
