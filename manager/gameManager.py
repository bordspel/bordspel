from manager.imageManager import ImageManager
from manager.audioManager import AudioManager
from manager.dependencyManager import DependencyManager

from bordspel.library.element import LayerManager
# from bordspel.library.element.custom import *

from networking.client import *

class GameManager:
    
    def __init__(self):
        self.imageManager = ImageManager()
        self.audioManager = AudioManager()
        self.dependencyManager = DependencyManager()

        self.client = Client()

        self.inGame = False
        self.inGameCounter = 500
        
        # self.dependencyManager.addDependency("websocket")
        # self.dependencyManager.installDependencies()

        # self.layerManager = LayerManager()
        self.layerManager = LayerManager(this)
        
        # All Menu images.
        self.imageManager.loadImage("./assets/menu/logo.png")

        # All Mario images.
        self.imageManager.loadImage("./assets/mario/heart.png")

        self.imageManager.loadImage("./assets/mario/tooltip-movement.png")
        self.imageManager.loadImage("./assets/mario/tooltip-jump.png")

        self.imageManager.loadImage("./assets/mario/horse_blue.png")
        self.imageManager.loadImage("./assets/mario/horse_red.png")

        self.imageManager.loadImage("./assets/mario/horse_blue_moving.png")
        self.imageManager.loadImage("./assets/mario/horse_red_moving.png")

        self.imageManager.loadImage("./assets/mario/guard.png")

        self.imageManager.loadImage("./assets/mario/castle.png")
        self.imageManager.loadImage("./assets/mario/background.png")
        

    def connectToServer(self):
        self.client.connect()

gameManager = GameManager()