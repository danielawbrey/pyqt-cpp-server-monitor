from PyQt5.QtWidgets import QWidget, QVBoxLayout
from .plot_widget import Plot_Widget
from .user_input_widget import User_Input_Widget
import fpdf
from . import worker, udp_client
import datetime
from PyQt5.QtCore import QTimer

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.start_time, self.stop_time = None, None
        
        self.layout = QVBoxLayout()
        self.plot = Plot_Widget(self)
        self.layout.addWidget(self.plot)
        self.user_input_widget = User_Input_Widget(self)
        self.layout.addWidget(self.user_input_widget)
        self.setLayout(self.layout)

    def start_test_manager(self, user_input):
        self.start_time = datetime.datetime.now()

        self.thread_data = worker.Worker(udp_client.UDP_Client(user_input[0].text(), user_input[1].text(), user_input[2].text(), user_input[3].text()), parent=self)
        self.thread_data.server_data.connect(self.plot.update_data)
        self.thread_data.start()

        self.plot.plot_timer.start(10)

    def stop_test_manager(self):
        self.stop_time = datetime.datetime.now()
        self.plot.plot_timer.stop()
        self.thread_data.exit_session()
        # self.log_test_data()
    
    def log_test_data(self):
        self.plot.figure.savefig('test.png')
        pdf = fpdf.FPDF()  
        pdf.add_page()
        pdf.set_font("Arial", size = 12)
        pdf.cell(200, 10, txt = ("Device IP Address: {}").format(self.user_input_widget.ip_address_input.text()), ln = 1, align = 'C')
        pdf.cell(200, 10, txt = ("Device Port: {}").format(self.user_input_widget.port_input.text()), ln = 2, align = 'C')
        pdf.cell(200, 10, txt = ("Test Duration: {}").format(self.user_input_widget.test_duration_input.text()), ln = 3, align = 'C')
        pdf.cell(200, 10, txt = ("Device Rate: {}").format(self.user_input_widget.test_rate_input.text()), ln = 4, align = 'C')
        pdf.cell(200, 10, txt = ("Execution Time: {}").format(self.stop_time-self.start_time), ln = 5, align = 'C')
        pdf.image('test.png', x=0, y=65, w=200, h=100)
        pdf.output("test_report.pdf") 
