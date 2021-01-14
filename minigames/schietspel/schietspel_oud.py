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

class SchietspelMinigame:
    def __init__(self):
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

        self.arrowPos = PVector()
        self.prevArrowPos = self.arrowPos.copy()
        self.arrowVel = PVector()
        self.g = PVector(0, 500)
        self.oldArrows = []

        self.scores = [0, 0]

        self.floorHeight = 150

        self.brown = "#6d4c41"
        self.purple = "#9c27b0"
        self.lightblue = "#80deea"

        # textFont(createFont("./assets/schietspel/Londrina.ttf", 192))
        # textSize(192)
        # textAlign(CENTER, CENTER)
        # strokeCap(SQUARE)

        self.wind = self.getWind()

        gameManager.imageManager.loadImage("./assets/schietspel/horse.png")
        gameManager.imageManager.loadImage("./assets/schietspel/arrow.png")
    
    def draw(self, layer, element):
        background("#4fc3f7")
        
        fill("#FFFFFF")
        text(self.scores[0], width/2-256, 128)
        text(self.scores[1], width/2+256, 128)
        
        stroke(self.lightblue)
        fill(self.lightblue)
        strokeCap(SQUARE)
        self.arrow(PVector(width/2, 128+32), PVector(self.wind, 0), 2, 64)
        
        translate(0, -self.floorHeight)
        
        if self.mode == "turning":
            strokeWeight(10)
            stroke(0)
            
            x = self.players[self.player].pos.x
            y = self.players[self.player].pos.y
            
            fill(self.purple)
            stroke(self.purple)
            strokeCap(ROUND)
            self.arrow(PVector.sub(self.players[self.player].pos, PVector(0, 64)), PVector(100*cos(self.angle), 100*sin(self.angle)), 1, 48)
            # line(x, y-64, x + 100*cos(angle), y + 100*sin(angle)-64)
                
            self.angle += self.angularSpeed * self.dir
            if self.angle > 0 or self.angle < -PI:
                self.dir *= -1
        
        if len(self.oldArrows) > 0:
            for a in self.oldArrows:
                self.drawArrow(a[0], a[1], a[2])
        
        if self.mode == "shooting":
            self.drawArrow(self.arrowPos, self.prevArrowPos, self.player)
            
            self.prevArrowPos = self.arrowPos.copy()
            self.updatePhysics(self.arrowPos, self.arrowVel)
            
            x = self.players[not self.player].pos.x
            y = self.players[not self.player].pos.y
            
            if self.arrowPos.x > x - 64 + 16 and self.arrowPos.x < x - 64 + 16 + 128 - 32 and self.arrowPos.y > y - 133 + 16 and self.arrowPos.y < y:
                self.scores[self.player] += 1
                self.pos = self.arrowPos.copy()
                if (not self.player and self.pos.x > x - 32) or (self.player and self.pos.x < x + 32):
                    self.pos.y += 16
                self.addOldArrow(self.pos, self.arrowVel.copy())
                
                self.player = not self.player
                self.mode = "turning"
                self.wind = self.getWind()
                
            if self.arrowPos.y > height:
                self.addOldArrow(self.arrowPos.copy(), self.arrowVel.copy())
                
                self.player = not self.player
                self.mode = "turning"
                self.wind = self.getWind()

        for e in self.elements:
            e.draw()
        
        noStroke()
        fill(self.brown)
        rect(0, height, width, self.floorHeight)
    
    def drawArrow(self, pos, prevPos, pl):
        pushMatrix()
        translate(pos.x, pos.y-10)
        p = (pl-.5)*-2
        scale(p, 1)
        a = atan((pos.y-prevPos.y)/((pos.x-prevPos.x) or .01))
        rotate(p*a)
        if -1 < a/PI < -.5:
            print("yes")
        translate(-128, 0)
        image(gameManager.imageManager.getImage("./assets/schietspel/arrow.png"), 0, 0)
        popMatrix()
        
    def addOldArrow(self, pos, vel):
        for i in range(3):
            prevPos = pos.copy()
            self.updatePhysics(pos, vel)
        self.oldArrows += [(pos, prevPos, self.player)]

    def updatePhysics(self, pos, vel):
        delta = 1/frameRate
        vel.add(PVector.mult(self.g, delta))
        vel.add(PVector.mult(PVector(self.wind, 0), delta))
        pos.add(PVector.mult(vel, delta))

    def arrow(self, base, vec, thick, arrowSize):
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
                    self.arrowPos = self.players[self.player].pos.copy()
                    self.prevArrowPos = self.arrowPos.copy().sub(PVector(cos(self.angle), sin(self.angle)))
                    self.arrowPos.y -= 64
                    self.arrowVel = PVector(800*cos(self.angle), 800*sin(self.angle))
                    self.mode = "shooting"
    
    def getWind(self):
        rand = (random()-.5)*2
        start = ((rand > 0) - .5)*-2
        return 50*start+(random()-.5)*50

schietspel = SchietspelMinigame()