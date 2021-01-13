from manager.gameManager import gameManager
from bordspel.library.element.custom import *
import random as rd
from time import time

gameManager.audioManager.loadAudio("minigames\\pong\\assets\\pop.mp3")
gameManager.audioManager.loadAudio("minigames\\pong\\assets\\block.mp3")
gameManager.audioManager.loadAudio("minigames\\pong\\assets\\blockH.mp3")
gameManager.audioManager.loadAudio("minigames\\pong\\assets\\blockM.mp3")
gameManager.audioManager.loadAudio("minigames\\pong\\assets\\blockL.mp3")

gameManager.imageManager.loadImage("minigames\\pong\\assets\\background720.png")

aDown = False
aUp = False
bDown = False
bUp = False
img = None
hp1 = 5
hp2 = 5
speed = 2

scoreA = 0
scoreB = 0

batVelocityB = 0

particles = []

spelOver = False
winner = False
gelijkspel = False

count = 0

def randomBlockSound():
    blockSound = rd.randint(1,3)
    if blockSound == 1:
        gameManager.audioManager.getAudio("minigames\\pong\\assets\\blockH.mp3").rewind()
        gameManager.audioManager.getAudio("minigames\\pong\\assets\\blockH.mp3").play()   
    if blockSound == 2:
        gameManager.audioManager.getAudio("minigames\\pong\\assets\\blockM.mp3").rewind()
        gameManager.audioManager.getAudio("minigames\\pong\\assets\\blockM.mp3").play()   
    if blockSound == 3:
        gameManager.audioManager.getAudio("minigames\\pong\\assets\\blockL.mp3").rewind()
        gameManager.audioManager.getAudio("minigames\\pong\\assets\\blockL.mp3").play()   

def onSetup():
    global w, h, ballX, ballY, ballSize, ballTrail, paddleWidth, paddleHeight, a, b, img, imgWhite, imgRed, started

    # Note: This needs to be changed to use the imageManager.
    img = loadImage("minigames\\pong\\assets\\background720.png")
    imgWhite = loadImage("minigames\\pong\\assets\\WhiteHeart.png")
    imgRed = loadImage("minigames\\pong\\assets\\RedHeart.png")

    noStroke()
    background(0)
    fill("#FFFFFF")
    textAlign(CENTER)
    h = height
    w = width
    
    ballX = w/2
    ballY = h/2
    ballTrail = [(ballX, ballY)]
    
    paddleWidth = h/20
    paddleHeight = h/4
    a = b = (h - paddleHeight) / 2

    started = False
    
    textSize(h/5)
    
    resetBall()
    
def onDraw(layer,element):       
    global a, b, ballX, ballY, ballTrail, ballVelocityX, ballVelocityY, ballSpeed, scoreA, scoreB, particles, hp1, hp2
    global count, batVelocityB, started, gewonnen, gelijkspel, spelOver
    background(img)
    # background(0)
    if not spelOver:
        if frameCount == 1:
            onSetup()
            
        # ball
        i = 1
        l = len(ballTrail)
        step = ballSize/l
        while i < l:
            stroke(255/l*i)
            cur = ballTrail[i]
            prev = ballTrail[i - 1]
            strokeWeight(step*i)
            line(prev[0], prev[1], cur[0], cur[1])
            i += 1
        noStroke()

        # bot B 
        # and ballVelocityX > 0
        # and w - paddleWidth - ballX < 200

        if ((b + paddleHeight / 2) - ballY) > 75 and w - paddleWidth - ballX < 200:
            b -= 10
        elif ((b + paddleHeight / 2) - ballY) < -75 and w - paddleWidth - ballX < 200:
            b += 10     

        if ballVelocityX < 0:
            if b + paddleHeight / 2 > height / 2 + 10:
                b -= 5
            elif b + paddleHeight / 2 < height / 2 - 10:
                b += 5

        # particles
        fill("#FFFFFF")
        i = 0
        while i < len(particles):
            pX = particles[i][0][0]
            pY = particles[i][0][1]
            big = particles[i][2]
            j = 0
            while j < len(particles[i][1]):
                k = particles[i][1][j]
                if k[1] > h/5.3 + big * h/20:
                    particles[i][1].pop(j)
                else:
                    pushMatrix()
                    translate(pX + k[1] * cos(k[0]), pY + k[1] * sin(k[0]))
                    scale(min(max(0.5-1/((ballSize*(1 + big*ballSize/40)) - k[1]/(h/5 + big * h/10)*(ballSize)*(1 + big*ballSize/40)),0.05),1.5))
                    if big:
                        image(imgRed, 0, element.y) 
                    else:
                        image(imgWhite, 0, element.y)
                    popMatrix()

                    k[1] += .5 * k[2] / frameRate * h
                    j += 1
            i += 1
        
        fill("#FFFFFF")
        rect(paddleWidth/4, a, paddleWidth/4*3, paddleHeight)
        rect(w - paddleWidth, b, paddleWidth/4*3, paddleHeight)
        
        text(scoreA, w/2 - h/5, h/5)
        text(scoreB, w/2 + h/5, h/5)
        text(str(int(endTime-time())), w/2, h/5)
        
        # fill("#000000")
        # rect(0,0,hp1*75,75)
        # rect(width-hp2*75,0,hp2*75,75)

        # i = hp1 - 1
        # while i >= 0: 
        #     pushMatrix()
        #     translate(i*75+5.5,10) 
        #     scale(0.5)
        #     image(imgRed,0,0)
        #     popMatrix()
        #     i -= 1
        # i = hp2
        # while i > 0:
        #     pushMatrix()
        #     translate(width-i*75+5.5,10) 
        #     scale(0.5)
        #     image(imgRed,0,0)
        #     popMatrix()
        #     i -= 1
        
        if aDown and a < h - paddleHeight - paddleWidth/3:
            a += speed / frameRate * h
        if aUp and a > paddleWidth/3:
            a -= speed / frameRate * h
        if bDown and b < h - paddleHeight - paddleWidth/3:
            b += speed / frameRate * h
        if bUp and b > paddleWidth/3:
            b -= speed / frameRate * h
        
        bX = ballVelocityX * ballSpeed / frameRate * h
        bY = ballVelocityY * ballSpeed / frameRate * h
        
        ballTrail += [(ballX + bX, ballY + bY)]
        if len(ballTrail) > 20:
            ballTrail.pop(0)
        
        ballX += bX
        ballY += bY
        
        if ballX < 0:
            scoreB += 1
            particles += [newParticles(ballX, ballY, False, True)]
            hp1 -= 1
            resetBall()
        if ballX < paddleWidth + ballSize/2 and a <= ballY <= a + paddleHeight:
            ballVelocityX = 1
            particles += [newParticles(ballX, ballY, False)]
            randomBlockSound()
        if ballX > w:
            scoreA += 1
            particles += [newParticles(ballX, ballY, True, True)]
            hp2 -= 1
            resetBall()
        if ballX > w - paddleWidth - ballSize/2 and b <= ballY <= b + paddleHeight:
            ballVelocityX = -1
            particles += [newParticles(ballX, ballY, True)]
            randomBlockSound()
        if ballY < 0 + ballSize/2:
            ballVelocityY = 1
        if ballY > h - ballSize/2:
            ballVelocityY = -1       
        ballSpeed += .0000001 / frameRate * h

        # Counter voor 30 seconds.
        if count <= (60 * 30) and count != -1:
            count += 1
        elif count != -1:
            count = -1

            gameManager.client.send("pong", {"player": gameManager.client.id, "scorePlayer": scoreA, "scoreBot": scoreB})

    if spelOver: 
        if gewonnen:
            winnerText = "Je hebt gewonnen!"
        else:
            winnerText = "Je hebt verloren!"
        if gelijkspel:
            winnerText = "Er is gelijkspel!"

        textAlign(CENTER,CENTER)
        textSize(120)
        fill("#FFFFFF")
        text('GAME OVER\n'+winnerText,width/2,height/2)  

def resetBall():
    global ballX, ballY, ballTrail, ballVelocityX, ballVelocityY, ballSpeed, ballSize
    
    gameManager.audioManager.getAudio("minigames\\pong\\assets\\pop.mp3").rewind()
    gameManager.audioManager.getAudio("minigames\\pong\\assets\\pop.mp3").play()

    ballX = w/2
    ballY = h/2
    ballTrail = [(ballX, ballY)]
    ballVelocityX = (int(random(2))-.5)*2
    ballVelocityY = (int(random(2))-.5)*2
    ballSpeed = .75
    ballSize = h / 15


def handleKeys(val):
    global aUp
    global aDown
    global bUp
    global bDown
    
    if key == "w":
        aUp = val
    elif key == "s":
        aDown = val

def newParticles(x, y, right, big=False):
    return [
            [x, y], 
            [[random(- HALF_PI + PI*right, HALF_PI + PI*right), 0, random(.5, 1)] for i in range(20 + 20*big)],
            big
        ]

def onKeyEvent(event):
    global keyPressed
    if event.type == "PRESS":
        handleKeys(True)
    if event.type == "RELEASE":
        handleKeys(False)

def networkListener(client, data):
    global gelijkspel, gewonnen, spelOver
    if data["type"] == "pong":
        winnaarSpeler = data["winner"]

        #########################################
        # GEBRUIK DEZE VARIABLES OM OP HET SCHERM TE LATEN ZIEN OF JE GEWONNEN, VERLOREN OF GELIJKSPEL HEBT!!!
        #########################################
        gelijkspel = winnaarSpeler == "NONE"
        gewonnen = winnaarSpeler == client.id
        spelOver = True

        print(gewonnen, gelijkspel)

def resetGame():
    global aDown, aUp, bDown, bUp, img, hp1, hp2, speed, scoreA, scoreB, count, batVelocityB, particles, spelOver, winner, gelijkspel, gewonnen
    aDown = False
    aUp = False
    bDown = False
    bUp = False
    img = None
    hp1 = 5
    hp2 = 5
    speed = 2

    scoreA = 0
    scoreB = 0

    count = 0

    batVelocityB = 0

    particles = []

    spelOver = False
    gewonnen = False
    gelijkspel = False

    gameManager.layerManager.removeLayerByName("startPong")
    gameManager.layerManager.removeLayerByName("minigamePong")

def startGame():
    gameManager.client.register_listener(networkListener)

    minigamePong = gameManager.layerManager.createLayer("minigamePong")

    element = minigamePong.createElement('Pong', 0, 0) 
    element.registerKeyListener(onKeyEvent)
    element.registerDrawListener(onDraw)

    buttonStart = Button("start", 640-60, 720/2, 120, 30, (156, 39, 176), (171, 71, 188))
    textStart = Text("text", 640, 360+10,"Start Game")

    startPong = gameManager.layerManager.createLayer("startPong")   
    gameManager.layerManager.setActiveLayerByName("startPong")

    element = startPong.createElement("startPong")

    def mouseStart(event):
        global endTime, startTime
        if event.type == "CLICK" and event.button == "LEFT":
            if buttonStart.focused:
                startTime = time()
                endTime = startTime + 31
                gameManager.layerManager.setActiveLayerByName("minigamePong") 
     
    def drawStart(layer,element):   
        background(gameManager.imageManager.getImage("minigames\\pong\\assets\\background720.png"))

    element.registerDrawListener(drawStart)
    element.registerMouseListener(mouseStart)
        
    startPong.addElement(buttonStart)
    startPong.addElement(textStart)
startGame()