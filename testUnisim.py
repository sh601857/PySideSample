import win32com.client
# Open Unisim
UnisimApp = win32com.client.Dispatch("UniSimDesign.Application.NewInstance")

# Show Unisim
UnisimApp.Visible = 1

# Open Case File
UnisimCases = UnisimApp.SimulationCases
OpenedCase = UnisimCases.Open( u"D:\\cases\\iCDU\\20160201 FINAL CASE_Simplified CDU_V4-LMOE.usc" )

Ops = OpenedCase.Flowsheet.Operations

for op in Ops:
    #if op.TypeName in ['absorber' , 'columnop'] :
        #print( "{0}\t{1}".format( op.Name , op.TypeName ) )
    if op.Name == 'OptimVar':
        print( "NumRow={0}\tNumCol={1}".format( op.NumberOfRows , op.NumberOfColumns ) )
        print ( op.Cell(2,1).CellText )
        print ( op.Cell(2,1).VariableName )
        print ( op.Cell(2,1).VariableType)
        print ( op.Cell(2,1).AttachedObjectName  )
        print ( op.Cell(2,1).CellValue  )
        print ( op.Cell(2,1).Type  )
        print ( op.Cell(2,1).AttachmentType   )
          

        print ( op.Cell(2,50).Type   )    
        print ( op.Cell(2,50).AttachmentType   )
        


UnisimApp.Quit()