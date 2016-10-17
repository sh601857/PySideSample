#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import sqlite3
from pathlib import Path
from PySide import QtCore
from PySide import QtGui
import AppProject

class SimSpecWidget(QtGui.QWidget):

    def __init__(self):
        super(SimSpecWidget, self).__init__()     
        self.initUI()

    def initUI(self): 
                  
        self.spbNColum = QtGui.QSpinBox()
        self.spbNColum.setRange(1,10)
        self.spbNColum.setValue(5) 
        self.ckShowSimtor = QtGui.QCheckBox(self.tr("Show simulator window during sampling"))

        hl1 =  QtGui.QHBoxLayout()
        hl1.addWidget(QtGui.QLabel(self.tr("Number of distillation columns:")) )
        hl1.addWidget(self.spbNColum)
        hl1.addWidget(self.ckShowSimtor)

        self.tvCDUName = QtGui.QTableView()
        self.smCDUName = QtGui.QStandardItemModel(self.tvCDUName)
        self.smCDUName.setColumnCount(4)
        self.smCDUName.setHorizontalHeaderLabels(['Name','Name in Unisim','Active?','Simulation Order'])
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

        saveBtn.clicked.connect(self.save)
        self.loadData()

    def loadData(self):

        if( self.smCDUName.rowCount() >0 ):
            self.smCDUName.removeRows(0, self.smCDUName.rowCount() )
        
        appPro = AppProject.AppProject()        
        dbFile =  appPro.getDBPath('CDUSpec.db')  

        if not Path( dbFile ).exists():           
            return
        
        conn = sqlite3.connect(dbFile)
        cursor = conn.cursor()
        try:
            for row in cursor.execute('SELECT Name,UnisimName,Acitive,SimNo FROM CUDNAMES ORDER BY SimNo'):
                itemrow =[]
                itemrow.append( QtGui.QStandardItem(row[0]) )
                itemrow.append( QtGui.QStandardItem(row[1]) )
                itemrow.append( QtGui.QStandardItem() )
                itemrow.append( QtGui.QStandardItem() )              
                itemrow[2].setCheckable(True)
                itemrow[2].setCheckState( QtCore.Qt.CheckState.Checked if row[2]  ==1 else QtCore.Qt.CheckState.Unchecked )
                itemrow[2].setEditable(False)
                itemrow[3].setData( row[3], QtCore.Qt.EditRole )
                self.smCDUName.appendRow( itemrow )
        except:
            pass       
        conn.close() 

    @QtCore.Slot()
    def save(self):

        appPro = AppProject.AppProject()        
        dbFile =  appPro.getDBPath('CDUSpec.db')       
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
        sql = "INSERT INTO CUDNAMES VALUES (?, ?, ?, ?)"        

        recs=[]
        for r in range( self.smCDUName.rowCount() ):
            rowlist=[]
            rowlist.append( self.smCDUName.item(r,0).data(QtCore.Qt.EditRole ) )
            rowlist.append( self.smCDUName.item(r,1).data(QtCore.Qt.EditRole ) )
            rowlist.append( 1 if self.smCDUName.item(r,2).data(QtCore.Qt.CheckStateRole) == QtCore.Qt.Checked  else 0 )
            rowlist.append( self.smCDUName.item(r,3).data(QtCore.Qt.EditRole ) )
            recs.append( tuple(rowlist) )

        cursor.executemany(sql,recs)
        conn.commit()			
        conn.close()   

        msgBox = QtGui.QMessageBox()
        msgBox.setText("The document has been Saved.")
        msgBox.exec_()        
        pass