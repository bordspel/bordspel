from bordspel.library.element.custom import *

from settings import *
from manager.gameManager import gameManager

def draw(layer, element):
    image(gameManager.imageManager.getImage("./assets/menu/main-background.png"), 0, 0)

def mouse(event):
    if event.type == "CLICK" and event.button == "LEFT":

        if button.focused:
            # TODO: Implement the screen where you enter your name and join the lobby
            pass 

mainMenuLayer = gameManager.layerManager.createLayer("menu-main")

mainMenuElement = mainMenuLayer.createElement("menu-main")
mainMenuElement.registerDrawListener(draw)
mainMenuElement.registerMouseListener(mouse)

button = Button("menu-main-startButton", screenWidth / 2 - 75, 400, 150, 60, (66, 105, 245), (66, 158, 245))
buttonText = Text("menu-main-startText", screenWidth / 2, 430, "Spelen")
# buttonText.setColor(255)
buttonText.setTextSize(22)

mainMenuLayer.addElement(button)
mainMenuLayer.addElement(buttonText)

# gameManager.layerManager.setActiveLayerByName("menu-main")