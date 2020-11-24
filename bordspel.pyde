from settings import *

from elements.layer import *
from elements.element import *
from elements.button import *
from elements.input import *
from elements.text import *

from manager.gameManager import gameManager

# Setup function.
def setup():
    size(screenWidth, screenHeight)
    # Note: Fullscreen requires scaling which is not implemented.
    # displayWidth and displayHeight need to be used.
    # fullScreen()

    # Define the GameManager.
    global gameManager
    # gameManager.imageManager.loadImage("sketch.png")
    # gameManager.audioManager.loadAudio("audio.mp3")
    # gameManager.audioManager.getAudio("audio.mp3").play()

    # Create the Layers with their respective elements.
    menu = Layer("menu")
    menu.addElement(Text("#text2", x=10, y=45, text="Name").horizontal(LEFT).textcolor("#757575").textsize(16))
    menu.addElement(Input("#input1", x=10, y=60, w=200, h=35, textSize=14))

    menu.addElement(Button("#button1", x=10, y=125, w=100, h=35).base("#4CAF50").highlight("#3e8e41"))
    menu.addElement(Text("#text1", x=60, y=140, text="Submit").textcolor("#FFFFFFF").textsize(16))
    
    game = Layer("game")
    game.addElement(Button("#button1", x=200, y=10, w=200, h=100, baseColor="#4CAF50", highlightColor="#3e8e41"))
    game.addElement(Text("#text1", x=300, y=60, text="Go to layer1", textSize=16, color="#FFFFFFF"))
        
    # Add the Layers to the LayerManager.
    layerManager.addLayer(menu)
    layerManager.addLayer(game)
        
    # Select the current active Layer.
    background(255)
    layerManager.setActiveLayer("menu")


def stop():
    gameManager.client.close()