from settings import screenWidth, screenHeight
from minigames.mario.bodies import PhysicsBody, CoordinatesUtil

from manager.gameManager import gameManager

class MarioMap:
    
    def __init__(self, minigame, layer):
        self.blocks = [
        MapBlock(0, 100, 300, 101)
        , MapBlock(500, 90, 1000, 91)
        , MapBlock(1150, 150, 1250, 151)
        , MapBlock(800, 220, 1100, 221)
        , MapBlock(1250, 280, 1500, 281)
        , MapBlock(1850, 310, 2000, 311)
        , MapBlock(2500, 200, 2700, 201)
        , MapBlock(3000, 260, 3300, 261)
        , MapBlock(3650, 280, 4200, 281)
        ]

        self.minigame = minigame
        self.layer = layer
        self.element = self.layer.createElement("MarioMap", 0, 0)
        self.element.registerDrawListener(self.draw)

        self.generateBodies()

        self.xOffset = 0
        self.xLeft, self.xRight = self.getFurthestLocations()

    def generateBodies(self):
        """
        Generates the bodies from the blocks to allow for physics interactions.
        """
        self.bodies = []

        for block in self.blocks:
            body = PhysicsBody(self.minigame.physicsManager, self.layer, block.sx, block.sy, block.ex - block.sx, block.sy - block.ey, collidable=True)
            self.bodies.append(body)

        self.minigame.physicsManager.bodies += self.bodies

    def getFurthestLocations(self):
        """
        Returns the furthest left and right x coordinate of the map.
        """
        xLeft = 0
        xRight = 0
        for block in self.blocks:
            if block.sx < xLeft:
                xLeft = block.sx
            if block.ex > xRight:
                xRight = block.ex

        return (xLeft, xRight)

    def isOnBorder(self):
        """
        Returns True if the offset is on a border (there is no more map available).
        """
        return self.xOffset <= self.xLeft or self.xOffset + screenWidth >= self.xRight

    def getBorderDirection(self):
        """
        Returns which border is the closest.
        """
        if self.xOffset <= self.xLeft:
            return "LEFT"
        if self.xOffset + screenWidth >= self.xRight:
            return "RIGHT"
        return "NONE"

    def getCurrentBlock(self):
        left, right = None, None

        for block in self.blocks:
            if left != None:
                right = block

            if self.minigame.marioPlayer.body.x + self.xOffset >= block.sx and block != right:
                left = block

    def draw(self, element, layer):
        # Draw the background.
        background(gameManager.imageManager.getImage("./assets/mario/background.png"))

        fill(0)
        for block in self.blocks:
            x1, y1 = CoordinatesUtil.toProcessingCoords(block.sx, block.sy)
            x2, y2 = CoordinatesUtil.toProcessingCoords(block.ex, block.ey)

            x1 -= self.xOffset
            x2 -= self.xOffset

            # line(x1, y1 + 7, x2, y1 + 7)
            strokeWeight(1)
            stroke(0)
            line(x1, y1 + 2, x2, y1 + 2)

class MapBlock:

    def __init__(self, sx, sy, ex, ey):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey