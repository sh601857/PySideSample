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
    if op.TypeName in ['absorber' , 'columnop'] :
        print( "{0}\t{1}".format( op.Name , op.TypeName ) )


UnisimApp.Quit()