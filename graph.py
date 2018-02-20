from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton

import numpy as np
import random as rand


class Graph(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        plt.ion()

        self.numbers = []
        self.plot()

    def plot(self):
        self.ax = self.figure.add_subplot(111)
        self.ax.yaxis.set_major_locator(MaxNLocator(nbins=1, integer=True))
        self.figure.canvas.draw()

    def addvalue(self, value=None):
        if value is not None:
            if value == 0:
                value = 100
            self.numbers.append(value)
            freq = [self.numbers.count(i) for i in self.numbers]
            self.ax.plot(self.numbers, freq, ".")
            self.figure.canvas.draw()
