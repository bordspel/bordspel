from manager.gameManager import gameManager

from minigames.mario.marioPlayer import MarioPlayer
from minigames.mario.marioMap import *
from minigames.mario.bodies import *

class MarioMinigame:

    def __init__(self):
        self.layer = gameManager.layerManager.createLayer("minigame-mario")
        gameManager.layerManager.setActiveLayerByName("minigame-mario")

        self.enemies = []

        self.physicsManager = PhysicsManager(self)

        self.marioMap = MarioMap(self, self.layer)
        self.enemies.append(MarioEnemy(self, self.layer, 650, 138, 850, 138))
        self.enemies.append(MarioEnemy(self, self.layer, 3025, 308, 3225, 308))
        self.marioTarget = MarioTarget(self, self.layer, 4000, 278, 50, 100)
        self.marioPlayer = MarioPlayer(self, self.layer, self.marioMap, 200, 200)

        self.keyListener = self.layer.createElement("minigame-mario-keylistener")
        self.keyListener.registerKeyListener(self.key)

        self.finished = False
        self.otherPlayerFinished = False

        self.speedX = 4
        self.key = ""

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

        if self.hitAnimation % 8 == 0:
            fill(220, 62, 25)
            rect(x - self.minigame.marioMap.xOffset, y, self.width, self.height)
        else:
            fill(255)
            rect(x - self.minigame.marioMap.xOffset, y, self.width, self.height)

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

        fill(0)
        rect(x, y, self.width, self.height)
        
        if self.isCollidingWithPlayer():
            self.minigame.finished = True

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

marioMinigame = MarioMinigame()