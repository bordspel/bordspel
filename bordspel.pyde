from settings import *

import menu.main
import menu.lobby

from manager.gameManager import gameManager

# playMiniGame("steekspel")

# Setup function.
def setup():
    size(screenWidth, screenHeight)
    # Note: Fullscreen requires scaling which is not implemented.
    # displayWidth and displayHeight need to be used.
    # fullScreen()

    # Define the GameManager.
    global gameManager

def stop():
    gameManager.client.send("exit", {})
    gameManager.client.close()

def draw():
    pass