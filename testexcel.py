import win32com.client
# Open Excel
Application = win32com.client.Dispatch("Excel.Application")

# Show Excel. Unlike PPT, Word & Excel open up "hidden"
Application.Visible = 1

# Add a workbook
Workbook = Application.Workbooks.Add()

# Take the active sheet
Base = Workbook.ActiveSheet

# Add an oval. Shape 9 is an oval.
oval = Base.Shapes.AddShape(9, 100, 100, 100, 100)

# In the first row, add Values: 0.0, 0.5, 1.0
Base.Cells(1, 1).Value = 'Values'
Base.Cells(1, 2).Value = 0.0
Base.Cells(1, 3).Value = 0.5
Base.Cells(1, 4).Value = 1.0