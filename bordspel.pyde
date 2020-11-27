from settings import *

from element.listeners import *
from element.layer import Layer
from element.elements.button import Button
from element.elements.input import Input
from element.elements.text import Text
from element.elements.image import Image

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
    gameManager.layerManager.addLayer(menu)
    gameManager.layerManager.addLayer(game)
        
    # Select the current active Layer.
    background(255)
    gameManager.layerManager.setActiveLayer("menu")


def stop():
    gameManager.client.close()