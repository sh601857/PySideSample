import sys
import matplotlib
matplotlib.use('Qt4Agg')
import pylab

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PySide import QtCore, QtGui

class PlotWidget(QtGui.QWidget):
    def __init__(self):
        super(PlotWidget, self).__init__()     
        self.initUI()

    def initUI(self):
        # generate the plot
        fig = Figure(figsize=(600,600), dpi=72, facecolor=(.94,.94,.94), edgecolor=(0,0,0),tight_layout=True)
        ax = fig.add_subplot(111,axis_bgcolor=(.94,.94,.94),title='test plot',xlabel='x',ylabel='y')
        ax.xaxis.set_tick_params(width=1,size=8)      
        ax.plot([0,1])
        # generate the canvas to display the plot
        canvas = FigureCanvas(fig)
        layout =  QtGui.QVBoxLayout()
        layout.addWidget(canvas)
        
        self.setLayout(layout)  