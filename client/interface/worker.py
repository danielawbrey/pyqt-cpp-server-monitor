from PyQt5.QtCore import QThread, pyqtSignal

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
