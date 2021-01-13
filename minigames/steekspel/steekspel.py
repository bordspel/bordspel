from manager.gameManager import gameManager
from bordspel.library.element.custom import *
from settings import screenWidth, screenHeight
import random

layer = gameManager.layerManager.createLayer("minigame-steekspel")

spelerWidth = 100
spelerHeight = 100
x_speler1 = 0
x_speler2 = screenWidth - spelerWidth
y_speler1 = screenHeight / 2
y_speler2 = screenHeight / 2
velocity1 = 10
velocity2 = -10 
hartjeX = random.randint(100, screenWidth - 100)
hartjeY = screenHeight * 0.55
hartjeSpeed = 50
meterDelay = 0
winnerDelay = 0
eindDelay = 0
buttonX = screenWidth * 0.80
buttonY = screenHeight * 0.13
gridBad1 = screenWidth * 0.2 #<384
gridBad2 = screenWidth * 0.8 #>1536
gridDecent1 = screenWidth * 0.35 #<672
gridDecent2 = screenWidth * 0.65 #>1248
gridGood1 = screenWidth * 0.45 #<864
gridGood2 = screenWidth * 0.55 #>1056
gridBest = screenWidth * 0.5 #864 ... 1056
score = 0

def keyIntro(event):
    #Checkt of spatie is ingedrukt
    if keyCode == 32:
        layer.removeElement(textIntro)
        elementMeter.registerDrawListener(drawMeter)
        elementSpatie.unregisterKeyListener(keyIntro)
        elementBackground.unregisterDrawListener(drawBackground)


def drawMeter(layer, element):
    background(254, 127, 156)
    global hartjeX, hartjeY, hartjeSpeed, meterDelay, score
    #Button
    fill(200, 0, 0)
    rect(buttonX , buttonY, 250, 180)
    #Meter
    imageMeter = loadImage('./Meter.png')
    image(imageMeter, 0, screenHeight * 0.85)
    #Hartje
    imageMeter = loadImage('./Hart.png')
    image(imageMeter, hartjeX, hartjeY)
    #Geeft snelheid aan de cirkel
    hartjeX = hartjeX + hartjeSpeed
    #Check of de cirkel aan eind of aan het begin is, zo ja dan gaat die de andere kant op
    if hartjeX > screenWidth - 50 or hartjeX < -100:
        hartjeSpeed = hartjeSpeed * -1
    #Checkt of je op de knop drukt, zodat het hartje stop en vanuit daar krijg je een score en ga je naar de volgende room
    if mousePressed == True:
        if buttonX < mouseX < buttonX + 250 and buttonY < mouseY < buttonY + 180: #Nog veranderen naar de button in library
            hartjeSpeed = 0
            if hartjeX <= gridBad1 or hartjeX >= gridBad2:
                score = 1
            elif hartjeX > gridBad1 and hartjeX <= gridDecent1 or hartjeX < gridBad2 and hartjeX >= gridDecent2:
                score = 2
            elif hartjeX > gridDecent1 and hartjeX <= gridGood1 or hartjeX < gridDecent2 and hartjeX >= gridGood2:
                score = 3
            else:
                score = 4
    if score > 0 and meterDelay != -1:
        meterDelay += 1
        if meterDelay >= 130:
            meterDelay == -1
            # =================================
            # = CODE VAN NETWORKING!          =
            # = Stuur de score naar de server =
            # =================================
            gameManager.client.send("steekspel", {"score": score})
            layer.removeElement(elementMeter)
            elementMeter.unregisterDrawListener(drawMeter)

            elementBackground.registerDrawListener(drawBackground)
            layer.addElement(textLoading)
        
def drawSpeler(layer, element):
    if element.id == 'Speler1' or elementSpeler1.hidden:
        # background(254, 127, 156)
        background(79, 195, 247)
    global velocity1, velocity2, winnerDelay, winner, gelijkspel 
    #Tekent 2 spelers
    if element.id == 'Speler1':
        imageHorseRight = loadImage('./HorseRight.png')
        image(imageHorseRight, element.x, element.y)
    if element.id == 'Speler2':
        imageHorseLeft = loadImage('./HorseLeft.png')
        image(imageHorseLeft, element.x, element.y)
    fill(109, 76, 65)
    rect(0, screenHeight, screenWidth, screenHeight * 0,80)
    if element.id == "Speler1":
        element.x += velocity1 
    if element.id == "Speler2":
        element.x += velocity2
    #Colision check
    if elementSpeler2.x - elementSpeler1.x - spelerWidth < 10:
        if gelijkspel:
            winnerDelay += 1
            velocity1 *= 0.95
            velocity2 *= 0.95
        else:
            if winner:
                elementSpeler2.unregisterDrawListener(drawSpeler)
                winnerDelay += 1
                velocity1 *= 0.95
            else:
                elementSpeler1.hide()
                winnerDelay += 1
                velocity2 *= 0.95
        if winnerDelay >= 180:
            elementEind.registerDrawListener(drawEind)
            elementSpeler1.unregisterDrawListener(drawSpeler)
            layer.removeElement(textEind)
     
def drawEind(layer, element):
    global eindDelay
    background(254, 127, 156)
    #Tekent eindtekst
    if eindDelay < 180:
        eindDelay += 1
    else:
        resetSteekspel()
        elementEind.unregisterDrawListener(drawEind)

def startSteekspel():
    gameManager.layerManager.setActiveLayerByName("minigame-steekspel")
    layer.addElement(textIntro)
    elementSpatie.registerKeyListener(keyIntro)
    elementBackground.registerDrawListener(drawBackground)

def resetSteekspel():
    global hartjeSpeed, meterDelay, winnerDelay, score, x_speler1, x_speler2, eindDelay, elementMeter, elementSpeler1, elementSpeler2, velocity1, velocity2
    hartjeSpeed = 50
    meterDelay = 0
    winnerDelay = 0
    score = 0
    x_speler1 = 0
    x_speler2 = screenWidth - spelerWidth
    eindDelay = 0
    velocity1 = 10
    velocity2 = -10 

    elementMeter = layer.createElement("Meter", 200, 200)
    elementSpeler1 = layer.createElement("Speler1", x_speler1, y_speler1)
    elementSpeler2 = layer.createElement("Speler2", x_speler2, y_speler2)

    layer.removeElement(textIntro)

def drawBackground(layer, element):
    background(254, 127, 156)

# Dit bepaald wie de winnaar is.
def networkListener(client, data):
    global gelijkspel, winner
    print(data)
    if data["type"] == "steekspel":
        winner = gameManager.client.id == data["winner"]
        gelijkspel = data["winner"] == "NONE"

        layer.addElement(textEind)

        if gelijkspel:
            textEind.setText("Het is gelijkspel")
        else:
            if winner:
                textEind.setText("Jij bent de winnaar")
            else:
                textEind.setText("Jij bent de verliezer")    
        

        elementBackground.unregisterDrawListener(drawBackground)
        layer.removeElement(textLoading)

        elementSpeler1.registerDrawListener(drawSpeler)
        elementSpeler2.registerDrawListener(drawSpeler)

gameManager.client.register_listener(networkListener)

elementSpeler1 = layer.createElement("Speler1", x_speler1, y_speler1)

elementSpeler2 = layer.createElement("Speler2", x_speler2, y_speler2)

elementSpatie = layer.createElement("Spatie", 0, 0)

elementBackground = layer.createElement('Background', 0, 0)

elementLoading = layer.createElement('LoadingScreen', 0, 0)

elementMeter = layer.createElement("Meter", 200, 200)

elementEind = layer.createElement("Eind", 0, 0)

textEind = Text("TextEind", screenWidth / 2, screenHeight / 2 - 200, "")
textEind.setTextSize(26)
textEind.setColor(255)

textIntro = Text("TextIntro", screenWidth / 2, screenHeight / 2, "Welkom bij het Steekspel!\n\nIn deze minigame ga je tegen elkaar strijden door middel van liefde.\nU krijgt zo een liefde meter te zien met een hartje die snel heen en weer beweegt.\nDe bedoeling is om dat hartje zo dicht mogelijk in het midden te krijgen van de liefde meter.\nHoe dichter het hartje in het midden is, hoe meer liefde je heb en hoe groter de kans is dat je wint.\nOm het hartje stop te zetten drukt u met uw muisknop op de rode knop rechtsboven.\n\n\n\n\nDruk op spatie om verder te gaan.")
textIntro.setTextSize(26)
textIntro.setColor(255)

textLoading = Text("TextLoading", screenWidth / 2, screenHeight / 2, "Aan het wachten op de andere speler...")
textLoading.setTextSize(34)
textLoading.setColor(255)

startSteekspel()