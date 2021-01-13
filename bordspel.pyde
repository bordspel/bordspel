from settings import *
# sfrom minigames.mario.mario import *
from minigames.schietspel.schietspel import Archer, SchietspelMinigame

import menu.main
import menu.beforeLobby

from manager.gameManager import gameManager

from custom.input import *

# layer = gameManager.layerManager.createLayer("aaaa")
# gameManager.layerManager.setActiveLayerByName("aaaa")

# i = Input(layer, 100, 100, 300, 100, textColor=255)

# Setup function.
def setup():
    size(screenWidth, screenHeight)
    # Note: Fullscreen requires scaling which is not implemented.
    # displayWidth and displayHeight need to be used.
    # fullScreen()

    # Define the GameManager.
    global gameManager
        
    # Select the current active Layer.
    background(255)


def stop():
    gameManager.client.send("exit", {})
    gameManager.client.close()

def draw():
    pass