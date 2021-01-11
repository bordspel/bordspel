from bordspel.library.element import LayerManager
from bordspel.library.element.custom import *

from settings import *

class PhysicsDirection:

    NONE = "NONE"
    FULL = "FULL"
    RIGHT, LEFT = "RIGHT", "LEFT"
    UP, DOWN = "UP", "DOWN"

    def __init__(self, xVelocity, yVelocity):
        self.xVelocity = xVelocity
        self.yVelocity = yVelocity

class PhysicsBody:

    GRAVITY = 2
    AIR_RESISTANCE = 0.055

    def __init__(self, manager, layer, x, y, width, height, collidable=False, gravity=False, friction=False, bottomCollision=False, xOffset=False):
        self.manager = manager
        
        self.x = x
        self.y = y

        self.i = 0

        self.width = width
        self.height = height

        self.direction = PhysicsDirection(0, 0)

        self.collidable = collidable
        self.gravity = gravity
        self.friction = friction
        self.bottomCollision = bottomCollision
        self.xOffset = xOffset

        self.element = layer.createElement("", x, y)
        self.element.registerDrawListener(self.tick)

    # Bleeding
    def tick(self, layer, element):
        """
        Tick function to check for collisions.
        """
        x, y = CoordinatesUtil.toProcessingCoords(self.x, self.y)
        element.x = x
        element.y = y 

        for body in self.manager.bodies:
            if body != self and self.isColliding(body):
                if self.collidable:
                    relativeDirection = self.getDirectionRelativeToBody(body)

                    if self.getTotalYVelocity() <= 0:
                        newYVelocity = -self.getGravityVelocity()
                    else:
                        newYVelocity = self.direction.yVelocity

                    if relativeDirection[1] == "UP":
                        self.direction.yVelocity = newYVelocity

                    if relativeDirection[1] == "DOWN":
                        self.direction.yVelocity = 0
                        self.direction.xVelocity = 0
                    
                    # Bleeding
                    if (relativeDirection[0] == "RIGHT" or relativeDirection[0] == "LEFT") and relativeDirection[1] != "UP":
                        #print("no")
                        self.direction.xVelocity = 0

        self.applyDirection()


    def applyDirection(self):
        """
        Apply all the forces on the body.
        """
        self.x += self.direction.xVelocity
        self.y += self.direction.yVelocity + self.getGravityVelocity()

        if self.friction:
            if abs(self.direction.yVelocity) < self.AIR_RESISTANCE:
                self.direction.yVelocity = 0
            else:
                self.direction.yVelocity += -self.AIR_RESISTANCE if self.direction.yVelocity > 0 else self.AIR_RESISTANCE

    def getTotalXVelocity(self):
        """
        Returns the total X velocity.
        """
        return self.direction.xVelocity

    def getTotalYVelocity(self):
        """
        Returns the total Y velocity.
        Note: This includes gravity.
        """
        return self.direction.yVelocity + self.getGravityVelocity()

    def getGravityVelocity(self):
        """
        Returns the gravity velocity if enabled.
        """
        if self.gravity:
            return -self.GRAVITY
        return 0

    def getCenter(self):
        """
        Returns the center X and Y coordinate of the body.
        """
        return (self.x + self.width / 2, self.y + self.height / 2)

    def isColliding(self, body):
        """
        Checks if the body is colliding with another body/list of bodies.
        """
        if isinstance(body, list):
            return [self.isColliding(i) for i in body]

        if not self.collidable:
            return False

        xOffset = self.manager.minigame.marioMap.xOffset if self.xOffset else 0

        if self.bottomCollision:
            return self.x + xOffset < body.x + body.width and\
                self.x + xOffset + self.width > body.x and\
                self.y - self.height < body.y + body.height and\
                self.y > body.y

        return self.x + xOffset < body.x + body.width and\
            self.x + xOffset + self.width > body.x and\
            self.y < body.y + body.height and\
            self.y + self.height > body.y
    
    # Bleeding
    def getDirectionRelativeToBody(self, body):
        """
        Returns the direction relative to another body.
        """
        xOffset = self.manager.minigame.marioMap.xOffset if self.xOffset else 0

        xRight = body.x - xOffset < self.x + self.width and body.x + body.width - xOffset > self.x + self.width
        xLeft = self.x > body.x - xOffset and self.x < body.x + body.width - xOffset

        yTop = self.y > body.y 
        yBottom = self.y - self.height + 3 <= body.y

        xDirection = 0
        yDirection = 0

        if xRight:
            xDirection = PhysicsDirection.RIGHT
        if xLeft:
            xDirection = PhysicsDirection.LEFT
        if xRight and xLeft:
            xDirection = PhysicsDirection.FULL
        if not xRight or not xLeft:
            xDirection = PhysicsDirection.NONE

        if yTop:
            yDirection = PhysicsDirection.UP
        if yBottom:
            yDirection = PhysicsDirection.DOWN

        # print(xLeft)

        """
        xCollision = self.direction.xVelocity != 0 or body.direction.xVelocity != 0
        yCollision = self.gravity or self.direction.yVelocity != 0 or body.direction.yVelocity != 0 or body.gravity

        if xCollision:
            xDirection = PhysicsDirection.RIGHT if self.getCenter()[0] > body.getCenter()[0] else PhysicsDirection.LEFT
        else:
            xDirection = PhysicsDirection.NONE
        if yCollision:
            yDirection = PhysicsDirection.UP if self.getCenter()[1] > body.getCenter()[1] else PhysicsDirection.DOWN
        else:
            yDirection = PhysicsDirection.NONE
        """

        return [xDirection, yDirection]

    def getXDirectionRelativeToBody(self, body):
        xOffset = self.manager.minigame.marioMap.xOffset if self.xOffset else 0

        left = self.x + xOffset < body.x + body.width
        right = self.x + xOffset + self.width > body.x

        return (left, right)
        
class PhysicsManager:

    def __init__(self, minigame):
        self.minigame = minigame
        self.bodies = []

class CoordinatesUtil:

    @staticmethod
    def toProcessingCoords(x, y):
        return (x, screenHeight - y)

    @staticmethod
    def toRegularCoords(x, y):
        return (x, screenHeight - y)