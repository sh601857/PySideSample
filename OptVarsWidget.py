from PySide.QtCore import *
from PySide.QtGui import *
from pathlib import Path
import sqlite3
import shutil
import pandas as PD
import numpy
import win32com.client
import AppProject

UnisimUnits = {1:'Temperature',2:'Pressure', 3:'MolarFlow', 4:'MassFlow', 5:'VolumeFlow', 6:'Enthalpy', 7:'Density',8:'HeatCapacity',9:'Entropy', 10:'ThermalConductivity',
               11:'Viscosity', 15:'HeatCapacityMass', 16:'MassDensity', 
               22:'Length', 24:'DeltaTemperature', 28:'StdDensity',
               30:'MassEnthalpy', 41:'Area',42:'Volume', 45:'DeltaPressure', 55:'VolumeFlowPerLength', 
               62:'StdVolumeFlow', 64:'Percent',65:'Work',70:'ActualVolumeFlow',
               84:'Power'}

class OptVarsModel(QAbstractTableModel):
    def __init__(self):
        super(OptVarsModel, self).__init__()
        self.tableHeaderNames = ['ID', 'Description', 'Unisim Value', 'Units', 'Known?', 'Can be Modified?', 'Type', 'Object', 'Property' ]
        self._dfData = PD.DataFrame(columns= self.tableHeaderNames )
        
        
    def rowCount(self, parent = QModelIndex()):
        return len(self._dfData)

    def columnCount(self, parent = QModelIndex()):
        return len(self.tableHeaderNames)
    
    def data(self, index, role = Qt.DisplayRole):
        if index.isValid() == False:
            return None #QVariant()
        if role == Qt.DisplayRole:
            return str(self._dfData.iloc[index.row(),index.column()] )
        elif role == Qt.EditRole:
            return ( self._dfData.iloc[index.row(),index.column()] )
        elif role == Qt.TextAlignmentRole:
            if index.column() == 2:
                return Qt.AlignRight 
            else:
                return Qt.AlignLeft 
        elif role == Qt.ForegroundRole:
            if self.flags(index) & Qt.ItemIsEditable :             
                return QBrush( QColor('#0000FF') )           
        else:
            return None #QVariant()

    def setData(self, index, value, role = Qt.EditRole):
        if role == Qt.EditRole :
            if index.column() == 1 :
                self._dfData.iloc[index.row(),index.column()] = value
        return True

    def flags(self, index):
        if index.column() in [1] :
            flag = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            flag = Qt.ItemIsSelectable | Qt.ItemIsEnabled 
        return flag
    
    def headerData(self, section, orientation, role = Qt.DisplayRole):
        if orientation == Qt.Horizontal :
            if role == Qt.DisplayRole :
                return self.tableHeaderNames[section]
        else:
            if role == Qt.DisplayRole :
                return section+1
        return None
    
    def loadData(self, data ):
        self.beginResetModel()
        self._dfData = data      
        self.endResetModel()    
        
        

class addVarDlg( QDialog ):
    def __init__(self):
        super(addVarDlg, self).__init__()     
        self.initUI()  
        
    def initUI(self): 
       
        pass

class OptVarsWidget(QWidget):

    def __init__(self):
        super(OptVarsWidget, self).__init__()     
        self.initUI()

    def initUI(self): 
        
        self.ckShowSimtor = QCheckBox(self.tr("Show simulator window during sampling"))
        self.ckShowSimtor.setChecked(True)
        self.btnLoadOptVars = QPushButton(self.tr("Load OptVars from Unisim"))
        self.tdSimFile = QLineEdit()
        self.tdSimFile.setReadOnly(True)
        hl1 =  QHBoxLayout()
        hl1.addWidget(self.tdSimFile)
        hl1.addWidget(self.ckShowSimtor)
        hl1.addWidget(self.btnLoadOptVars)
    
        self.tvOptVars = QTableView()
        self.tvOptVars.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )
    
        self.tmOptVars = OptVarsModel()    
        self.tvOptVars.setModel(self.tmOptVars)        

        saveBtn = QPushButton(self.tr("Save"))  
        updateUnisimBtn = QPushButton(self.tr("Update Unisim Spreadsheet"))  
        updateUnisimBtn.setEnabled( False )
        
        addBtn = QPushButton(self.tr("Add"))  
                
    
        buttonBox = QDialogButtonBox(Qt.Horizontal)
        buttonBox.addButton(addBtn, QDialogButtonBox.ActionRole)
        
        buttonBox.addButton(saveBtn, QDialogButtonBox.ActionRole)         
        buttonBox.addButton(updateUnisimBtn, QDialogButtonBox.ActionRole)
        
        layout =  QVBoxLayout()        
        layout.addLayout(hl1)
        layout.addWidget(self.tvOptVars)
        #layout.addStretch()
        layout.addWidget(buttonBox)
        
        layout.setContentsMargins(1,1,1,1)
        self.setLayout(layout)         
        
        self.btnLoadOptVars.clicked.connect( self.loadUnisimOptVars )
        addBtn.clicked.connect( self.add )
        saveBtn.clicked.connect( self.save )
    
    
        
    def loadData(self):
        appPro = AppProject.AppProject()        
        dbFile =  appPro.getPath('DB','CDUSpec.db')
        if dbFile != '' and Path( dbFile ).exists(): 
            try:
                pass
            except:
                appPro.mLogWdg.logAppend( self.tr('OptVar LoadData failed.') ,True) 
        
        simFile =  appPro.getPath('Sim','UnisimCaseFile.usc')
        if simFile != '' and Path( simFile ).exists():
            self.tdSimFile.setText( simFile )
        else:
            self.tdSimFile.setText( self.tr('No Unisim file selected' ) )
            
    
    @Slot()
    def add(self):  
        pass
        
    @Slot()
    def save(self): 
       
        appPro = AppProject.AppProject()        
        dbFile =  appPro.getPath('DB','CDUSpec.db')       
        conn = sqlite3.connect(dbFile)
        #cursor = conn.cursor()
        #cursor.execute('DROP TABLE IF EXISTS OptVars')
        #cursor.execute("""
        #CREATE TABLE  OptVars (
            #index INTEGER NOT NULL,
            #Column text ,
            #Description text,
            #VarType INTEGER,
            #UnisimValue real,
            #Units text,
            #AnaLB real,
            #AnaUB real,
            #OptLB real,
            #OptUB real,
            #)
        #""")        
        try:
            pass
        except:
            appPro.mLogWdg.logAppend( self.tr('Saving CDU variables failed.') ,True) 
        finally:    
            #conn.commit()			
            conn.close()
        
    @Slot()
    def loadUnisimOptVars(self):         
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
            
            varList = []
            uts = OpenedCase.UtilityObjects
            for ut in uts:
                if op.TypeName == 'bptableutility':
                    pass
                elif op.TypeName == 'traysizingutility':
                    pass
                
            fss = []
            fss.append(OpenedCase.Flowsheet)
            fss.extend(OpenedCase.Flowsheet.Flowsheets)
            for fs in fss:               
                Ops = fs.Operations
                for op in Ops:
                    if op.TypeName == 'columnop':
                        pass
                    elif op.TypeName == 'coolerop':
                        pass                
                    elif op.TypeName == 'heaterop':
                        pass
                    elif op.TypeName == 'heatexop':
                        pass                
                    elif op.TypeName == 'spreadsheetop':
                        pass  
                    elif op.TypeName == 'teeop':
                        pass
                    elif op.TypeName == 'virtualstreamop':
                        pass
                    
                Mss = fs.Streams
                for ms in Mss:
                    if ms.TypeName == 'materialstream':
                        pass
                    elif ms.TypeName == 'energystream':
                        pass
                
            UnisimApp.Quit()            
            appPro.mLogWdg.logAppend( self.tr('Loading OptimVar from Unisim finished') ,True)
        