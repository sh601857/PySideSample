import sys
import matplotlib
matplotlib.use('Qt4Agg')
import pylab

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons,SpanSelector

from PySide.QtCore import *
from PySide.QtGui import *

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=9, height=6, dpi=None):
        self.fig = Figure(figsize=(width, height), facecolor=(.94,.94,.94), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)    
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.axes = self.fig.add_axes([0.06, 0.10, 0.9, 0.85], axis_bgcolor=(.94,.94,.94))
        
        self.compute_initial_figure()
        
        # horizontal x range span
        axxspan = self.fig.add_axes([0.06, 0.05, 0.9, 0.02])
        axxspan.axis([-0.2, 1.2, -0.2, 1.2])
        axxspan.tick_params('y', labelright = False ,labelleft = False ,length=0)
        self.xspan = SpanSelector(axxspan, self.onselectX, 'horizontal',useblit=True, span_stays=True,  rectprops=dict(alpha=0.5, facecolor='blue'))
        
        # vertical y range span
        axyspan = self.fig.add_axes([0.02, 0.10, 0.01, 0.85])
        axyspan.axis([-0.2, 1.2, -0.2, 1.2])
        axyspan.tick_params('x', labelbottom = False ,labeltop = False ,length=0)
        self.yspan = SpanSelector(axyspan, self.onselectY, 'vertical',useblit=True, span_stays=True,  rectprops=dict(alpha=0.5, facecolor='blue'))
        # reset x y spans
        axReset = self.fig.add_axes([0.01, 0.05, 0.03, 0.03],frameon=False, )
        self.bnReset = Button(axReset, 'Reset')
        self.bnReset.on_clicked( self.xyReset )
        # contextMenu
        acExportPlot = QAction(self.tr("Export plot"), self)
        FigureCanvas.connect(acExportPlot,SIGNAL('triggered()'), self, SLOT('exportPlot()') )
        FigureCanvas.addAction(self, acExportPlot )
        FigureCanvas.setContextMenuPolicy(self, Qt.ActionsContextMenu )
        
    def onselectX(self, xmin, xmax) :
        self.axes.set_xlim(xmin, xmax)
        self.draw_idle()
        
    def onselectY(self, ymin, ymax) :
        self.axes.set_ylim(ymin, ymax)
        self.draw_idle() 
        
    def xyReset(self, event) :
        self.axes.set_xlim(-0.2, 1.2)
        self.axes.set_ylim(-0.2, 1.2)
        self.yspan.stay_rect.set_visible(False)
        self.xspan.stay_rect.set_visible(False)
        self.draw_idle()

    
    def compute_initial_figure(self):
        N = 50
        x = np.random.rand(N)
        y = np.random.rand(N)
        colors = np.random.rand(N)
        area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses
        
        self.axes.scatter(x, y, s=area, c=colors, alpha=0.5) 
        self.axes.axis([-0.2, 1.2, -0.2, 1.2])
        
    def exportPlot(self):
        
        fileName = QFileDialog.getSaveFileName( self, self.tr("Save figure"), "", ("PNG file (*.png)") ) [0]
        if fileName == '':   # No file selected
            return  
        self.fig.savefig( fileName, format='png' )
        
class PlotWidget(QWidget):
    def __init__(self):
        super(PlotWidget, self).__init__()     
        self.initUI()
        
    def initUI(self):
                        
        # generate the canvas to display the plot
        #self.canvas = FigureCanvas(self.fig)
        
        self.canvas = MyMplCanvas(self, width=5, height=4)
        layout =  QVBoxLayout()
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)  
        
        
        
        #class MyMplCanvas(FigureCanvas):
            #"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
        
            #def __init__(self, parent=None, width=5, height=4, dpi=None):
                #fig = Figure(figsize=(width, height), dpi=dpi)
                #FigureCanvas.__init__(self, fig)
                #self.setParent(parent)
            
                #FigureCanvas.setSizePolicy(self,
                                           #QSizePolicy.Expanding,
                                           #QSizePolicy.Expanding)
                #FigureCanvas.updateGeometry(self)
                
                #axcolor = 'lightgoldenrodyellow'
                #self.axes = fig.add_axes([0.25, 0.25, 0.65, 0.7], axisbg=axcolor)
                
                ##self.axes.subplots_adjust(left=0.25, bottom=0.25)
                ## We want the axes cleared every time plot() is called
                ##self.axes.hold(False)
                
                #self.compute_initial_figure()  
                
                
                
                #axxmin = fig.add_axes([0.25, 0.1, 0.65, 0.03], axisbg=axcolor)
                #axxmax = fig.add_axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor) 
                
                #self.sXMIN = Slider(axxmin, 'XMin', 0.0, 1.0, valinit=0.0)
                #self.sXMAX = Slider(axxmax, 'XMax', 0.0, 1.0, valinit=1.0,slidermin=self.sXMIN) 
                #self.sXMIN.slidermax = self.sXMAX
                
                #self.sXMIN.on_changed(self.updateSider)
                #self.sXMAX.on_changed(self.updateSider)                        
        
            #def compute_initial_figure(self):
                #t = np.arange(0.0, 1.0, 0.001)
                #a0 = 5
                #f0 = 3
                #s = a0*np.sin(2*np.pi*f0*t)
                #self.l, = self.axes.plot(t, s, lw=2, color='red')
                #self.axes.axis([0, 1, -10, 10])  
                ##plt.show()
                
            #def updateSider(self, val):
                ##t = np.arange(0.0, 1.0, 0.001)
                #xmin = self.sXMIN.val
                #xmax = self.sXMAX.val
                ##self.l.set_ydata(amp*np.sin(2*np.pi*freq*t))
                #self.axes.set_xlim( xmin, xmax )
                
                #self.draw_idle()