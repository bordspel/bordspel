from manager.gameManager import gameManager

from minigames.mario.marioPlayer import MarioPlayer, MarioEnemyPlayer
from minigames.mario.marioMap import *
from minigames.mario.bodies import *

from bordspel.library.element.custom import *

class MarioMinigame:

    def __init__(self):
        gameManager.layerManager.removeLayerByName("minigame-mario")
        self.layer = gameManager.layerManager.createLayer("minigame-mario")
        gameManager.layerManager.setActiveLayerByName("minigame-mario")

        self.enemies = []

        self.physicsManager = PhysicsManager(self)

        self.marioMap = MarioMap(self, self.layer)
        self.enemies.append(MarioEnemy(self, self.layer, 650, 138, 850, 138))
        self.enemies.append(MarioEnemy(self, self.layer, 3025, 308, 3225, 308))
        self.marioTarget = MarioTarget(self, self.layer, 4000, 278, 50, 100)

        self.marioEnemyPlayer = MarioEnemyPlayer(self, self.layer, 200, 200)
        self.marioPlayer = MarioPlayer(self, self.layer, self.marioMap, 200, 200)

        self.keyListener = self.layer.createElement("minigame-mario-keylistener")
        self.keyListener.registerKeyListener(self.key)

        self.finished = False

        self.speedX = 4
        self.key = ""

        gameManager.client.register_listener(self.networkListener)

    def showEndScreen(self, winner):
        self.endScreen = MarioEndScreen(self, self.layer, winner)

    def key(self, event):
        if event.type == "PRESS":
            if event.key == "a":
                self.key = "a"
            if event.key == "d":
                self.key = "d"
        if event.type == "RELEASE":
            if event.key == "a":
                 self.key = ""
            if event.key == "d":
                 self.key = ""

    def networkListener(self, client, data):
        if data["type"] == "mario" and data["action"] == "win":
            winner = data["player"] == gameManager.client.id

            if not self.finished:
                self.finished = True

                self.hide()

                self.showEndScreen(winner)

    def hide(self):
        self.marioMap.element.unregisterDrawListener(self.marioMap.draw)

        for enemy in self.enemies:
            enemy.element.unregisterDrawListener(enemy.draw)

        self.marioEnemyPlayer.element.unregisterDrawListener(self.marioEnemyPlayer.draw)

        self.marioPlayer.body.element.unregisterDrawListener(self.marioPlayer.draw)
        self.marioPlayer.body.element.unregisterKeyListener(self.marioPlayer.key)

        self.keyListener.unregisterKeyListener(self.key)

        self.marioTarget.element.unregisterDrawListener(self.marioTarget.draw)

class MarioEnemy:

    def __init__(self, minigame, layer, xStart, yStart, xEnd, yEnd):
        self.minigame = minigame
        self.layer = layer

        self.body = PhysicsBody(minigame.physicsManager, layer, xStart, yStart, 100, 100)

        self.xStart = xStart
        self.yStart = yStart

        self.xEnd = xEnd
        self.yEnd = yEnd

        self.width = 50
        self.height = 50

        self.hitAnimation = 0

        self.element = self.layer.createElement("MarioEnemy", xStart, yStart)
        self.element.registerDrawListener(self.draw)

    def draw(self, layer, element):
        x, y = CoordinatesUtil.toProcessingCoords(self.body.x, self.body.y)

        # Switch direction when the Enemy is out of their area.
        if self.body.x + self.width <= self.xStart + self.width:
            self.body.direction.xVelocity = 1
        if self.body.x >= self.xEnd:
            self.body.direction.xVelocity = -1

        # When the Player collides with the enemy show the animation and remove a heart.
        if self.isCollidingWithPlayer() and self.hitAnimation == 0:
            self.hitAnimation += 1
            self.minigame.marioPlayer.hp -= 1

        if self.hitAnimation > 0:
            self.hitAnimation += 1

            if self.hitAnimation > 60:
                self.hitAnimation = 0

        if self.hitAnimation % 20 < 10:
            if self.body.direction.xVelocity == 1:
                pushMatrix()
                translate(x - self.minigame.marioMap.xOffset, 0)
                scale(-1, 1)
                image(gameManager.imageManager.getImage("./assets/mario/guard.png"), 0, y + 3, self.width, self.height)
                popMatrix()
            else:
                pushMatrix()
                translate(x - self.minigame.marioMap.xOffset, 0)
                image(gameManager.imageManager.getImage("./assets/mario/guard.png"), 0, y + 3, self.width, self.height)
                popMatrix()
                
    def isCollidingWithPlayer(self):
        """
        Returns True if this enemy is colliding with the Player.
        """
        px, py = self.minigame.marioPlayer.body.x, self.minigame.marioPlayer.body.y
        w, h = self.minigame.marioPlayer.width, self.minigame.marioPlayer.height
        xOffset = self.minigame.marioMap.xOffset

        return px + xOffset < self.body.x + self.width and\
            px + xOffset + w > self.body.x and\
            py < self.body.y + self.height and\
            py + h > self.body.y

class MarioTarget:

    def __init__(self, minigame, layer, x, y, width, height):
        self.minigame = minigame
        self.layer = layer

        self.x = x
        self.y = y + height

        self.width = width
        self.height = height

        self.element = self.layer.createElement("MarioTarget")
        self.element.registerDrawListener(self.draw)

    def draw(self, layer, element):
        xOffset = self.minigame.marioMap.xOffset
        x, y = CoordinatesUtil.toProcessingCoords(self.x, self.y)
        x -= xOffset

        # Draw the castle
        image(gameManager.imageManager.getImage("./assets/mario/castle.png"), x, y, self.width, self.height)

        # fill(0)
        # rect(x, y, self.width, self.height)
        
        if self.isCollidingWithPlayer():

            for i in range(0, 61):
                gameManager.client.send("mario", {"action": "win", "player": gameManager.client.id})

    def isCollidingWithPlayer(self):
        """
        Returns True if this enemy is colliding with the Player.
        """
        px, py = self.minigame.marioPlayer.body.x, self.minigame.marioPlayer.body.y
        w, h = self.minigame.marioPlayer.width, self.minigame.marioPlayer.height
        xOffset = self.minigame.marioMap.xOffset

        return px + xOffset < self.x + self.width and\
            px + xOffset + w > self.x and\
            py < self.y + self.height and\
            py + h > self.y

class MarioEndScreen:

    def __init__(self, minigame, layer, winner):
        self.minigame = minigame
        self.layer = layer

        self.counter = self.layer.createElement("counter")
        self.counter.registerDrawListener(self.tick)

        self.count = 0

        if winner:
            result = "Je hebt gewonnen!"
            result2 = "Je krijgt 15 Dukaten en 1 Charisma."
        else:
            result = "Je hebt verloren!"
            result2 = "Je verliest 15 Dukaten en 1 Charisma."

        self.text = Text("TextEndScreen", screenWidth / 2, screenHeight / 2 - 50, result)
        self.text.setTextSize(40)

        self.text2 = Text("TextEndScreen", screenWidth / 2, screenHeight / 2 + 50, result2)
        self.text2.setTextSize(30)

        self.layer.addElement(self.text)
        self.layer.addElement(self.text2)

    def tick(self, layer, element):
        background(gameManager.imageManager.getImage("./assets/mario/background.png"))
        self.count += 1

        if self.count >= 360:
            self.layer.removeElement(self.text)
            self.layer.removeElement(self.text2)

            gameManager.inGame = False
            gameManager.inGameCounter = 0

            self.counter.unregisterDrawListener(self.tick)

            # Switch the layer back to the lobby.
            gameManager.layerManager.setActiveLayerByName("menu-lobby")