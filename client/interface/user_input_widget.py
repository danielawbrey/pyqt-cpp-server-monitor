from PyQt5.QtWidgets import QPushButton, QWidget, QLineEdit, QGridLayout, QLabel
from PyQt5.QtCore import QTimer, QRegExp
from PyQt5.QtGui import QRegExpValidator

class User_Input_Widget(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.stop_test_manager)

        self.init_ui()

    def init_ui(self):
        self.layout = QGridLayout()

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
        self.toggle_buttons(True)
        self.timer.start(int(self.test_duration_input.text())*1000)
        user_input = [self.ip_address_input, self.port_input, self.test_duration_input, self.test_rate_input]

        if(self.verify_user_input(user_input)):
            self.parent.start_test_manager(user_input)

    def stop_test_manager(self):
        self.timer.stop()
        self.toggle_buttons(False)
        self.parent.stop_test_manager()
    
    def toggle_buttons(self, context):
        self.stop_test_button.setEnabled(context)
        self.start_test_button.setEnabled(not context)
    
    def verify_user_input(self, user_input):
        for input in user_input:
            if(input.text() == ""):
                self.user_dialog.setText("Fill out each input to continue")
                self.toggle_buttons(False)
                return False
        return True