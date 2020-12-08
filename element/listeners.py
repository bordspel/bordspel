from manager.gameManager import gameManager

from settings import *

"""
Do not use these functions. Use the Element and Layer system.
These functions listen for the various events in the window and fire the correct event handlers.
"""
def draw():
    background(255)
    
    # Used for debug.
    if DEBUG:
        textSize(12)
        textAlign(RIGHT, BOTTOM)
        fill(0)
        s = "Layer: " + str(gameManager.layerManager.getActiveLayerName())
        text(s, screenWidth, screenHeight)
        
    # Used to reset the cursor.
    if len(gameManager.layerManager.customCursors) == 0:
        cursor(ARROW)
    
    gameManager.layerManager.__callDraw__()

def mouseClicked():
    gameManager.layerManager.__callMouse__("click")
    
def mouseMoved():
    gameManager.layerManager.__callMouse__("move")
        
def mousePressed():
    gameManager.layerManager.__callMouse__("pressed")
       
def mouseReleased():
    gameManager.layerManager.__callMouse__("released")
    
def keyTyped():
    gameManager.layerManager.__callKey__("typed")
    
# This doesn't work for some reason.
# https://py.processing.org/reference/keyPressed.html
def keyReleased():
    gameManager.layerManager.__callKey__("released")

def keyPressed():
    gameManager.layerManager.__callKey__("pressed")