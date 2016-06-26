#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
from PySide import QtCore
from PySide import QtGui
import SimSpecWidget

class MainW(QtGui.QMainWindow):

    def __init__(self):
        super(MainW, self).__init__()

        self.initUI()

    def initUI(self):               
        # create commonds tree        
        self.cmdmodel = QtGui.QStandardItemModel()
        parentItem = self.cmdmodel.invisibleRootItem()
        item = QtGui.QStandardItem(self.tr("1.Specification"))
        item.appendRow(QtGui.QStandardItem("Simulation Specs"))
        item.appendRow(QtGui.QStandardItem("CDU Variables"))
        item.appendRow(QtGui.QStandardItem("Product Quality"))
        item.appendRow(QtGui.QStandardItem("Monitored Variables"))
        item.appendRow(QtGui.QStandardItem("HEN Stream Data"))
        parentItem.appendRow(item)
        
        item = QtGui.QStandardItem(self.tr("2.Sampling"))
        item.appendRow(QtGui.QStandardItem("Sample Plan"))
        item.appendRow(QtGui.QStandardItem("Sampling"))
        parentItem.appendRow(item)

        item = QtGui.QStandardItem(self.tr("3.Analysis"))
        item.appendRow(QtGui.QStandardItem("Settings"))
        item.appendRow(QtGui.QStandardItem("Plots"))
        item.appendRow(QtGui.QStandardItem("Rules"))  
        item.appendRow(QtGui.QStandardItem("View Point"))      
        parentItem.appendRow(item)
        
        item = QtGui.QStandardItem(self.tr("4.Build ANNS"))
        item.appendRow(QtGui.QStandardItem("Settings"))
        item.appendRow(QtGui.QStandardItem("Regress"))
        item.appendRow(QtGui.QStandardItem("Plots"))       
        parentItem.appendRow(item)      
 
        item = QtGui.QStandardItem(self.tr("5.ANNS+i-Heat"))
        item.appendRow(QtGui.QStandardItem("CDU Settings"))
        item.appendRow(QtGui.QStandardItem("i-Heat Settings"))
        item.appendRow(QtGui.QStandardItem("Simulate"))   
        item.appendRow(QtGui.QStandardItem("Tables"))  
        item.appendRow(QtGui.QStandardItem("Plots")) 
        parentItem.appendRow(item)   
                
        self.cmdTree = QtGui.QTreeView(self)
        self.cmdTree.setModel(self.cmdmodel)
        self.cmdTree.setHeaderHidden(True)
        self.cmdTree.expandToDepth(2)
        dockWidget = QtGui.QDockWidget((""), self)
        dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        dockWidget.setWidget(self.cmdTree)
        dockWidget.setBaseSize(200,800)
        dockWidget.setTitleBarWidget(QtGui.QWidget(dockWidget))
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockWidget)#hide the titlebar

        #Create central widget			
        self.firstPageWidget =  SimSpecWidget.SimSpecWidget()
        self.secondPageWidget =  QtGui.QWidget()
        self.thirdPageWidget =  QtGui.QWidget()

        self.censw =  QtGui.QStackedWidget()
        self.censw.addWidget(self.firstPageWidget)
        self.censw.addWidget(self.secondPageWidget)
        self.censw.addWidget(self.thirdPageWidget)
        self.censw.setCurrentIndex(0)

        self.setCentralWidget(self.censw)

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
        self.setWindowTitle('CDU-Int')    
        self.showMaximized()


def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainW()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
