import win32com.client
import sqlite3


# Open Unisim
UnisimApp = win32com.client.Dispatch("UniSimDesign.Application.NewInstance")

# Show Unisim
UnisimApp.Visible = 1

# Open Case File
UnisimCases = UnisimApp.SimulationCases
OpenedCase = UnisimCases.Open( u"D:\\cases\\iCDU\\20161220_20161213_Software_New_interface\\UnisimSim.usc" )


varList = []
uts = OpenedCase.UtilityObjects
for ut in uts:
    if ut.TypeName == 'bptableutility':
        var = ut.ReidVapourPressure
        varList.append( (ut.TypeName, '', ut.Name, 'ReidVapourPressure', '-1' , '' , var.Value, var.IsKnown , var.CanModify , var.UnitConversionType  ) )         
        var = ut.FlashPoint
        varList.append( (ut.TypeName, '', ut.Name, 'FlashPoint', '-1' , '' , var.Value, var.IsKnown , var.CanModify , var.UnitConversionType  ) )          
        cutPs = ut.CutPointCurveValue
        
        for i in range( len(cutPs) ):
            curve = ut.TBPCurve
            varList.append( (ut.TypeName, '', ut.Name, 'TBPCurve', i , '{0:.1f}'.format( cutPs[i] ) , curve.Values[i], curve.IsKnown[i] , curve.CanModify[i]  , curve.UnitConversionType[i]  ) ) 
            curve = ut.D86Curve
            varList.append( (ut.TypeName, '', ut.Name, 'D86Curve', i , '{0:.1f}'.format( cutPs[i] ) , curve.Values[i], curve.IsKnown[i] , curve.CanModify[i] , curve.UnitConversionType[i]  ) )         
            curve = ut.D1160VacCurve
            varList.append( (ut.TypeName, '', ut.Name, 'D1160VacCurve', i , '{0:.1f}'.format( cutPs[i] ) , curve.Values[i], curve.IsKnown[i] , curve.CanModify[i]  , curve.UnitConversionType[i] ) ) 
            curve = ut.D1160AtmCurve
            varList.append( (ut.TypeName, '', ut.Name, 'D1160AtmCurve', i , '{0:.1f}'.format( cutPs[i] ) , curve.Values[i], curve.IsKnown[i] , curve.CanModify[i]  , curve.UnitConversionType[i] ) )     
    elif ut.TypeName == 'traysizingutility':
        secs = ut.SectionNames.Values
        for i in range( len(secs) ):
            curve = ut.MaxFloodingPercentCalcd
            varList.append( (ut.TypeName, '', ut.Name, 'MaxFloodingPercentCalcd', i , secs[i], curve.Values[i], curve.IsKnown[i] , curve.CanModify[i]  , curve.UnitConversionType[i]  ) ) 
            curve = ut.MaxDCBackupPercentCalcd
            varList.append( (ut.TypeName, '', ut.Name, 'MaxDCBackupPercentCalcd', i , secs[i], curve.Values[i], curve.IsKnown[i] , curve.CanModify[i]  , curve.UnitConversionType[i] ) ) 
            curve = ut.MaxWeirLoadingCalcd
            varList.append( (ut.TypeName, '', ut.Name, 'MaxWeirLoadingCalcd', i , secs[i], curve.Values[i], curve.IsKnown[i] , curve.CanModify[i] , curve.UnitConversionType[i]  ) )               
fss = []
fss.append(OpenedCase.Flowsheet)
fss.extend(OpenedCase.Flowsheet.Flowsheets)
for fs in fss:               
    Ops = fs.Operations
    for op in Ops:
        if op.TypeName == 'columnop':
            for i, spec in enumerate( op.ColumnFlowsheet.Specifications ):
                var = spec.Goal 
                varList.append( (op.TypeName, fs.Name, op.Name, 'Specifications', i , '{0}.Goal'.format( spec.name ) , var.Value, var.IsKnown , var.CanModify  , var.UnitConversionType ) )                 
                var = spec.Current  
                varList.append( (op.TypeName, fs.Name, op.Name, 'Specifications', i , '{0}.Current'.format( spec.name ) , var.Value, var.IsKnown , var.CanModify , var.UnitConversionType  ) )        
        elif op.TypeName == 'coolerop':
            var = op.PressureDrop
            varList.append( (op.TypeName, fs.Name, op.Name, 'PressureDrop', '-1' , '' , var.Value, var.IsKnown , var.CanModify  , var.UnitConversionType ) ) 
            var = op.DeltaT
            varList.append( (op.TypeName, fs.Name, op.Name, 'DeltaT', '-1' , '' , var.Value, var.IsKnown , var.CanModify  , var.UnitConversionType ) )
            var = op.Duty
            varList.append( (op.TypeName, fs.Name, op.Name, 'Duty', '-1' , '' , var.Value, var.IsKnown , var.CanModify  , var.UnitConversionType ) )
            
        elif op.TypeName == 'heaterop':
            var = op.PressureDrop
            varList.append( (op.TypeName, fs.Name, op.Name, 'PressureDrop', '-1' , '' , var.Value, var.IsKnown , var.CanModify , var.UnitConversionType  ) ) 
            var = op.DeltaT
            varList.append( (op.TypeName, fs.Name, op.Name, 'DeltaT', '-1' , '' , var.Value, var.IsKnown , var.CanModify  , var.UnitConversionType ) )
            var = op.Duty
            varList.append( (op.TypeName, fs.Name, op.Name, 'Duty', '-1' , '' , var.Value, var.IsKnown , var.CanModify  , var.UnitConversionType ) )
            
        elif op.TypeName == 'heatexop':
            var = op.Duty
            varList.append( (op.TypeName, fs.Name, op.Name, 'Duty', '-1' , '' , var.Value, var.IsKnown , var.CanModify , var.UnitConversionType  ) )                
        elif op.TypeName == 'spreadsheetop':
            imCells = op.Imports 
            for i, cell in enumerate( imCells ):
                varList.append( (op.TypeName, fs.Name, op.Name, 'Imports', i , op.Imports.Names[i] , cell.ImportedVariable.Value, cell.ImportedVariable.IsKnown , cell.ImportedVariable.CanModify , cell.ImportedVariable.UnitConversionType) ) 
                
            pass  
        elif op.TypeName == 'teeop':
            BrNames = op.Products.Names
            SPFracs = op.Splits
            for i in range( len(BrNames) ):
                varList.append( (op.TypeName, fs.Name, op.Name, 'Splits', i , BrNames[i] , SPFracs.Values[i], SPFracs.IsKnown[i] , SPFracs.CanModify[i]  , SPFracs.UnitConversionType[i] ) ) 
            
        elif op.TypeName == 'virtualstreamop':
            var = op.MasFlowMultiplier
            varList.append( (op.TypeName, fs.Name, op.Name, 'MasFlowMultiplier', '-1' , '' , var.Value, var.IsKnown , var.CanModify , var.UnitConversionType  ) )
        
    Mss = fs.Streams
    for ms in Mss:
        if ms.TypeName == 'materialstream':
            var = ms.VapourFraction
            varList.append( (ms.TypeName, fs.Name, ms.Name, 'VapourFraction', '-1' , '' , var.Value, var.IsKnown , var.CanModify , var.UnitConversionType  ) ) 
            var = ms.Temperature
            varList.append( (ms.TypeName, fs.Name, ms.Name, 'Temperature', '-1' , '' , var.Value, var.IsKnown , var.CanModify , var.UnitConversionType  ) ) 
            var = ms.Pressure
            varList.append( (ms.TypeName, fs.Name, ms.Name, 'Pressure', '-1' , '' , var.Value, var.IsKnown , var.CanModify  , var.UnitConversionType ) ) 
            var = ms.MassFlow
            varList.append( (ms.TypeName, fs.Name, ms.Name, 'MassFlow', '-1' , '' , var.Value, var.IsKnown , var.CanModify  , var.UnitConversionType ) ) 
            var = ms.HeatFlow
            varList.append( (ms.TypeName, fs.Name, ms.Name, 'HeatFlow', '-1' , '' , var.Value, var.IsKnown , var.CanModify  , var.UnitConversionType ) ) 
            var = ms.ActualVolumeFlow
            varList.append( (ms.TypeName, fs.Name, ms.Name, 'ActualVolumeFlow', '-1' , '' , var.Value, var.IsKnown , var.CanModify , var.UnitConversionType  ) ) 
            var = ms.StdLiqVolFlow
            varList.append( (ms.TypeName, fs.Name, ms.Name, 'StdLiqVolFlow', '-1' , '' , var.Value, var.IsKnown , var.CanModify  , var.UnitConversionType ) ) 
            var = ms.MassDensity
            varList.append( (ms.TypeName, fs.Name, ms.Name, 'MassDensity', '-1' , '' , var.Value, var.IsKnown , var.CanModify , var.UnitConversionType  ) )    
            var = ms.MassHeatCapacity
            varList.append( (ms.TypeName, fs.Name, ms.Name, 'MassHeatCapacity', '-1' , '' , var.Value, var.IsKnown , var.CanModify , var.UnitConversionType  ) )  
            var = ms.Viscosity
            varList.append( (ms.TypeName, fs.Name, ms.Name, 'Viscosity', '-1' , '' , var.Value, var.IsKnown , var.CanModify  , var.UnitConversionType ) )              

        elif ms.TypeName == 'energystream':
            var = ms.HeatFlow
            varList.append( (ms.TypeName, fs.Name, ms.Name, 'HeatFlow', '-1' , '' , var.Value, var.IsKnown , var.CanModify , var.UnitConversionType  ) )  
            
        

       
dbFile =  'Unisim.db'       
conn = sqlite3.connect(dbFile)
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS D_Vars')
cursor.execute("""
    CREATE TABLE  D_Vars (
    ObjType TEXT NOT NULL,
    FlowSheet TEXT,
    ObjName TEXT,
    Property TEXT,
    VIndex INTEGER,
    VName  TEXT,
    Value REAL,
    IsKnown INTEGER,
    CanModify INTEGER,
    UnitConType INTEGER
    )
""")        

if len( varList ) > 0:
    cursor.executemany("insert into D_Vars values (?,?,?,?,?,?,?,?,?,?)", varList )
conn.commit()			
conn.close() 

#uobjs = OpenedCase.UtilityObjects
#for ut in uobjs:
    #print( "{0}\t{1}".format( ut.Name , ut.TypeName ) )


#fss = []
#fss.append(OpenedCase.Flowsheet)
#fss.extend(OpenedCase.Flowsheet.Flowsheets)
    
#for fs in fss:    

    #print( "FS [{0}]##############################################################".format( fs.Name ) )
    
    #Ops = fs.Operations    
    #for op in Ops:
        #print( "{0}\t{1}".format( op.Name , op.TypeName ) )
        
    #Mss = fs.Streams
    #for ms in Mss:  
        #print( "{0}\t{1}".format( ms.Name , ms.TypeName ) )    



    #optvar=None
    #T102=None    
    #if op.TypeName in ['absorber' , 'columnop'] :
        #print( "{0}\t{1}".format( op.Name , op.TypeName ) )

    #if op.Name == 'OptimVar':
        #optvar = op
        ##print( "NumRow={0}\tNumCol={1}".format( op.NumberOfRows , op.NumberOfColumns ) )
        #for irow in range(1, op.NumberOfRows):
            #if op.Cell(2,irow).AttachmentType != 1:
                #break     
            
            #print ( '-------------------------row{0}-------------------------'.format( irow ))     
            #print ( 'AttachedObjectName ', op.Cell(2,irow).AttachedObjectName  )
            #print ( 'AttachmentType     ', op.Cell(2,irow).AttachmentType   )
            #print ( 'CellText           ',op.Cell(2,irow).CellText )
            #print ( 'CellValue          ',op.Cell(2,irow).CellValue  )
            #print ( 'IsValid            ',op.Cell(2,irow).IsValid   )
            #print ( 'Type               ',op.Cell(2,irow).Type  )
            #print ( 'Units              ',op.Cell(2,irow).Units   )
            #print ( 'VariableName       ',op.Cell(2,irow).VariableName )
            #print ( 'VariableType       ',op.Cell(2,irow).VariableType)
            #print ( 'VariableValue      ',op.Cell(2,irow).Variable.Value) 
        
 
    #if op.Name == 'T102':
        #T102 = op
        #usdColumnSpecs = op.ColumnFlowsheet.Specifications
        #for usdColumnSpec in usdColumnSpecs:
            #print( '{0:20} active={1}'.format( usdColumnSpec.name , usdColumnSpec.IsActive ) )
 
#optvar.Cell(2,47).ImportedVariable = T102.ColumnFlowsheet.Specifications.Item('PA_1_Duty(Pa)').Goal          

OpenedCase.SaveAs( 'D:\\cases\\iCDU\\saveas.usc' )    
UnisimApp.Quit()