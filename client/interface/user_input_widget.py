import fpdf
from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QGridLayout, QLabel
from PyQt5.QtCore import QTimer, QRegExp
from PyQt5.QtGui import QRegExpValidator
from interface.worker import Worker
import datetime
from .udp_client import UDP_Client

class User_Input_Widget(QWidget):
    def __init__(self, plot):
        super().__init__()
        self.layout = QGridLayout()
        self.thread_data = None
        self.plot = plot

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.stop_test_manager)

        self.start_time, self.stop_time = None, None

        self.user_dialog = QLabel()
        self.layout.addWidget(self.user_dialog,0,0)

        self.test_duration_input = QLineEdit()
        self.test_duration_input.setPlaceholderText("Test Duration (s)")
        self.test_duration_input.setValidator(QRegExpValidator(QRegExp('[0-9]+')))
        self.layout.addWidget(self.test_duration_input,1,0)

        self.test_rate_input = QLineEdit()
        self.test_rate_input.setPlaceholderText("Test Rate (ms)")
        self.test_rate_input.setValidator(QRegExpValidator(QRegExp('[0-9]+')))
        self.layout.addWidget(self.test_rate_input,1,1)

        self.ip_address_input = QLineEdit()
        self.ip_address_input.setPlaceholderText("Device IP Address")
        self.ip_address_input.setValidator(QRegExpValidator(QRegExp('^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$')))
        self.layout.addWidget(self.ip_address_input,2,0)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Device Port")
        self.port_input.setValidator(QRegExpValidator(QRegExp('[0-9]+')))
        self.layout.addWidget(self.port_input,2,1)

        self.start_test_button = QPushButton("Start Test")
        self.start_test_button.clicked.connect(self.start_test_manager)
        self.layout.addWidget(self.start_test_button,3,0)

        self.stop_test_button = QPushButton("End Test")
        self.stop_test_button.setEnabled(False) 
        self.stop_test_button.clicked.connect(self.stop_test_manager)
        self.layout.addWidget(self.stop_test_button,3,1)
        
        self.setLayout(self.layout)

    def start_test_manager(self):
        self.button_manager('start')

        user_input = [self.ip_address_input, self.port_input, self.test_duration_input, self.test_rate_input]

        if(self.verify_user_input(user_input)):
            self.start_time = datetime.datetime.now()

            self.timer.start(int(self.test_duration_input.text())*1000)

            self.thread_data = Worker(UDP_Client(user_input[0].text(), user_input[1].text(), user_input[2].text(), user_input[3].text()), parent=self)
            self.thread_data.server_data.connect(self.plot_data)
            self.thread_data.start()

            self.plot.plot_timer.start(10)

    def plot_data(self,x,y):
        self.plot.update_data(x,y)

    def stop_test_manager(self):
        self.thread_data.exit_session()
        self.button_manager('stop')
        self.stop_time = datetime.datetime.now()
        self.timer.stop()
        self.plot.plot_timer.stop()
        self.log_test_data()
        
    def button_manager(self, context):
        if(context == 'start'):
            self.stop_test_button.setEnabled(True)
            self.start_test_button.setEnabled(False)
        else:
            self.start_test_button.setEnabled(True)
            self.stop_test_button.setEnabled(False)
    
    def log_test_data(self):
        self.plot.figure.savefig('test.png')
        pdf = fpdf.FPDF()  
        pdf.add_page()
        pdf.set_font("Arial", size = 12)
        pdf.cell(200, 10, txt = ("Device IP Address: {}").format(self.ip_address_input.text()), ln = 1, align = 'C')
        pdf.cell(200, 10, txt = ("Device Port: {}").format(self.port_input.text()), ln = 2, align = 'C')
        pdf.cell(200, 10, txt = ("Test Duration: {}").format(self.test_duration_input.text()), ln = 3, align = 'C')
        pdf.cell(200, 10, txt = ("Device Rate: {}").format(self.test_rate_input.text()), ln = 4, align = 'C')
        pdf.cell(200, 10, txt = ("Execution Time: {}").format(self.stop_time-self.start_time), ln = 5, align = 'C')
        pdf.image('test.png', x=0, y=65, w=200, h=100)
        pdf.output("test_report.pdf") 

    def timeout_event(self):
        print("Test completed")
        self.stop_test_manager()
        self.log_test_data()

    def verify_user_input(self, user_input):
        for input in user_input:
            if(input.text() == ""):
                self.user_dialog.setText("Fill out each input to continue")
                self.stop_test_manager()
                return False
        return True