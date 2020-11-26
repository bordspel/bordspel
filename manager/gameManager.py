from manager.imageManager import ImageManager
from manager.audioManager import AudioManager
from manager.dependencyManager import DependencyManager

from networking.client import *

class GameManager:
    
    def __init__(self):
        self.imageManager = ImageManager()
        self.audioManager = AudioManager()
        self.dependencyManager = DependencyManager()
        
        self.dependencyManager.addDependency("websocket")
        self.dependencyManager.installDependencies()

        self.client = Client()
        # self.client.connect()

gameManager = GameManager()