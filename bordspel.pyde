from settings import *

# import menu.main
# import menu.lobby

from manager.gameManager import gameManager

import minigames.mario.mario

def playMiniGame(minigame):
    if minigame == "mario":
        minigames.mario.mario.MarioMinigame()
    if minigame == "steekspel":
        pass
    if minigame == "pong":
        pass
    if minigame == "willem zn spel":
        pass

gameManager.connectToServer()

playMiniGame("mario")

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

def draw():
    pass