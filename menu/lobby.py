from bordspel.library.element.custom import *

from manager.gameManager import gameManager
from settings import *

cursorReset = 0
usernames = []

def draw(layer, element):
    background("#ea87fa")
    image(gameManager.imageManager.getImage("./assets/menu/logo.png"), screenWidth - 300, 100, 200, 200)

    global cursorReset
    cursorReset += 1
    if cursorReset == 10 and cursorReset != -1:
        cursorReset = -1
        gameManager.client.register_listener(networkListener)
        gameManager.layerManager.activeCursors.clear()

    # Get the list of members.
    if frameCount % 120 == 0:
        gameManager.client.send("members", {})

    # Draw the usernames.
    fill("#e09beb")
    stroke(105)
    rect(50, 15, 150, 300)
    usernamesText.setText("\n\n".join(usernames))

def networkListener(client, data):
    global usernames

    if data["type"] == "members":
        usernames = data["usernames"]

lobbyLayer = gameManager.layerManager.createLayer("menu-lobby")

lobbyElement = lobbyLayer.createElement("lobby-element")
lobbyElement.registerDrawListener(draw)

lobbyWaitingText = Text("lobby-waiting", screenWidth / 2, 50, "Wanneer alle spelers zijn gejoind kan het spel worden gestart!")
lobbyLayer.addElement(lobbyWaitingText)

usernamesText = Text("lobby-usernames", 125, 100, "")
lobbyLayer.addElement(usernamesText)

startButton = Button("lobby-start-game", screenWidth / 2 - 75, screenHeight / 2 - 30, 150, 60, (156, 39, 176), (187, 26, 214))
startButtonText = Text("lobby-start-gametext", screenWidth / 2, screenHeight / 2, "Start")
startButtonText.setColor(255)
startButtonText.setTextSize(22)

lobbyLayer.addElement(startButton)
lobbyLayer.addElement(startButtonText)