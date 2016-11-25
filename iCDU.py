#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
import os
from pathlib import Path
from PySide import QtCore
from PySide import QtGui
import AppProject
import SimSpecWidget
import PlotWidget



class MainW(QtGui.QMainWindow):

    def __init__(self):
        super(MainW, self).__init__()
        self.initUI()

    def initUI(self):  
        
        self.setWindowIcon(QtGui.QIcon('CDU.ico'))
        if (os.name == 'nt'):
            # This is needed to display the app icon on the taskbar on Windows 7
            import ctypes
            myappid = 'iCDU.1.0.0' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)          
        
        # create commonds tree        
        self.cmdmodel = QtGui.QStandardItemModel()
        parentItem = self.cmdmodel.invisibleRootItem()
        item = QtGui.QStandardItem(self.tr("1.Specification"))
        item.setData(101,QtCore.Qt.UserRole+1)
        subitem = QtGui.QStandardItem("Simulation Specs")
        subitem.setData( 101, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem)
        subitem = QtGui.QStandardItem("CDU Variables")
        subitem.setData( 102, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem)
        subitem = QtGui.QStandardItem("Product Quality")
        subitem.setData( 103, QtCore.Qt.UserRole+1 )
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
        self.cmdTree.setMinimumWidth(150)
        dockWidget = QtGui.QDockWidget((""), self)
        dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea)
        dockWidget.setWidget(self.cmdTree)
        dockWidget.setBaseSize(200,800)
        dockWidget.setTitleBarWidget(QtGui.QWidget(dockWidget))
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dockWidget)#hide the titlebar

        #Create central widget			
        self.simSpecWgt =  SimSpecWidget.SimSpecWidget()
        self.plotWgt =  PlotWidget.PlotWidget()
        self.emptyPageWidget =  QtGui.QWidget()

        self.censw =  QtGui.QStackedWidget()
        self.censw.addWidget(self.emptyPageWidget)
        self.censw.addWidget(self.simSpecWgt)
        self.censw.addWidget(self.plotWgt)
        
        self.censw.setCurrentIndex(0)
        self._curWgtID = 0

        self.setCentralWidget(self.censw)

        # Actions
        newProAct = QtGui.QAction(self.tr('New Project'), self)
        #newProAct.setShortcut('Ctrl+Q')
        newProAct.setStatusTip(self.tr('Create a new porject'))
        newProAct.triggered.connect(self.newProject)        

        openProAct = QtGui.QAction(self.tr('Open Project'), self)
        #openProAct.setShortcut('Ctrl+Q')
        openProAct.setStatusTip(self.tr('Open a existing porject'))
        openProAct.triggered.connect(self.openProject)  
        
        closeProAct = QtGui.QAction(self.tr('Close project'), self)
        #closeProAct.setShortcut('Ctrl+Q')
        closeProAct.setStatusTip(self.tr('Close project'))
        closeProAct.triggered.connect(self.closeProject) 
        
        saveAct = QtGui.QAction(self.tr('Save'), self)
        #saveAct.setShortcut('Ctrl+Q')
        saveAct.setStatusTip(self.tr('Save'))
        saveAct.triggered.connect(self.save)  

        exitAction = QtGui.QAction(self.tr('Exit'), self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip(self.tr('Exit application') )
        exitAction.triggered.connect(self.close)

        self.statusBar()
        # menus
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newProAct)
        fileMenu.addAction(openProAct)
        fileMenu.addAction(closeProAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('CDU-Int')    
        self.showMaximized()

        self.cmdTree.clicked.connect(self.setWidget)
        
        QtCore.QTimer.singleShot(200, self.resetDockWidth)
        
    @QtCore.Slot()
    def resetDockWidth(self):
        self.cmdTree.setMinimumWidth(10)

    def setCensWgt(self,wgtID):
        if wgtID == 101:
            self.censw.setCurrentWidget(self.simSpecWgt)
            self.simSpecWgt.loadData()
        elif wgtID==102:
            self.censw.setCurrentWidget(self.plotWgt)
        else:
            self.censw.setCurrentWidget(self.emptyPageWidget)
            
        self._curWgtID = wgtID
        
    @QtCore.Slot()
    def setWidget(self,index):
        wgtID = self.cmdmodel.itemFromIndex(index).data(QtCore.Qt.UserRole+1)
        if( self._curWgtID != wgtID):        
            self.setCensWgt(wgtID)

    @QtCore.Slot()
    def newProject(self):            
        fileName = QtGui.QFileDialog.getSaveFileName(self, self.tr("New project"), "", "iCDU Project Files (*.icdup)"  ) [0]
        if fileName == '':
            return 
        print( fileName )
        
        appPro = AppProject.AppProject()
        appPro.mFilePath = fileName
        appPro.save()
        appPro.creatFolder()
        self.setCensWgt(0)
        
        self.setWindowTitle( 'CDU-Int[{0}]'.format( appPro.mFilePath ) )
    @QtCore.Slot()
    def openProject(self):            
        fileName = QtGui.QFileDialog.getOpenFileName( self, self.tr("Open project"), "", ("iCDU Project Files (*.icdup)") ) [0]
        if fileName == '':
            return 
        print( fileName )
        appPro = AppProject.AppProject()
        appPro.mFilePath = fileName
        appPro.load()
        
        self.setWindowTitle( 'CDU-Int[{0}]'.format( appPro.mFilePath ) )
        self.setCensWgt(0)
    @QtCore.Slot()
    def closeProject(self):            

        pass
    
    @QtCore.Slot()
    def save(self):            
        appPro = AppProject.AppProject()
        if appPro.mFilePath != u'':
            appPro.save()
        
        pass
    
def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainW()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
