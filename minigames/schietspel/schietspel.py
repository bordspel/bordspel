from manager.gameManager import gameManager
from random import random
from time import time

class Archer():
    def __init__(self, parent, dir=1):
        self.parent = parent
        self.pos = PVector(0, 0)
        self.dir = dir
        parent.elements.append(self)
    
    def draw(self):
        fill(self.parent.brown)
        noStroke()
        pushMatrix()
        translate(self.pos.x-64*self.dir, self.pos.y-133)
        scale(self.dir, 1)
        image(gameManager.imageManager.getImage("./assets/schietspel/horse.png"), 0, 0)
        popMatrix()

class Arrow:
    def __init__(self, pos, vel, player):
        self.pos = pos
        self.prevPos = pos.copy()
        self.vel = vel
        self.player = player
        self.stuck = False
        self.g = PVector(0, 500)
    
    def draw(self):
        pushMatrix()
        translate(self.pos.x, self.pos.y-10)
        p = (self.player-.5)*-2
        scale(p, 1)
        a = atan((self.pos.y-self.prevPos.y)/((self.pos.x-self.prevPos.x) or .01))
        rotate(p*a)
        translate(-128, 0)
        image(gameManager.imageManager.getImage("./assets/schietspel/arrow.png"), 0, 0)
        popMatrix()
    
    def updatePhysics(self):
        if not self.stuck:
            self.prevPos = self.pos.copy()
            delta = 1/frameRate
            self.vel.add(PVector.mult(self.g, delta))
            self.pos.add(PVector.mult(self.vel, delta))
    
    def stickArrow(self):
        for i in range(3):
            self.updatePhysics()
        self.stuck = True

class SchietspelMinigame:
    def __init__(self):
        gameManager.imageManager.loadImage("./assets/schietspel/horse.png")
        gameManager.imageManager.loadImage("./assets/schietspel/arrow.png")

        gameManager.layerManager.removeLayerByName("minigame-schietspel")
        self.layer = gameManager.layerManager.createLayer("minigame-schietspel")
        gameManager.layerManager.setActiveLayerByName("minigame-schietspel")

        self.keyListener = self.layer.createElement("minigame-schietspel-keylistener")
        self.keyListener.registerKeyListener(self.key)
        self.keyListener.registerDrawListener(self.draw)

        self.elements = []
        self.mode = "turning"
        self.player = 0

        self.players = [Archer(self, -1), Archer(self, 1)]
        self.players[0].pos = PVector(100, 720)
        self.players[1].pos = PVector(1180, 720)

        self.angle = 0
        self.angularSpeed = .05
        self.dir = -1

        self.arrows = []

        self.scores = [0, 0]

        self.floorHeight = 150

        self.brown = "#6d4c41"
        self.purple = "#9c27b0"
        self.lightblue = "#80deea"

        self.state = "play"
        self.winner = ""
        self.timer = 0

        gameManager.client.register_listener(self.networkListener)
    
    def draw(self, layer, element):
        background("#4fc3f7")
        if self.state == "play":
            textSize(192)
            textAlign(CENTER, CENTER)
            strokeCap(SQUARE)

            
            fill("#FFFFFF")
            text(str(self.scores[0]), width/2-256, 128)
            text(str(self.scores[1]), width/2+256, 128)
            
            translate(0, -self.floorHeight)
            
            if self.mode == "turning":
                strokeWeight(10)
                stroke(0)
                
                x = self.players[0].pos.x
                y = self.players[0].pos.y
                
                fill(self.purple)
                stroke(self.purple)
                strokeCap(ROUND)
                self.pointy(PVector.sub(self.players[self.player].pos, PVector(0, 64)), PVector(100*cos(self.angle), 100*sin(self.angle)), 1, 48)
                    
                self.angle += self.angularSpeed * self.dir
                if self.angle > 0 or self.angle < -PI:
                    self.dir *= -1
            
            for a in self.arrows:
                a.updatePhysics()
                a.draw()
            
            if self.mode == "shooting":
                x = self.players[1].pos.x
                y = self.players[1].pos.y
                
                if self.currentArrow.pos.x > x - 64 + 16 and self.currentArrow.pos.x < x - 64 + 16 + 128 - 32 and self.currentArrow.pos.y > y - 133 + 16 and self.currentArrow.pos.y < y:
                    self.scores[0] += 1

                    if self.scores[0] >= 5:
                        gameManager.client.send("schietspel", {"command": "won", "player": gameManager.client.id})
                        self.state = "end"
                        return
                    
                    if self.currentArrow.pos.x > x - 32:
                        self.currentArrow.pos.y += 16
                    
                    self.stopArrow(True)

                    
                if self.currentArrow.pos.y > height:
                    self.stopArrow(False)

            for e in self.elements:
                e.draw()
            
            noStroke()
            fill(self.brown)
            rect(0, height, width, self.floorHeight)
        else:
            textSize(64)
            fill(255)
            if self.winner:
                text(self.winner + " won the game", width/2, height/2)
            else:
                text("You won the game!", width/2, height/2)
            self.timer += 1
            if self.timer > 360:
                gameManager.inGame = False
                gameManager.inGameCounter = 0

                self.keyListener.unregisterKeyListener(self.key)
                self.keyListener.unregisterDrawListener(self.draw)

                gameManager.layerManager.setActiveLayerByName("menu-lobby")


    def stopArrow(self, hit):
        self.currentArrow.stickArrow()
        if self.currentArrow.player == 0:
            gameManager.client.send("schietspel", {"command": "stick", "pos": [self.currentArrow.pos.x, self.currentArrow.pos.y], "prevPos": [self.currentArrow.prevPos.x, self.currentArrow.prevPos.y], "hit": hit, "player": gameManager.client.id})
        self.mode = "turning"

    def pointy(self, base, vec, thick, arrowSize):
        pushMatrix()
        translate(base.x, base.y)
        strokeWeight(32*thick)
        line(0, 0, vec.x, vec.y)
        rotate(vec.heading())
        translate(vec.mag() - arrowSize/4, 0)
        noStroke()
        triangle(0, 32*thick, 0, -32*thick, arrowSize, 0)
        popMatrix()

    def key(self, event):
        if event.type == "RELEASE":
            if event.key == " ":
                if self.mode == "turning":
                    pos = self.players[0].pos.copy()
                    vel = PVector(800*cos(self.angle), 800*sin(self.angle))
                    self.currentArrow = Arrow(pos, vel, 0)
                    self.currentArrow.prevPos = self.currentArrow.pos.copy().sub(PVector(cos(self.angle), sin(self.angle)))
                    self.currentArrow.pos.y -= 64
                    self.arrows.append(self.currentArrow)
                    self.mode = "shooting"
                    gameManager.client.send("schietspel", {"command": "shoot", "vel": [vel.x, vel.y], "player": gameManager.client.id})
    
    def networkListener(self, client, data):
        if data["type"] == "schietspel":
            if data["command"] == "shoot":
                pos = self.players[1].pos.copy()
                pos.y -= 64
                self.enemyArrow = Arrow(pos, PVector(-data["vel"][0], data["vel"][1]), 1)
                self.arrows.append(self.enemyArrow)
            elif data["command"] == "stick":
                if data["hit"]:
                    self.scores[1] += 1
                self.enemyArrow.stickArrow()
                self.enemyArrow.stuck = True
                self.enemyArrow.pos = PVector(data["pos"].x, data["pos"].y)
                self.enemyArrow.prevPos = PVector(data["prevPos"].x, data["prevPos"].y)
            elif data["command"] == "won":
                print("won")
                if not self.state == "end":
                    self.winner = data["name"]
                    self.state = "end"

def startGame():
    schietspel = SchietspelMinigame()