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
import win32com.client
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
        
class CDUDep(QtCore.QAbstractTableModel):
    def __init__(self,cduModel):
        super(CDUDep, self).__init__()
        self.cduModel = cduModel
        self.depList =[]
        
    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.cduModel.cduData) + 1

    def columnCount(self, parent = QtCore.QModelIndex()):
        return len(self.cduModel.cduData) + 1
    
    def headerData(self, section, orientation, role = QtCore.Qt.DisplayRole):
            return ''
        
    def data(self, index, role = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.CheckStateRole:
            if index.row() == 0 or index.column() ==  0:
                return None
            else:
                cduNames = self.cduModel.cduData['UnisimName'].values
                if (cduNames[index.row()-1],cduNames[index.column()-1]) in self.depList:
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked 
            
        if role == QtCore.Qt.DisplayRole:
            if  index.row() == 0 and index.column() >  0:
                return self.cduModel.cduData.iloc[index.column()-1,0]
            if  index.row() > 0  and index.column() == 0:
                return self.cduModel.cduData.iloc[index.row()-1,0]
            return ''
    
    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.CheckStateRole :
            if index.row() > 0 or index.column() >  0:
                cduNames = self.cduModel.cduData['UnisimName'].values
                if value == QtCore.Qt.Checked :
                    self.depList.append((cduNames[index.row()-1],cduNames[index.column()-1])) 
                else :
                    self.depList.remove((cduNames[index.row()-1],cduNames[index.column()-1]))
            return True       
        return True
        
    def flags(self, index):    
        if index.row() == 0 or index.column() ==  0:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled 
        else :
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable       
        
    def updateCDU(self):
        self.beginResetModel()
        if len(self.cduModel.cduData) > 0 :
            cduNames = self.cduModel.cduData['UnisimName'].values
            for i in range(len(self.depList)-1,-1,-1):
                if not (self.depList[i][0] in cduNames and self.depList[i][1] in cduNames ):
                    del self.depList[i]
        else:
            self.depList=[]
            
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
        self.ckShowSimtor.setChecked(True)
        self.btnBroseSimFile = QtGui.QPushButton(self.tr("Select Unisim case file"))
        self.btnLoadEquip = QtGui.QPushButton(self.tr("Load Columns from Unisim"))
        self.tdSimFile = QtGui.QLineEdit()
        self.tdSimFile.setReadOnly(True)
        hl1 =  QtGui.QHBoxLayout()
        #hl1.addWidget(QtGui.QLabel(self.tr("Number of distillation columns:")) )
        #hl1.addWidget(self.spbNColum)
        hl1.addWidget(self.tdSimFile)
        hl1.addWidget(self.btnBroseSimFile)
        hl1.addWidget(self.ckShowSimtor)
        hl1.addWidget(self.btnLoadEquip)

        self.tvCDUName = QtGui.QTableView()
        
        self.smCDUName = CDUModel()
        
        self.tvCDUName.setModel(self.smCDUName)
        
        self.tvCDUDepd = QtGui.QTableView()
        self.smCDUDepd = CDUDep(self.smCDUName)
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
        layout.addWidget(QtGui.QLabel(self.tr("Column Names:")) )
        layout.addWidget(self.tvCDUName)
        layout.addWidget(QtGui.QLabel(self.tr("Column sequence(dependency): For each column in the rows, check the upstream column")) )
        layout.addWidget(self.tvCDUDepd)
        layout.addStretch()
        layout.addWidget(buttonBox)
        self.setLayout(layout)      
        
        self.btnBroseSimFile.clicked.connect(self.copyUnisimFile) 
        self.btnLoadEquip.clicked.connect(self.loadUnisimEquips) 
        saveBtn.clicked.connect(self.save)
        importExcelBtn.setEnabled(False)
        exportExcelBtn.setEnabled(False)
        exportUnisimBtn.setEnabled(False)
        
        self.loadData()
        self.tvCDUName.setColumnWidth(0,200)
        self.tvCDUName.setColumnWidth(1,200)
        self.tvCDUName.setColumnWidth(2,100)
        self.tvCDUName.setColumnWidth(3,150)
    def loadData(self):
        
        appPro = AppProject.AppProject()        
        dbFile =  appPro.getPath('DB','CDUSpec.db')  
        if dbFile != '' and Path( dbFile ).exists():           
            conn = sqlite3.connect(dbFile)
            try:              
                data = PD.read_sql_query('SELECT Name,UnisimName,Acitive,SimNo FROM CUDNAMES ORDER BY SimNo', conn)    
                self.smCDUName.loadData(data)
                cursor = conn.cursor()
                self.smCDUDepd.depList=[]
                for row in cursor.execute("SELECT CDU, DEP from CUDDep"):
                    self.smCDUDepd.depList.append( (row[0], row[1]) )
                self.smCDUDepd.updateCDU()
            except:
                pass       
            conn.close()
        else:
            data = PD.DataFrame(columns= self.smCDUName.tableHeaderNames )
            self.smCDUName.loadData(data)
            self.smCDUDepd.updateCDU()
            
        simFile =  appPro.getPath('Sim','UnisimCaseFile.usc')
        if simFile != '' and Path( simFile ).exists():
            self.tdSimFile.setText( simFile )
        else:
            self.tdSimFile.setText( self.tr('No Unisim file selected' ) )
        
    @QtCore.Slot()
    def save(self):

        appPro = AppProject.AppProject()        
        dbFile =  appPro.getPath('DB','CDUSpec.db')       
        conn = sqlite3.connect(dbFile)
        try :
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
            
            cursor.execute('DROP TABLE IF EXISTS CUDDep')
            cursor.execute("""
            CREATE TABLE  CUDDep (
                CDU text NOT NULL,
                DEP text NOT NULL
                )
            """)
            if len( self.smCDUDepd.depList) > 0:
                cursor.executemany("insert into CUDDep values (?,?)", self.smCDUDepd.depList)
            conn.commit()			
            conn.close()  
            
            appPro.mLogWdg.logAppend( self.tr('Simulation Specs has been Saved.') ,True)    
        except:
            appPro.mLogWdg.logAppend( self.tr('Saving Simulation Specs failed.') ,True) 
        finally:    
            #conn.commit()			
            conn.close()
    
    @QtCore.Slot()
    def copyUnisimFile(self):
        appPro = AppProject.AppProject()
        simFile =  appPro.getPath('Sim','UnisimCaseFile.usc')
        if simFile == '':    # Project not createed
            appPro.mLogWdg.logAppend( self.tr('<font color=\"#6F4E37\">Please create a new project first.</font>') ,True)
            return        
        
        # Get Unisim case file path
        fileName = QtGui.QFileDialog.getOpenFileName( self, self.tr("Select Unisim Case Flei"), "", ("Unisim case Files (*.usc)") ) [0]
        if fileName == '':   # No file selected
            return         
        shutil.copyfile(fileName, simFile)  # Copy to Sim 
        
        # update view
        if Path( simFile ).exists():
            self.tdSimFile.setText( simFile )
        else:
            self.tdSimFile.setText( self.tr('No Unisim file selected' ) )        
        
    @QtCore.Slot()
    def loadUnisimEquips(self):
        appPro = AppProject.AppProject()
        simFile =  appPro.getPath('Sim','UnisimCaseFile.usc')
        if simFile != '' and Path( simFile ).exists():
            # Open Unisim
            UnisimApp = win32com.client.Dispatch("UniSimDesign.Application.NewInstance")
            
            # Show Unisim
            UnisimApp.Visible = 1 if self.ckShowSimtor.isChecked() else 0
            appPro.mLogWdg.logAppend( self.tr('UniSimDesign application started.') ,True)
            
            # Open Case File
            UnisimCases = UnisimApp.SimulationCases
            OpenedCase = UnisimCases.Open( simFile )
            
            appPro.mLogWdg.logAppend( self.tr('[{0}] opend.').format( simFile ) ,True)
            Ops = OpenedCase.Flowsheet.Operations
            equips=[]
            for op in Ops:
                if op.TypeName in ['absorber' , 'columnop'] :
                    equips.append(op.Name)
            if( len(equips) > 0 ):
                data = PD.DataFrame({'Name':equips,'UnisimName':equips,'Acitive':1, 'SimNo':0}, index= range(0,len(equips)))
                data = data[['Name','UnisimName','Acitive','SimNo']]
                self.smCDUName.loadData(data)
                self.smCDUDepd.updateCDU()
            UnisimApp.Quit()            
        appPro.mLogWdg.logAppend( self.tr('Loading columns from Unisim finished') ,True)
        
