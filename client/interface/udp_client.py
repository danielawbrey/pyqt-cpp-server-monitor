import socket

class UDP_Client:
    def __init__(self, ip_address, device_port, test_duration, test_rate):
        self.ip_address = ip_address
        self.device_port = int(device_port)
        self.test_duration = int(test_duration)
        self.test_rate = int(test_rate)
        self.client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def send_message(self, message):   
        self.client_socket.sendto(str.encode(message), (self.ip_address, int(self.device_port)))

    def get_message_response(self):
        msgFromServer = self.client_socket.recvfrom(1024)
        print(("Message received {}").format(msgFromServer[0].decode('utf-8')))
        return msgFromServer