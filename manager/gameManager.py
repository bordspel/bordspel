from manager.imageManager import ImageManager
from manager.audioManager import AudioManager

from networking.client import *

class GameManager:
    
    def __init__(self):
        self.imageManager = ImageManager()
        self.audioManager = AudioManager()

        self.client = Client()

gameManager = GameManager()