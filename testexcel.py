import time
import pythoncom
import win32com.client
import threading
stopEvent = threading.Event()

class ExcelEvents:

    _CanQuit = False
    #def OnNewWorkbook(self, wb):
        ##if type(wb) != types.InstanceType:
            ##raise RuntimeError("The transformer doesnt appear to have translated this for us!")
        #print ("OnNewWorkbook")
    #def OnWindowActivate(self, wb, wn):
        ##if type(wb) != types.InstanceType or type(wn) != types.InstanceType:
            ##raise RuntimeError("The transformer doesnt appear to have translated this for us!")
        #print("OnWindowActivate")
    #def OnWindowDeactivate(self, wb, wn):
        #print("OnWindowDeactivate")
    #def OnSheetDeactivate(self, sh):
        #print("OnSheetDeactivate")
    #def OnSheetBeforeDoubleClick(self, Sh, Target, Cancel):
        #print (Target.Column)
        #return 0
    def OnWorkbookBeforeClose(self, Wb, Cancel):
        print ('OnWorkbookBeforeClose[{0}]'.format(Wb.FullName))
        if Wb.FullName == u'D:\\GitHub\\PySideSample\\test.xlsm':
            print(u'****Excel Can Quit Now*****')
            self._CanQuit = True                
        return 0
    
class WorkbookEvents:
    _colsed = False
    def OnActivate(self):
        print ("workbook OnActivate")
    def OnBeforeRightClick(self, Target, Cancel):
        print ("OnBeforeRightClick")
        
    def onBeforeClose(self, Cancel):
        print ("OnBeforeRightClick")

# Open Excel
#xlApp = win32com.client.DispatchWithEvents("Excel.Application", ExcelEvents)


ExcelEvents._CanQuit = False
xlApp = win32com.client.Dispatch("Excel.Application")
xlApp = win32com.client.DispatchWithEvents(xlApp, ExcelEvents)

# Show Excel. Unlike PPT, Word & Excel open up "hidden"
xlApp.Visible = 1
xlApp.UserControl = 1
xlApp._CanQuit = False

# Add a workbook
wbTest = xlApp.Workbooks.Open(u'D:\\GitHub\\PySideSample\\test.xlsm')
print( 'Workbook[{0}]'.format( wbTest.FullName ) )

# Take the active sheet
wsSheet1 = wbTest.Sheets('Sheet1')
print( 'Worksheet[{0}]'.format( wsSheet1.Name ) )
wsSheet1.Activate()

# Add an oval. Shape 9 is an oval.
oval = wsSheet1.Shapes.AddShape(9, 100, 100, 100, 100)

# In the first row, add Values: 0.0, 0.5, 1.0
wsSheet1.Cells(1, 1).Value = 'Values'
wsSheet1.Cells(1, 2).Value = 0.0
wsSheet1.Cells(1, 3).Value = 0.5
wsSheet1.Cells(1, 4).Value = 1.0

xlApp.Calculate()

while xlApp._CanQuit == False:

    time.sleep( 0.1 )
    pythoncom.PumpWaitingMessages()

xlApp=None




