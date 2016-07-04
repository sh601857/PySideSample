#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
from PySide import QtCore
from PySide import QtGui
import SimSpecWidget
import PlotWidget

class MainW(QtGui.QMainWindow):

    def __init__(self):
        super(MainW, self).__init__()

        self.initUI()

    def initUI(self):               
        # create commonds tree        
        self.cmdmodel = QtGui.QStandardItemModel()
        parentItem = self.cmdmodel.invisibleRootItem()
        item = QtGui.QStandardItem(self.tr("1.Specification"))
        item.setData(0,QtCore.Qt.UserRole+1)
        subitem = QtGui.QStandardItem("Simulation Specs")
        subitem.setData( 0, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem)
        subitem = QtGui.QStandardItem("CDU Variables")
        subitem.setData( 1, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem)
        subitem = QtGui.QStandardItem("Product Quality")
        subitem.setData( 2, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem)
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
        self.simSpecWgt =  SimSpecWidget.SimSpecWidget()
        self.plotWgt =  PlotWidget.PlotWidget()
        self.thirdPageWidget =  QtGui.QWidget()

        self.censw =  QtGui.QStackedWidget()
        self.censw.addWidget(self.simSpecWgt)
        self.censw.addWidget(self.plotWgt)
        self.censw.addWidget(self.thirdPageWidget)
        self.censw.setCurrentIndex(1)

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

        self.cmdTree.clicked.connect(self.setWidget)
        
    @QtCore.Slot()
    def setWidget(self,index):
        wgtID = self.cmdmodel.itemFromIndex(index).data(QtCore.Qt.UserRole+1)
        if wgtID == 0:
            self.censw.setCurrentWidget(self.simSpecWgt)
        elif wgtID==1:
            self.censw.setCurrentWidget(self.plotWgt)
        else:
            self.censw.setCurrentWidget(self.thirdPageWidget)
def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainW()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
