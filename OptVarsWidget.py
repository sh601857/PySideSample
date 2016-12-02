from PySide.QtCore import *
from PySide.QtGui import *
from pathlib import Path
import sqlite3
import shutil
import pandas as PD
import numpy
import win32com.client
import AppProject

UnisimUnits = {1:'Temperature',4:'MassFlow',6:'Enthalpy',24:'DeltaTemperature'}

class OptVarsModel(QAbstractTableModel):
    def __init__(self):
        super(OptVarsModel, self).__init__()
        self.tableHeaderNames = ['Equip', 'Description', 'Variable Type', 'Unisim Value', 'Units', 'Analysis LB','Analysis UB','Opt LB','Opt UB']
        self._dfData = PD.DataFrame(columns= self.tableHeaderNames )
        
        
    def rowCount(self, parent = QModelIndex()):
        return len(self._dfData)

    def columnCount(self, parent = QModelIndex()):
        return len(self.tableHeaderNames)
    
    def data(self, index, role = Qt.DisplayRole):
        if index.isValid() == False:
            return None #QVariant()
        if role == Qt.DisplayRole:
            if index.column() == 2:
                return str( UnisimUnits[ self._dfData.iloc[index.row(),index.column()] ])
            elif index.column() in [3,5,6,7,8]:
                return '{0:.3f}'.format(self._dfData.iloc[index.row(),index.column()] )
            else:
                return str(self._dfData.iloc[index.row(),index.column()] )
        elif role == Qt.EditRole:
            return ( self._dfData.iloc[index.row(),index.column()] )
        elif role == Qt.TextAlignmentRole:
            if index.column() in [3,5,6,7,8]:
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
            if index.column() in [0,5,6,7,8] :
                self._dfData.iloc[index.row(),index.column()] = value
        return True

    def flags(self, index):
        if index.column() in [0,5,6,7,8] :
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
    
        buttonBox = QDialogButtonBox(Qt.Horizontal)
        buttonBox.addButton(saveBtn, QDialogButtonBox.ActionRole)  
        buttonBox.addButton(updateUnisimBtn, QDialogButtonBox.ActionRole)
        
        layout =  QVBoxLayout()        
        layout.addLayout(hl1)
        layout.addWidget(self.tvOptVars)
        #layout.addStretch()
        layout.addWidget(buttonBox)
        self.setLayout(layout)         
        
        self.btnLoadOptVars.clicked.connect( self.loadUnisimOptVars )
        saveBtn.clicked.connect( self.save )
        
    def loadData(self):
        appPro = AppProject.AppProject()        
        dbFile =  appPro.getPath('DB','CDUSpec.db')
        if dbFile != '' and Path( dbFile ).exists(): 
            try:
                conn = sqlite3.connect(dbFile)
                data = PD.read_sql_query('select _Index, Equip, Description, VarType, UnisimValue, Units, AnaLB, AnaUB, OptLB, OptUB from OptVars ORDER BY _Index', conn, index_col='_Index')
                self.tmOptVars.loadData(data)
            except:
                appPro.mLogWdg.logAppend( self.tr('OptVar LoadData failed.') ,True) 
        
        simFile =  appPro.getPath('Sim','UnisimCaseFile.usc')
        if simFile != '' and Path( simFile ).exists():
            self.tdSimFile.setText( simFile )
        else:
            self.tdSimFile.setText( self.tr('No Unisim file selected' ) )
            
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
            self.tmOptVars._dfData.to_sql('OptVars', conn, index=True, index_label='_Index', if_exists='replace') 
            appPro.mLogWdg.logAppend( self.tr('CDU variables have been saved.') ,True) 
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
            Ops = OpenedCase.Flowsheet.Operations
            equips=[]
            for op in Ops:
                if op.Name == 'OptimVar':
                    nRows = op.NumberOfRows
                    lDesc=[]
                    lVarType=[]
                    lUnisimValue=[]
                    lUnits = []
                    lLB=[]
                    lUB=[]
                    
                    for irow in range(1,nRows):
                        if op.Cell(2,irow).AttachmentType != 1:
                            break
                        lDesc.append(op.Cell(1,irow).CellText)
                        lVarType.append(op.Cell(2,irow).VariableType)
                        lUnisimValue.append(op.Cell(2,irow).CellValue)
                        lUnits.append(op.Cell(2,irow).Units)
                        lLB.append(op.Cell(3,irow).CellValue)
                        lUB.append(op.Cell(4,irow).CellValue)
                    
                    
                    if( len(lDesc) > 0 ):
                        data = PD.DataFrame({'Equip':'---','Description':lDesc,  'VarType':lVarType, 'Units':lUnits, 'UnisimValue':lUnisimValue,'AnaLB':lLB,'AnaUB':lUB,'OptLB':lLB,'OptUB':lUB}, index= range(0,len(lDesc)))
                        data = data[['Equip','Description', 'VarType', 'UnisimValue','Units','AnaLB','AnaUB','OptLB','OptUB']]
                        self.tmOptVars.loadData(data)
                        break
                
            UnisimApp.Quit()            
            appPro.mLogWdg.logAppend( self.tr('Loading OptimVar from Unisim finished') ,True)
        