from settings import *

from element.listeners import *
from element.layer import Layer
from element.elements.button import Button
from element.elements.input import Input
from element.elements.text import Text
from element.elements.image import Image
from element.physicsBody import *

from manager.gameManager import gameManager
from random import random

# Setup function.
left = False
right = False

def setup():
    global box, box2, world, boxPhysics, box2Physics
    size(screenWidth, screenHeight)
    # Note: Fullscreen requires scaling which is not implemented.
    # displayWidth and displayHeight need to be used.
    # fullScreen()

    # Define the GameManager.
    global gameManager
    # gameManager.imageManager.loadImage("sketch.png")
    # gameManager.audioManager.loadAudio("audio.mp3")
    # gameManager.audioManager.getAudio("audio.mp3").play()

    # Create the Layers with their respective elements.
    menu = Layer("menu")
    menu.addElement(Text("#text2", x=10, y=45, text="Name").horizontal(LEFT).textcolor("#757575").textsize(16))
    menu.addElement(Input("#input1", x=10, y=60, w=200, h=35, textSize=14))

    menu.addElement(Button("#button1", x=10, y=125, w=100, h=35).base("#4CAF50").highlight("#3e8e41"))
    menu.addElement(Text("#text1", x=60, y=140, text="Submit").textcolor("#FFFFFFF").textsize(16))

    game = Layer("game")
    game.addElement(Button("#button1", x=200, y=10, w=200, h=100, baseColor="#4CAF50", highlightColor="#3e8e41"))
    game.addElement(Text("#text1", x=300, y=60, text="Go to layer1", textSize=16, color="#FFFFFFF"))
    # Add the Layers to the LayerManager.
    gameManager.layerManager.addLayer(menu)
    gameManager.layerManager.addLayer(game)
    # Select the current active Layer.
    background(255)
    gameManager.layerManager.setActiveLayer("menu")

    world = PhysicsWorld()

    floor = Button("#box", x=0, y=height-50, w=width, h=50).base("#7F7FFF").highlight("#FF5555")
    menu.addElement(floor)
    floorPhysics = PhysicsBody(floor, Rect(PVector(), w=width*2, h=50))
    floorPhysics.mass = 0.
    world.bodies += [floorPhysics]
    # for i in range(10):
        # box = Button("#box", x=random()*(width-25), y=random()*(height-75), w=25, h=25).base("#7F7FFF").highlight("#7F7FFF")
        # menu.addElement(box)
        # boxPhysics = PhysicsBody(box, Rect(PVector(), w=25, h=25))
        # boxPhysics.mass = .1
        # world.bodies += [boxPhysics]
    
    box = Button("#box", x=width/4*3, y=width/2, w=100, h=25).base("#7F7FFF").highlight("#7F7FFF")
    menu.addElement(box)
    boxPhysics = PhysicsBody(box, Rect(PVector(), w=100, h=25))
    boxPhysics.mass = 0.
    world.bodies += [boxPhysics]

    box = Button("#box", x=width/4, y=height/2, w=50, h=50).base("#7F7FFF").highlight("#7F7FFF")
    menu.addElement(box)
    boxPhysics = PhysicsBody(box, Rect(PVector(), w=50, h=50))
    world.bodies += [boxPhysics]
    box.registerDrawListener(moveBox)
    floor.registerDrawListener(world.update)
    box.registerKeyListener(checkKeys)

def stop():
    gameManager.client.close()

def moveBox(event):
    if left:
        boxPhysics.vel.x -= 5
    if right:
        boxPhysics.vel.x += 5

def checkKeys(event):
    global left, right
    if event.type == "released":
        if event.keyCode == 37:
            left = False
        elif event.keyCode == 39:
            right = False
        elif event.keyCode == 38:
            boxPhysics.vel.y -= 100

def keyPressed():
    global left, right
    if key == CODED:
        if keyCode == LEFT:
            left = True
        elif keyCode == RIGHT:
            right = True
    gameManager.layerManager.__callKey__("pressed")