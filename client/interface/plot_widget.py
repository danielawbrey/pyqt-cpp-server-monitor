from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt5.QtCore import QTimer

class Plot_Widget(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=10, height=10, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        
        self.axes = self.fig.add_subplot(111)
        self.axes.set_ylim(ymin=0, ymax=10)
        self.axes.set_ylabel("milliamps")

        self.axes.set_xlim(xmin=0, xmax=10)
        self.axes.set_xlabel("millivolts")

        self.plot_timer = QTimer()
        self.plot_timer.timeout.connect(self.update_plot)

        self.xdata = []
        self.ydata = []

        super(Plot_Widget, self).__init__(self.fig)

    def update_data(self,x,y):
        self.xdata.append(x)
        self.ydata.append(y)
        
    def update_plot(self):
        self.axes.cla()
        self.axes.plot(self.xdata, self.ydata, 'r')
        self.fig.canvas.draw_idle()
        
    def clear_data(self):
        self.axes.clear()
        self.xdata = []
        self.ydata = []