# -*- coding: utf-8 -*-


import sys
import os
from pathlib import Path
from PySide import QtCore
from PySide import QtGui
import AppProject
import SimSpecWidget
import OptVarsWidget
import PlotWidget
import LogWidget



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
        
        
        self._createCMDDock() #Create cmd tree dockwidget
        
        self._createLogDock() #Create log dockwidget

        self._createCentralWgt() #Create central widget	
        
        self._createActionMenuToolBar() #Create actions menu and toolbar	
        
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('CDU-Int')    
        self.showMaximized()

        # Connests signals and slots
        self.cmdTree.clicked.connect(self.setWidget)
        
        # Reset left dock width  after app starts
        QtCore.QTimer.singleShot(200, self.resetDockWidth)
        
    @QtCore.Slot()
    def resetDockWidth(self):
        self.cmdTree.setMinimumWidth(10)

    def setCensWgt(self,wgtID):
        if wgtID == 101:
            self.censw.setCurrentWidget(self.simSpecWgt)
            self.simSpecWgt.loadData()
        elif wgtID == 102:
            self.censw.setCurrentWidget(self.optVarsWgt)
            self.optVarsWgt.loadData()            
        elif wgtID==302:
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
        appPro.mLogWdg.clearLog()
        appPro.mLogWdg.logAppend( self.tr('Project [{0}] cteated.').format( appPro.mFilePath ) ,True)
        
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
        appPro.mLogWdg.clearLog()
        appPro.mLogWdg.logAppend( self.tr('Project [{0}] opend.').format( appPro.mFilePath ) ,True)
        
    @QtCore.Slot()
    def closeProject(self):            

        pass
    
    @QtCore.Slot()
    def save(self):            
        appPro = AppProject.AppProject()
        # save current working widget
        
        # save project file
        if appPro.mFilePath != u'':
            appPro.save()
            
            
    def _createCMDDock(self):  
        # create commonds tree        
        self.cmdmodel = QtGui.QStandardItemModel()
        parentItem = self.cmdmodel.invisibleRootItem()
        item = QtGui.QStandardItem(self.tr("1.Specification"))
        item.setData(101,QtCore.Qt.UserRole+1)
        subitem = QtGui.QStandardItem(self.tr("Simulation Specs"))
        subitem.setData( 101, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem)
        subitem = QtGui.QStandardItem(self.tr("CDU Variables"))
        subitem.setData( 102, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem)
        subitem = QtGui.QStandardItem(self.tr("Product Quality"))
        subitem.setData( 103, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem)
        subitem = QtGui.QStandardItem(self.tr("Monitored Variables"))
        subitem.setData( 104, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem)
        subitem = QtGui.QStandardItem("HEN Stream Data")
        subitem.setData( 105, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem)
        parentItem.appendRow(item)
    
        item = QtGui.QStandardItem(self.tr("2.Sampling"))
        item.setData(201,QtCore.Qt.UserRole+1)
        subitem = QtGui.QStandardItem("Sample Plan")
        subitem.setData( 201, QtCore.Qt.UserRole+1 )
        item.appendRow(subitem) 
        subitem = QtGui.QStandardItem("Sampling")
        subitem.setData(202,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)
        parentItem.appendRow(item)
    
        item = QtGui.QStandardItem(self.tr("3.Analysis"))        
        item.setData(301,QtCore.Qt.UserRole+1)
        subitem = QtGui.QStandardItem("Settings")
        subitem.setData(301,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)
        subitem = QtGui.QStandardItem("Plots")
        subitem.setData(302,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)
        subitem = QtGui.QStandardItem("Rules")
        subitem.setData(303,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)
        subitem = QtGui.QStandardItem("View Point")
        subitem.setData(304,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)
        parentItem.appendRow(item)
    
        item = QtGui.QStandardItem(self.tr("4.Build ANNS"))
        item.setData(401,QtCore.Qt.UserRole+1)
        subitem = QtGui.QStandardItem("Settings")
        subitem.setData(401,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)        
        subitem = QtGui.QStandardItem("Regress")
        subitem.setData(402,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)        
        subitem = QtGui.QStandardItem("Plots")
        subitem.setData(403,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)   
        parentItem.appendRow(item)      
    
        item = QtGui.QStandardItem(self.tr("5.ANNS+i-Heat"))
        item.setData(501,QtCore.Qt.UserRole+1)
        subitem = QtGui.QStandardItem("CDU Settings")
        subitem.setData(501,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)         
        subitem = QtGui.QStandardItem("i-Heat Settings")
        subitem.setData(502,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)  
        subitem = QtGui.QStandardItem("Simulate")
        subitem.setData(503,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)  
        subitem = QtGui.QStandardItem("Tables")
        subitem.setData(504,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)  
        subitem = QtGui.QStandardItem("Plots")
        subitem.setData(505,QtCore.Qt.UserRole+1)
        item.appendRow(subitem)  
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
  
    def _createLogDock(self):
        self.logWgt = LogWidget.LogWidget()
        appPro = AppProject.AppProject()
        appPro.mLogWdg = self.logWgt   # AppProject hold LogWidget for clients 
    
        self._dockLogWgt = QtGui.QDockWidget(self.tr("Log"), self)
        self._dockLogWgt.setWidget( self.logWgt )
        self._dockLogWgt.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        self._dockLogWgt.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea)
        self._dockLogWgt.setFeatures( QtGui.QDockWidget.DockWidgetClosable | QtGui.QDockWidget.DockWidgetMovable | QtGui.QDockWidget.DockWidgetFloatable)
        self._dockLogWgt.setMinimumHeight(  60 )
        self._dockLogWgt.setMaximumHeight( 600 )
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self._dockLogWgt)
        self.setCorner( QtCore.Qt.BottomLeftCorner, QtCore.Qt.LeftDockWidgetArea )
        
    def _createCentralWgt(self) :
        self.simSpecWgt =  SimSpecWidget.SimSpecWidget()
        self.optVarsWgt =  OptVarsWidget.OptVarsWidget()
        self.plotWgt =  PlotWidget.PlotWidget()
        self.emptyPageWidget =  QtGui.QWidget()
    
        self.censw =  QtGui.QStackedWidget()
        self.censw.addWidget(self.emptyPageWidget)
        self.censw.addWidget(self.optVarsWgt)
        self.censw.addWidget(self.simSpecWgt)
        self.censw.addWidget(self.plotWgt)
    
        self.censw.setCurrentIndex(0)
        self._curWgtID = 0
    
        self.setCentralWidget(self.censw)   
        
        
    def _createActionMenuToolBar(self):
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
    
        viewMenu = menubar.addMenu('&View')
        viewMenu.addAction( self._dockLogWgt.toggleViewAction() )
    
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)     
        
        
def main():

    app = QtGui.QApplication(sys.argv)
    ex = MainW()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
