from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLineEdit, QGridLayout, QLabel
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QRegExp
from PyQt5.QtGui import QRegExpValidator
import sys
import time
import datetime
import udp_client
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import fpdf

class Worker(QThread):
    server_data = pyqtSignal(int,int)
    exit_server = pyqtSignal(object)
    finished = pyqtSignal(int)

    def __init__(self, udp_client, parent):
        super().__init__(parent)
        self.udp_client = udp_client
        self.thread_running = True
    
    def run(self):
        self.udp_client.send_message("1;")
        self.udp_client.get_message_response()
        test_description = ("TEST;CMD=START;DURATION={};RATE={};").format(self.udp_client.test_duration, self.udp_client.test_rate)
        self.udp_client.send_message(test_description)
        self.udp_client.get_message_response()

        while self.thread_running:
            data = self.udp_client.get_message_response()
            data = data[0].decode('utf-8').split(';')
            self.udp_client.send_message("Data received")
            self.server_data.emit(int(data[0]), int(data[1]))
            time.sleep(0.1)

    def exit_session(self):
        self.thread_running = False
        self.udp_client.send_message("TEST;CMD=STOP;")
        self.udp_client.get_message_response()
        self.udp_client.get_message_response()

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.start_time, self.stop_time = None, None
        self.layout = QGridLayout()
        self.plot = Plot_Widget()
        self.layout.addWidget(self.plot)
        self.user_input_widget = User_Input_Widget(self.plot)
        self.layout.addWidget(self.user_input_widget)
        self.setLayout(self.layout)

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
        self.stop_test_button.setEnabled(False) # Display button but don't enable until test has 
        self.stop_test_button.clicked.connect(self.stop_test_manager)
        self.layout.addWidget(self.stop_test_button,3,1)
        
        self.setLayout(self.layout)

    def start_test_manager(self):
        self.button_manager('start')
        # self.plot.clear()
        user_input = [self.ip_address_input, self.port_input, self.test_duration_input, self.test_rate_input]

        if(self.verify_user_input(user_input)):
            self.start_time = datetime.datetime.now()

            self.timer.start(int(self.test_duration_input.text())*1000) # Convert to seconds per requirements

            self.thread_data = Worker(udp_client.UDP_Client(user_input[0].text(), user_input[1].text(), user_input[2].text(), user_input[3].text()), parent=self)
            self.thread_data.server_data.connect(self.plot_data)
            self.thread_data.start()

            self.plot.clear_data()
            self.plot.plot_timer.start(10)

    def plot_data(self,x,y):
        self.plot.update_data(x,y)

    def stop_test_manager(self):
        self.stop_time = datetime.datetime.now()
        self.button_manager('stop')
        self.thread_data.exit_session()
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
        self.axes.cla()  # Clear the canvas.
        self.axes.plot(self.xdata, self.ydata, 'r')
        self.fig.canvas.draw_idle()
        
    def clear_data(self):
        self.axes.clear()
        self.xdata = []
        self.ydata = []

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.showMaximized()
    sys.exit(app.exec_())