from bordspel.library.element.custom import *

from manager.gameManager import gameManager
from settings import *

cursorReset = 0
usernames = []

import minigames.mario.mario
import minigames.steekspel.steekspel
import minigames.pong.pong

def playMiniGame(minigame):
    if minigame == "mario":
        minigames.mario.mario.MarioMinigame()
    if minigame == "steekspel":
        minigames.steekspel.steekspel.startSteekspel()
    if minigame == "pong":
        minigames.pong.pong.startGame()
    if minigame == "schietspel":
        pass

def draw(layer, element):
    gameManager.inGameCounter += 1

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

        gameManager.client.send("getChallenge", {})

    # Draw the 4 players.
    noFill()
    strokeWeight(1)
    stroke(144)

    rect(80, screenHeight / 2, 150, 100)
    rect(400, screenHeight / 2, 150, 100)
    rect(730, screenHeight / 2, 150, 100)
    rect(1050, screenHeight / 2, 150, 100)

    p1 = usernames[0][1] if len(usernames) >= 1 else "..."
    p2 = usernames[1][1] if len(usernames) >= 2 else "..."
    p3 = usernames[2][1] if len(usernames) >= 3 else "..."
    p4 = usernames[3][1] if len(usernames) >= 4 else "..."

    text1.setText(p1)
    text2.setText(p2)
    text3.setText(p3)
    text4.setText(p4)

    if btn1.hovering and p1 != gameManager.client.username and btn1.focused:
        gameManager.client.send("challenge", {"user1": gameManager.client.id, "user2": usernames[0][0]})
    if btn2.hovering and p2 != gameManager.client.username and btn2.focused:
        gameManager.client.send("challenge", {"user1": gameManager.client.id, "user2": usernames[1][0]})
    if btn3.hovering and p3 != gameManager.client.username and btn3.focused:
        gameManager.client.send("challenge", {"user1": gameManager.client.id, "user2": usernames[2][0]})
    if btn4.hovering and p4 != gameManager.client.username and btn4.focused:
        gameManager.client.send("challenge", {"user1": gameManager.client.id, "user2": usernames[3][0]})

def networkListener(client, data):
    global usernames, inGame

    if data["type"] == "members":
        usernames = data["usernames"]

    if data["type"] == "getChallenge":
        user1 = data["user1"]
        user2 = data["user2"]
        challenge = data["challenge"]

        if (user1 == client.id or user2 == client.id) and not gameManager.inGame and gameManager.inGameCounter > 300:
            gameManager.inGame = True

            playMiniGame(challenge)
            

lobbyLayer = gameManager.layerManager.createLayer("menu-lobby")

lobbyElement = lobbyLayer.createElement("lobby-element")
lobbyElement.registerDrawListener(draw)

lobbyWaitingText = Text("lobby-waiting", screenWidth / 2, 50, "Klik op een speler om hun uit te dagen in een duel!")
lobbyLayer.addElement(lobbyWaitingText)

"""
startButton = Button("lobby-start-game", screenWidth / 2 - 75, screenHeight / 2 - 30, 150, 60, (156, 39, 176), (187, 26, 214))
startButtonText = Text("lobby-start-gametext", screenWidth / 2, screenHeight / 2, "Start")
startButtonText.setColor(255)
startButtonText.setTextSize(22)

lobbyLayer.addElement(startButton)
lobbyLayer.addElement(startButtonText)
"""

text1 = Text("text1", 155, screenHeight / 2 + 50, "")
text2 = Text("text2", 475, screenHeight / 2 + 50, "")
text3 = Text("text3", 805, screenHeight / 2 + 50, "")
text4 = Text("text4", 1125, screenHeight / 2 + 50, "")

lobbyLayer.addElement(text1)
lobbyLayer.addElement(text2)
lobbyLayer.addElement(text3)
lobbyLayer.addElement(text4)

btn1 = Button("button1", 100, screenHeight / 2 + 120, 100, 50, (156, 39, 176), (187, 26, 214))
btn2 = Button("button2", 425, screenHeight / 2 + 120, 100, 50, (156, 39, 176), (187, 26, 214))
btn3 = Button("button3", 760, screenHeight / 2 + 120, 100, 50, (156, 39, 176), (187, 26, 214))
btn4 = Button("button4", 1080, screenHeight / 2 + 120, 100, 50, (156, 39, 176), (187, 26, 214))

lobbyLayer.addElement(btn1)
lobbyLayer.addElement(btn2)
lobbyLayer.addElement(btn3)
lobbyLayer.addElement(btn4)