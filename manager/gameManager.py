from manager.imageManager import ImageManager
from manager.audioManager import AudioManager

class GameManager:
    
    def __init__(self):
        self.imageManager = ImageManager()
        self.audioManager = AudioManager()

gameManager = GameManager()