from manager.gameManager import gameManager
import random as rd

gameManager.audioManager.loadAudio("minigames\\pong\\assets\\pop.mp3")
gameManager.audioManager.loadAudio("minigames\\pong\\assets\\block.mp3")
gameManager.audioManager.loadAudio("minigames\\pong\\assets\\blockH.mp3")
gameManager.audioManager.loadAudio("minigames\\pong\\assets\\blockM.mp3")
gameManager.audioManager.loadAudio("minigames\\pong\\assets\\blockL.mp3")

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

particles = []

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
    global w, h, ballX, ballY, ballSize, ballTrail, paddleWidth, paddleHeight, a, b, img, imgWhite, imgRed
    
    # Note: This needs to be changed to use the imageManager.
    img = loadImage("minigames\\pong\\assets\\background.jpg")
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
    
    textSize(h/5)
    
    resetBall()
    
def onDraw(layer,element):       
    global a, b, ballX, ballY, ballTrail, ballVelocityX, ballVelocityY, ballSpeed, scoreA, scoreB, particles, hp1, hp2
    global count
    # FIX DE BACKGROUND SIZEEEE
    # background(img)
    background(0)
    if hp1 >0 and hp2 >0:
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
        
        fill("#000000")
        rect(0,0,hp1*75,75)
        rect(width-hp2*75,0,hp2*75,75)

        i = hp1 - 1
        while i >= 0: 
            pushMatrix()
            translate(i*75+5.5,10) 
            scale(0.5)
            image(imgRed,0,0)
            popMatrix()
            i -= 1
        i = hp2
        while i > 0:
            pushMatrix()
            translate(width-i*75+5.5,10) 
            scale(0.5)
            image(imgRed,0,0)
            popMatrix()
            i -= 1
        
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
        if count <= (60 * 7) and count != -1:
            count += 1
        elif count != -1:
            count = -1

            gameManager.client.send("pong", {"player": gameManager.client.id, "scorePlayer": scoreA, "scoreBot": scoreB})

    else: 
        if hp1 <1:
            winner = "Player 2 has won!"
        else:
            winner = "Player 1 has won!"
        textAlign(CENTER,CENTER)
        textSize(120)
        fill("#FFFFFF")
        text('GAME OVER\n'+winner,width/2,height/2)  

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
    elif key == CODED:
        if keyCode == UP:
            bUp = val
        elif keyCode == DOWN:
            bDown = val

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
    if data["type"] == "pong":
        winner = data["winner"]

        #########################################
        # GEBRUIK DEZE VARIABLES OM OP HET SCHERM TE LATEN ZIEN OF JE GEWONNEN, VERLOREN OF GELIJKSPEL HEBT!!!
        #########################################
        gelijkspel = winner == "NONE"
        gewonnen = winner == client.id

        print(gewonnen, gelijkspel)

gameManager.client.register_listener(networkListener)
      
minigamePong = gameManager.layerManager.createLayer("minigamePong")
gameManager.layerManager.setActiveLayerByName("minigamePong")
element = minigamePong.createElement('Pong', 0, 0) 

element.registerDrawListener(onDraw)
element.registerKeyListener(onKeyEvent)