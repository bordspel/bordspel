from bordspel.library.element.custom import *
from custom.input import Input

from settings import *
from manager.gameManager import gameManager

def draw(layer, element):
    background("#d8a6e0")
    image(gameManager.imageManager.getImage("./assets/menu/logo.png"), screenWidth - 300, 100, 200, 200)

def mouse(event):
    if event.type == "CLICK" and event.button == "LEFT":

        if button.focused:
            if len(input.text) == 0:
                return

            gameManager.client.username = input.text

            # Connect to the server.
            gameManager.layerManager.setActiveLayerByName("menu-lobby")
            gameManager.connectToServer()

mainMenuLayer = gameManager.layerManager.createLayer("menu-main")

mainMenuElement = mainMenuLayer.createElement("menu-main")
mainMenuElement.registerDrawListener(draw)
mainMenuElement.registerMouseListener(mouse)

input = Input(mainMenuLayer, screenWidth / 2 - 75, 325, 150, 35)

button = Button("menu-main-startButton", screenWidth / 2 - 75, 400, 150, 60, (156, 39, 176), (187, 26, 214))
buttonText = Text("menu-main-startText", screenWidth / 2, 430, "Spelen")
buttonText.setColor(255)
buttonText.setTextSize(22)

naamText = Text("menu-main-invalidnaam", screenWidth / 2 - 50, 310, "Naam")
naamText.setColor(105)

mainMenuLayer.addElement(button)
mainMenuLayer.addElement(buttonText)
mainMenuLayer.addElement(naamText)

gameManager.layerManager.setActiveLayerByName("menu-main")