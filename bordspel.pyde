from settings import *
from minigames.mario.mario import *

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
    pass
    # gameManager.client.close()

def draw():
    pass