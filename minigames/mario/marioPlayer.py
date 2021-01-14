from settings import screenWidth, screenHeight
from manager.gameManager import gameManager
from minigames.mario.bodies import PhysicsBody, CoordinatesUtil

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

        self.hp = 3
        self.timer = 0

        self.tooltipTimer = 0
        self.moving = False

        self.body = PhysicsBody(self.minigame.physicsManager, self.layer, startX, startY, self.width, self.height, collidable=True, friction=True, gravity=True, bottomCollision=True, xOffset=True)
        self.body.element.registerDrawListener(self.draw)
        self.body.element.registerKeyListener(self.key)
        self.minigame.physicsManager.bodies.append(self.body)

        self.reset(first=True)

    def draw(self, layer, element):
        # Draw the Player.
        # fill(77, 170, 46)
        # rect(element.x, element.y, self.width, self.height)

        playerImage = "./assets/mario/horse_blue.png"
        if self.body.direction.xVelocity != 0 or self.previousXOffset != self.map.xOffset:
            self.moving = True
            if (self.timer % 30) >= 15:
                playerImage = "./assets/mario/horse_blue_moving.png"
        else:
            self.moving = False

        if self.facing == "LEFT":
            pushMatrix()
            translate(self.width + element.x, 0)
            scale(-1, 1)
            image(gameManager.imageManager.getImage(playerImage), 0, element.y, self.width, self.height)
            popMatrix()
        else:
            image(gameManager.imageManager.getImage(playerImage), element.x, element.y, self.width, self.height)

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
            for i in range(0, 61):
                gameManager.client.send("mario", {"action": "win", "player": ""})

            self.minigame.finished = True
            self.minigame.hide()
            self.minigame.showEndScreen(False)

        # Send the position of the Player to the client.
        if frameCount % 3 == 0:
            gameManager.client.send("mario", {"action": "position", "player": gameManager.client.id, "x": self.body.x, "y": self.body.y, "xOffset": self.map.xOffset, "direction": self.facing, "moving": self.moving})
    
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
        
class MarioEnemyPlayer:

    def __init__(self, minigame, layer, x, y):
        self.layer = layer
        self.minigame = minigame

        self.x, self.y = CoordinatesUtil.toProcessingCoords(x, y)
        self.xOffset = 0
        self.direction = "RIGHT"
        self.moving = False

        self.width = 36
        self.height = 50

        self.element = self.layer.createElement("MarioEnemyPlayer", self.x, self.y)
        self.element.registerDrawListener(self.draw)

        gameManager.client.register_listener(self.networkListener)

    def draw(self, layer, element):
        playerImage = "./assets/mario/horse_red.png"
        if self.moving:
            if (frameCount % 30) >= 15:
                playerImage = "./assets/mario/horse_red_moving.png"

        if self.direction == "LEFT":
            pushMatrix()
            translate(self.width + element.x - self.minigame.marioMap.xOffset + self.xOffset, 0)
            scale(-1, 1)
            image(gameManager.imageManager.getImage(playerImage), 0, element.y + self.height, self.width, self.height)
            popMatrix()
        else:
            image(gameManager.imageManager.getImage(playerImage), element.x - self.minigame.marioMap.xOffset + self.xOffset, element.y + self.height, self.width, self.height)
        
    def networkListener(self, client, data):
        if data["type"] == "mario" and data["action"] == "position":
            if data["player"] != client.id:
                x, y = CoordinatesUtil.toProcessingCoords(data["x"], data["y"] + self.height)
                self.xOffset = data["xOffset"]
                self.direction = data["direction"]
                self.moving = data["moving"]

                self.element.x = x
                self.element.y = y