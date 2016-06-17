#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
from PySide import QtCore
from PySide import QtGui

class MainW(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainW, self).__init__()
        
        self.initUI()
        
    def initUI(self):               
        # create commonds tree        
        model = QtGui.QStandardItemModel()
        parentItem = model.invisibleRootItem()
        for i in range(4):
            item = QtGui.QStandardItem(self.tr("Step %d" % i) )
            parentItem.appendRow(item)
            for s in range(3):
                cmditem = QtGui.QStandardItem("CMD %d" % s)
                item.appendRow(cmditem)
        cmdTree = QtGui.QTreeView(self)
        cmdTree.setModel(model)
        cmdTree.setHeaderHidden(True)
        cmdTree.expandToDepth(2)
        dockWidget = QtGui.QDockWidget((""), self)
        dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        dockWidget.setWidget(cmdTree)
        dockWidget.setBaseSize(200,800)
        dockWidget.setTitleBarWidget(QtGui.QWidget(dockWidget))
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockWidget)#hide the titlebar
        
	#Create central widget			
        textEdit = QtGui.QTextEdit()		
        self.setCentralWidget(textEdit)
	
	# Actions
        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()
	# menus
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')    
        self.showMaximized()
        
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = MainW()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
