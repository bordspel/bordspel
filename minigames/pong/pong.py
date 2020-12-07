from manager.gameManager import gameManager
aDown = False
aUp = False
bDown = False
bUp = False
img = None

speed = 2

scoreA = 0
scoreB = 0

particles = []

def onSetup():
    global w, h, ballX, ballY, ballSize, ballTrail, paddleWidth, paddleHeight, a, b, img
    
    # Note: This needs to be changed to use the imageManager.
    img = loadImage("minigames\\pong\\background.jpg")

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
    global a, b, ballX, ballY, ballTrail, ballVelocityX, ballVelocityY, ballSpeed, scoreA, scoreB, particles
    if frameCount == 1:
        onSetup()
    background(img)
    
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
            if k[1] > h/5 + big * h/10:
                particles[i][1].pop(j)
            else:
                circle(pX + k[1] * cos(k[0]), pY + k[1] * sin(k[0]), (ballSize*(1 + big*ballSize/40)) - k[1]/(h/5 + big * h/10)*(ballSize)*(1 + big*ballSize/40))
                k[1] += .5 * k[2] / frameRate * h
                j += 1
        i += 1
    
    fill("#FFFFFF")
    rect(paddleWidth/4, a, paddleWidth/4*3, paddleHeight)
    rect(w - paddleWidth, b, paddleWidth/4*3, paddleHeight)
    
    text(scoreA, w/2 - h/5, h/5)
    text(scoreB, w/2 + h/5, h/5)
    
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
        resetBall()
    if ballX < paddleWidth + ballSize/2 and a <= ballY <= a + paddleHeight:
        ballVelocityX = 1
        particles += [newParticles(ballX, ballY, False)]
    if ballX > w:
        scoreA += 1
        particles += [newParticles(ballX, ballY, True, True)]
        resetBall()
    if ballX > w - paddleWidth - ballSize/2 and b <= ballY <= b + paddleHeight:
        ballVelocityX = -1
        particles += [newParticles(ballX, ballY, True)]
    if ballY < 0 + ballSize/2:
        ballVelocityY = 1
    if ballY > h - ballSize/2:
        ballVelocityY = -1       
    ballSpeed += .0000001 / frameRate * h
        
def resetBall():
    global ballX, ballY, ballTrail, ballVelocityX, ballVelocityY, ballSpeed, ballSize
    
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
      
minigamePong = gameManager.layerManager.createLayer("minigamePong")
gameManager.layerManager.setActiveLayerByName("minigamePong")
element = minigamePong.createElement('Pong', 0, 0) 

element.registerDrawListener(onDraw)
element.registerKeyListener(onKeyEvent)