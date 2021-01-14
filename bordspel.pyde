from settings import *

import menu.main
import menu.lobby

from manager.gameManager import gameManager

# menu.lobby.playMiniGame("schietspel")

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

    textFont(createFont("./assets/schietspel/Londrina.ttf", 192))

def stop():
    gameManager.client.send("exit", {})
    gameManager.client.close()

def draw():
    pass