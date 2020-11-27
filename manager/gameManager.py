from manager.imageManager import ImageManager
from manager.audioManager import AudioManager
from manager.dependencyManager import DependencyManager
from manager.layerManager import LayerManager

from networking.client import *

class GameManager:
    
    def __init__(self):
        self.imageManager = ImageManager()
        self.audioManager = AudioManager()
        self.dependencyManager = DependencyManager()
        
        self.dependencyManager.addDependency("websocket")
        self.dependencyManager.installDependencies()

        self.layerManager = LayerManager()

        self.client = Client()
        # self.client.connect()

gameManager = GameManager()