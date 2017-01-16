import time
import win32com.client

# Open Excel
xlApp = win32com.client.Dispatch("Excel.Application")

# Show Excel. Unlike PPT, Word & Excel open up "hidden"
xlApp.Visible = 1
xlApp.UserControl = 0

# Add a workbook
wbTest = xlApp.Workbooks.Open('D:\\GitHub\\PySideSample\\test.xlsm')
print( 'Workbook[{0}]'.format( wbTest.Name ) )

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


while xlApp.Visible:

    time.sleep(1)

wbTest.Save()




