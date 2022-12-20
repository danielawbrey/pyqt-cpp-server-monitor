from PyQt5.QtWidgets import QWidget, QVBoxLayout
from .plot_widget import Plot_Widget
from .user_input_widget import User_Input_Widget

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.plot = Plot_Widget()
        self.layout.addWidget(self.plot)
        self.user_input_widget = User_Input_Widget(self.plot)
        self.layout.addWidget(self.user_input_widget)
        self.setLayout(self.layout)