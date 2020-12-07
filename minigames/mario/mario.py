from manager.gameManager import gameManager
from settings import screenWidth

class MarioMinigame:

    def __init__(self):
        self.layer = gameManager.layerManager.createLayer("minigame-mario")
        gameManager.layerManager.setActiveLayerByName("minigame-mario")

        self.marioMap = MarioMap(self, self.layer)
        #self.marioEnemy = MarioEnemy(self.layer, 100, 300, 400, 300)
        self.marioPlayer = MarioPlayer(self, self.layer, self.marioMap, 200, 350)

        self.keyListener = self.layer.createElement("minigame-mario-keylistener")
        self.keyListener.registerKeyListener(self.key)

        self.speedX = 12
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

class MarioMap:

    def __init__(self, minigame, layer):
        self.floor = [(i, 400) for i in range(-500, 500)] + [(i, 350) for i in range(500, 1000)]
        
        self.minigame = minigame
        self.layer = layer
        self.element = self.layer.createElement("MarioMap", 0, 0)
        self.element.registerDrawListener(self.draw)

        self.directionX = 0
        self.xOffset = 0

    def getVisibleFloor(self):
        visibleFloor = []
        for i in range(int(self.xOffset), int(self.xOffset) + screenWidth + 1):
            f = self.floor[i]
            visibleFloor.append((i - int(self.xOffset), f[1]))
        return visibleFloor

    def isMoreFloor(self):
        if self.xOffset + self.minigame.speedX >= self.floor[-1][0]:
            return False
        if self.xOffset - self.minigame.speedX + screenWidth <= self.floor[0][0]:
            return False
        return True

    def draw(self, element, layer):
        for f in self.getVisibleFloor():
            point(f[0], f[1])

        if self.minigame.key == "a":
            self.directionX = -self.minigame.speedX
        elif self.minigame.key == "d":
            self.directionX = self.minigame.speedX
        else:
            self.directionX = 0

        if self.isMoreFloor():
            self.xOffset += self.directionX


class MarioPlayer:

    def __init__(self, minigame, layer, map, startX, startY):
        self.minigame = minigame
        self.layer = layer
        self.map = map

        self.startX = startX
        self.startY = startY

        self.width = 50
        self.height = 50

        self.directionY = 0
        self.directionX = 0

        self.jumpY = 0
        self.inJump = False

        self.element = self.layer.createElement("MarioPlayer", self.startX, self.startY)
        self.element.registerDrawListener(self.draw)
        self.element.registerKeyListener(self.key)
    
    def jump(self):
        self.directionY = -2
        self.jumpY = self.element.y - 100
        self.inJump = True

    def draw(self, layer, element):
        rect(element.x, element.y, self.width, self.height)

        if self.map.xOffset > 0 and element.x < self.startX:
            self.map.xOffset -= self.minigame.speedX
        if self.map.xOffset < 0 and element.x + self.width > screenWidth - self.startX:
            self.map.xOffset += self.minigame.speedX

        # Get the floor at the left and right of the Player hitbox.
        left = [c for c in self.map.getVisibleFloor() if c[0] == int(element.x)][0]
        right = [c for c in self.map.getVisibleFloor() if c[0] == int(element.x) + self.width][0]
        
        # Prevent the x from going outside of the map.
        if element.x + self.directionX <= 1 or element.x + self.directionX >= screenWidth:
            self.directionX = 0

        # Prevent the Player from going through the floor.
        if (element.y + self.height >= left[1] or element.y + self.height >= right[1]) and self.directionY > 0:
            self.directionY = 0
            self.inJump = False

        # Prevent the Player from going up the floor.
        # TODO.

        # Let the player fall when they are not on the floor.
        if element.y + self.height != left[1] and element.y + self.height != right[1] and not self.inJump:
            self.directionY = 2

        # When the player jumps ensure that they come back to the ground.
        if self.directionY < 0:
            if element.y <= self.jumpY and self.inJump:
                self.directionY = 2

        # Check the keys.
        if not self.map.isMoreFloor():
            if self.minigame.key == "a":
                self.directionX = -self.minigame.speedX
            elif self.minigame.key == "d":
                self.directionX = self.minigame.speedX
            else:
                self.directionX = 0

        # Prevent the Player from going outside of the map.
        if not self.map.isMoreFloor():
            if element.x + self.width + self.directionX >= screenWidth:
                self.directionX = 0
            if element.x + self.directionX <= 0:
                self.directionX = 0
            element.x += self.directionX
        else:
            # self.map.directionX = self.directionX
            self.directionX = 0
            element.x = self.startX

        element.y += self.directionY

    def key(self, event):
        # Detect the spacebar for jumps.
        if event.key == " " and not self.inJump and event.type == "PRESS":
            self.jump()

            

class MarioEnemy:

    def __init__(self, layer, xStart, yStart, xEnd, yEnd):
        self.layer = layer

        self.xStart = xStart
        self.yStart = yStart

        self.xEnd = xEnd
        self.yEnd = yEnd

        self.width = 100
        self.height = 100

        self.direction = 1

        self.element = self.layer.createElement("MarioEnemy", xStart, yStart)
        self.element.registerDrawListener(self.draw)

    def draw(self, layer, element):
        rect(element.x, element.y, 50, 50)
        if element.x + self.width <= self.xStart + self.width:
            self.direction = 1
        if element.x >= self.xEnd:
            self.direction = -1
        element.x += self.direction

marioMinigame = MarioMinigame()