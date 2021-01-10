# http://pypi.python.org/pypi/websocket-client/
# from websocket import *
from settings import *

import socket
import json
import threading
import random
import string

class Client:

    def __init__(self):
        self.listeners = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
        self.room = "room123"

    def register_listener(self, _callback):
        if _callback != None:
            self.listeners.append(_callback)

    def connect(self):
        try:
            # self.sock = create_connection("ws://localhost:8080")
            self.sock.connect((socketIP, socketPort))
            
            self.listenerThread = threading.Thread(target=self.listen)
            self.listenerThread.start()
        except:
            print("Connection failed while trying to connect to the server.")

        self.send("handshake", {})

    def send(self, type, data):
        data["type"] = type
        data["id"] = self.id
        data["room"] = self.room

        try:
            self.sock.send(json.dumps(data))
        except:
            print("Exception while trying to send data to the server.")

    def listen(self):
        self.running = True
        self.sock.settimeout(3)

        while self.running:
            try:
                message = self.sock.recv(4096)

                if message != None:
                    message = json.loads(message)
                    for l in self.listeners:
                        l(self, message)
            except:
                pass

    def close(self):
        self.send("exit", {})

        self.running = False
        self.sock.close()

def listen(client, data):
    print(data)