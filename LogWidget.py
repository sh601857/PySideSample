# -*- coding: utf-8 -*-

from PySide.QtCore import *
from PySide.QtGui import *

class LogWidget(QWidget):
    def __init__(self):
        super(LogWidget, self).__init__()     
        self.initUI()
    
    def initUI(self):
        self.setWindowFlags(Qt.Dialog  | Qt.CustomizeWindowHint | Qt.WindowTitleHint )
        self._teLogInfo = QTextEdit()
        self._teLogInfo.setReadOnly(True)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self._teLogInfo)
        vbox.setContentsMargins(1,1,1,1)
        self.setLayout(vbox)
        
    def clearLog(self):
        self._teLogInfo.clear()
        
        
    @Slot()
    def logAppend(self, info,  forceRepaint=True,  insert=False): 
        if insert :
            if info[0:3] == "#cl" :
                ptb = self._teLogInfo.document().lastBlock()
                cursor = QTextCursor( ptb )
                cursor.select( QTextCursor.BlockUnderCursor )
                cursor.removeSelectedText()
                self._teLogInfo.append( info[3:] )
            else:
                self._teLogInfo.insertHtml(info)
            if forceRepaint:
                self._teLogInfo.repaint()
        else:
            self._teLogInfo.append( info )
            if forceRepaint:
                self._teLogInfo.repaint()
  