import socket
import json
import threading
import random
import string

from settings import *

class Client:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listeners = []

        self.id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
        self.room = "room123"

    def register_listener(self, _callback):
        if _callback != None:
            self.listeners.append(_callback)

    def connect(self):
        self.sock.connect((socketIP, socketPort))
        
        self.listenerThread = threading.Thread(target=self.listen)
        self.listenerThread.start()

        self.send("handshake", {})

    def send(self, type, data):
        data["type"] = type
        data["id"] = self.id
        data["room"] = self.room
        self.sock.send(json.dumps(data))

    def listen(self):
        self.running = True
        self.sock.settimeout(5)

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