from settings import *
from minigames.mario.mario import *

import menu.main
import menu.beforeLobby

from manager.gameManager import gameManager

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