#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
from PySide import QtCore
from PySide import QtGui

class SimSpecWidget(QtGui.QWidget):

    def __init__(self):
        super(SimSpecWidget, self).__init__()     
        self.initUI()
    
    def initUI(self): 
        self.spbNColum = QtGui.QSpinBox()
        self.spbNColum.setRange(1,10)
        self.spbNColum.setValue(5) 
        self.ckShowSimtor = QtGui.QCheckBox(self.tr("Show simulator window during sampling"))
        
        hl1 =  QtGui.QHBoxLayout()
        hl1.addWidget(QtGui.QLabel(self.tr("Number of distillation columns:")) )
        hl1.addWidget(self.spbNColum)
        hl1.addWidget(self.ckShowSimtor)
        
        tv1 = QtGui.QTableView()
        findButton = QtGui.QPushButton(self.tr("&Find"))
        findButton.setDefault(True)
        
        moreButton = QtGui.QPushButton(self.tr("&More"))
        moreButton.setCheckable(True)
        
        moreButton.setAutoDefault(False)
        
        buttonBox = QtGui.QDialogButtonBox(QtCore.Qt.Horizontal)
        buttonBox.addButton(findButton, QtGui.QDialogButtonBox.ActionRole)
        buttonBox.addButton(moreButton, QtGui.QDialogButtonBox.ActionRole) 
        
        layout =  QtGui.QVBoxLayout()        
        layout.addLayout(hl1)
        layout.addWidget(tv1)
        layout.addStretch()
        layout.addWidget(buttonBox)
        self.setLayout(layout)         