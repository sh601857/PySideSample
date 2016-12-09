import win32com.client
# Open Unisim
UnisimApp = win32com.client.Dispatch("UniSimDesign.Application.NewInstance")

# Show Unisim
UnisimApp.Visible = 1

# Open Case File
UnisimCases = UnisimApp.SimulationCases
OpenedCase = UnisimCases.Open( u"D:\\cases\\iCDU\\20160201 FINAL CASE_Simplified CDU_V4-LMOE.usc" )

Ops = OpenedCase.Flowsheet.Operations
optvar=None
T102=None
for op in Ops:
    #if op.TypeName in ['absorber' , 'columnop'] :
        #print( "{0}\t{1}".format( op.Name , op.TypeName ) )

    if op.Name == 'OptimVar':
        optvar = op
        #print( "NumRow={0}\tNumCol={1}".format( op.NumberOfRows , op.NumberOfColumns ) )
        for irow in range(1, op.NumberOfRows):
            if op.Cell(2,irow).AttachmentType != 1:
                break     
            
            print ( '-------------------------row{0}-------------------------'.format( irow ))     
            print ( 'AttachedObjectName ', op.Cell(2,irow).AttachedObjectName  )
            print ( 'AttachmentType     ', op.Cell(2,irow).AttachmentType   )
            print ( 'CellText           ',op.Cell(2,irow).CellText )
            print ( 'CellValue          ',op.Cell(2,irow).CellValue  )
            print ( 'IsValid            ',op.Cell(2,irow).IsValid   )
            print ( 'Type               ',op.Cell(2,irow).Type  )
            print ( 'Units              ',op.Cell(2,irow).Units   )
            print ( 'VariableName       ',op.Cell(2,irow).VariableName )
            print ( 'VariableType       ',op.Cell(2,irow).VariableType)
            print ( 'VariableValue      ',op.Cell(2,irow).Variable.Value) 
        
 
    if op.Name == 'T102':
        T102 = op
        usdColumnSpecs = op.ColumnFlowsheet.Specifications
        for usdColumnSpec in usdColumnSpecs:
            print( '{0:20} active={1}'.format( usdColumnSpec.name , usdColumnSpec.IsActive ) )
 
optvar.Cell(2,47).ImportedVariable = T102.ColumnFlowsheet.Specifications.Item('PA_1_Duty(Pa)').Goal          

OpenedCase.SaveAs( 'D:\\cases\\iCDU\\saveas.usc' )    
UnisimApp.Quit()