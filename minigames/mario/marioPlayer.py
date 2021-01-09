from settings import screenWidth, screenHeight
from manager.gameManager import gameManager
from minigames.mario.bodies import PhysicsBody

class MarioPlayer:

    def __init__(self, minigame, layer, map, startX, startY):
        self.minigame = minigame
        self.layer = layer
        self.map = map

        self.startX = startX
        self.startY = startY

        self.width = 36
        self.height = 50

        self.facing = "RIGHT"
        self.previousXOffset = 0

        self.started = False

        self.hp = 2
        self.timer = 0

        self.tooltipTimer = 0

        self.body = PhysicsBody(self.minigame.physicsManager, self.layer, startX, startY, self.width, self.height, collidable=True, friction=True, gravity=True, bottomCollision=True, xOffset=True)
        self.body.element.registerDrawListener(self.draw)
        self.body.element.registerKeyListener(self.key)
        self.minigame.physicsManager.bodies.append(self.body)

        self.reset(first=True)

    def draw(self, layer, element):
        # Draw the Player.
        # fill(77, 170, 46)
        # rect(element.x, element.y, self.width, self.height)

        playerImage = "./assets/mario/player.png"
        if self.body.direction.xVelocity != 0 or self.previousXOffset != self.map.xOffset:
            if (self.timer % 30) >= 15:
                playerImage = "./assets/mario/player-moving.png"

        if self.facing == "LEFT":
            pushMatrix()
            translate(self.width + element.x, 0)
            scale(-1, 1)
            image(gameManager.imageManager.getImage(playerImage), 0, element.y)
            popMatrix()
        else:
            image(gameManager.imageManager.getImage(playerImage), element.x, element.y)

        # Draw the tooltips at the start of the game.
        if self.tooltipTimer <= 300:
            if self.tooltipTimer < 150:
                image(gameManager.imageManager.getImage("./assets/mario/tooltip-movement.png"), element.x + self.width / 2 - 111, element.y - 50)
            if self.tooltipTimer >= 150:
                image(gameManager.imageManager.getImage("./assets/mario/tooltip-jump.png"), element.x + self.width / 2 - 110, element.y - 50)

            self.tooltipTimer += 1

        # Draw the hp.
        i = self.hp
        while i > 0:
            image(gameManager.imageManager.getImage("./assets/mario/heart.png"), i * 30, 10)

            i -= 1

        # Draw the timer.
        fill(0)
        textSize(30)
        text(str(round(self.timer / 60.0, 1)), screenWidth - 100, 75)

        if self.started:
            self.timer += 1

        # Check the keys.
        self.previousXOffset = self.map.xOffset

        if self.minigame.key == "a":
            self.started = True
            self.facing = "LEFT"

            if self.map.getBorderDirection() == "LEFT" or self.body.x > screenWidth / 2 - self.width:
                self.body.direction.xVelocity = -self.minigame.speedX
            else:
                self.body.direction.xVelocity = 0
                self.body.x = screenWidth / 2 - self.width

                self.map.xOffset += -self.minigame.speedX

        if self.minigame.key == "d":
            self.started = True
            self.facing = "RIGHT"

            if self.map.getBorderDirection() == "RIGHT" or self.body.x < screenWidth / 2 - self.width:
                self.body.direction.xVelocity = self.minigame.speedX
            else:
                self.body.direction.xVelocity = 0
                self.body.x = screenWidth / 2 - self.width

                self.map.xOffset += self.minigame.speedX

        if self.minigame.key != "a" and self.minigame.key != "d":
            self.body.direction.xVelocity = 0

        # Prevent moving outside of the map.
        if self.body.x <= 1 and self.minigame.key != "d":
            self.body.direction.xVelocity = 0

        if self.body.x + self.width >= (screenWidth - 4) and self.minigame.key != "a":
            self.body.direction.xVelocity = 0

        # If the Player fell out of map reset the map.
        if self.body.y < self.height:
            self.reset()

        # Check if the Player died.
        if self.hp <= 0:
            pass
            #TODO
            #element.hide()

    def reset(self, first=False):
        """
        Resets the Player and the Map.
        """
        self.body.x = self.startX
        self.body.y = self.startY

        if not first:
            self.hp -= 1

        self.map.xOffset = 0
    
    def jump(self):
        """
        Makes the Player jump.
        """
        self.body.direction.yVelocity = 5

    def isOnGround(self):
        """
        Returns True if the Player on the ground.
        """
        return True in self.body.isColliding(self.map.bodies)

    def key(self, event):
        # Detect the spacebar for jumps.
        if event.key == " " and event.type == "PRESS" and self.isOnGround():
            self.started = True
            self.jump()