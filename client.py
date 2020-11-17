import socket
import threading
from settings import *

class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listeners = []

    def register_listener(self, _callback):
        if _callback != None:
            self.listeners.append(_callback)

    def connect(self):
        self.sock.connect((socketIP, socketPort))
        
        self.listenerThread = threading.Thread(target=self.listen)
        self.listenerThread.start()

    def send(self, data):
        self.sock.send(data)

    def listen(self):
        self.running = True
        self.sock.settimeout(5)

        while self.running:
            try:
                message = self.sock.recv(4096)
                for l in self.listeners:
                    l(self, message)
            except:
                pass

    def close(self):
        self.running = False
        self.sock.close()