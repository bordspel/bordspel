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
hartjeY = screenHeight * 0.71
hartjeSpeed = 50
meterDelay = 0
winnerDelay = 0
eindDelay = 0
buttonX = screenWidth * 0.80
buttonY = screenHeight * 0.13
gridBad1 = screenWidth * 0.2 
gridBad2 = screenWidth * 0.8
gridDecent1 = screenWidth * 0.3
gridDecent2 = screenWidth * 0.7
gridGood1 = screenWidth * 0.4
gridGood2 = screenWidth * 0.6
gridExcellent1 = screenWidth * 0.45
gridExcellent2 = screenWidth * 0.55
gridBest = screenWidth * 0.5

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
    fill(254, 127, 156)
    rect(0, screenHeight * 0.75, screenWidth, 300)
    #Verticale streep
    fill(0)
    strokeWeight(4)
    line(screenWidth / 2, screenHeight, screenWidth / 2, screenHeight * 0.75)
    strokeWeight(1)
    #Cirkel
    fill(200, 0, 0)
    circle(hartjeX, hartjeY, 185)
    #Geeft snelheid aan de cirkel
    hartjeX = hartjeX + hartjeSpeed
    #Check of de cirkel aan eind of aan het begin is, zo ja dan gaat die de andere kant op
    if hartjeX > screenWidth - 100 or hartjeX < 100:
        hartjeSpeed = hartjeSpeed * -1
    #Checkt of je op de knop drukt, zodat het hartje stop en vanuit daar krijg je een score en ga je naar de volgende room
    if mousePressed == True:
        if buttonX < mouseX < buttonX + 250 and buttonY < mouseY < buttonY + 180: #Nog veranderen naar de button in library
            hartjeSpeed = 0
            if hartjeX + 145 <= gridBad1 or hartjeX + 145 >= gridBad2:
                score = 1
            elif hartjeX + 145 > gridBad1 and hartjeX + 145 <= gridDecent1 or hartjeX + 145 < gridBad2 and hartjeX + 145 >= gridDecent2:
                score = 2
            elif hartjeX + 145 > gridDecent1 and hartjeX + 145 <= gridGood1 or hartjeX + 145 < gridDecent2 and hartjeX + 145 >= gridGood2:
                score = 3
            elif hartjeX + 145 > gridGood1 and hartjeX + 145 <= gridExcellent1 or hartjeX + 145 < gridGood2 and hartjeX + 145 >= gridExcellent2:
                score = 4
<<<<<<< Updated upstream
    if score > 0:
=======
            else:
                score = 5
    if score > 0 and meterDelay != -1:
>>>>>>> Stashed changes
        meterDelay += 1
        if meterDelay >= 130:
            # =================================
            # = CODE VAN NETWORKING!          =
            # = Stuur de score naar de server =
            # =================================
            gameManager.client.send("steekspel", {"score": score})

            # DIT MOET NAAR DE FUNCTIE `networkListener()` toe!!!!
            layer.removeElement(elementMeter)
            elementMeter.unregisterDrawListener(drawMeter)
<<<<<<< Updated upstream
            elementSpeler1.registerDrawListener(drawSpeler)
            elementSpeler2.registerDrawListener(drawSpeler)
        
def drawSpeler(layer, element):
    if element.id == 'Speler1':
        background(254, 127, 156)
    global velocity1, velocity2, winnerDelay
    fill(0,0,128)
    #Tekent 2 spelers
    rect(element.x, element.y, spelerWidth, spelerHeight)
=======
            elementBackground.registerDrawListener(drawBackground)
            layer.addElement(textLoading)
        
def drawSpeler(layer, element):
    if element.id == 'Speler1' or elementSpeler1.hidden:
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
    rect(200, screenHeight, screenWidth, screenHeight * 0,80)
>>>>>>> Stashed changes
    if element.id == "Speler1":
        element.x += velocity1 
    if element.id == "Speler2":
        element.x += velocity2
    #Colision check
    if elementSpeler2.x - elementSpeler1.x - spelerWidth < 10:
<<<<<<< Updated upstream
        elementSpeler2.unregisterDrawListener(drawSpeler)
        winnerDelay += 1
        velocity1 *= 0.95
        if winnerDelay >= 180:
            elementEind.registerDrawListener(drawEind)
            elementSpeler1.unregisterDrawListener(drawSpeler)
     
def drawEind(layer, element):
    global eindDelay
    background(254, 127, 156)
    #Tekent eindtekst
    if eindDelay == 0:
        layer.addElement(textEind)
    if eindDelay < 180:
        eindDelay += 1
    else:
        resetSteekspel()
        elementEind.unregisterDrawListener(drawEind)
        layer.removeElement(textEind)
        startSteekspel()
=======
        if gelijkspel:
            winnerDelay += 1
            velocity1 *= 0.97
            velocity2 *= 0.97
        else:
            if winner:
                elementSpeler2.unregisterDrawListener(drawSpeler)
                winnerDelay += 1
                velocity1 *= 0.95
            else:
                elementSpeler1.hide()
                winnerDelay += 1
                velocity2 *= 0.95
        if winnerDelay >= 620:
            elementSpeler1.unregisterDrawListener(drawSpeler)
            elementSpeler2.unregisterDrawListener(drawSpeler)
            layer.removeElement(textEind)
>>>>>>> Stashed changes

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

def drawBackground(layer, element):
    background(254, 127, 156)

# Dit bepaald wie de winnaar is.
def networkListener(client, data):
<<<<<<< Updated upstream
=======
    global gelijkspel, winner
>>>>>>> Stashed changes
    if data["type"] == "steekspel":
        winner = gameManager.client.id == data["winner"]
        gelijkspel = data["winner"] == "NONE"

<<<<<<< Updated upstream
        # HIER MOET DE CODE VAN DE WIN/LOSE ANIMATIE KOMEN
        print(winner)
        print(gelijkspel)
=======
        layer.addElement(textEind)

        if gelijkspel:
            textEind.setText("Het is gelijkspel!\n Jullie hebben niks gewonnen of veloren.")
        else:
            if winner:
                textEind.setText("Jij bent de winnaar!\n Je krijgt 15 Dukaten en 1 Charisma van de verliezer.")
            else:
                textEind.setText("Jij bent de verliezer!\n Je moet 15 Dukaten en 1 Charisma aan de winnaar geven.")    
        

        elementBackground.unregisterDrawListener(drawBackground)
        layer.removeElement(textLoading)

        elementSpeler1.registerDrawListener(drawSpeler)
        elementSpeler2.registerDrawListener(drawSpeler)
>>>>>>> Stashed changes

gameManager.client.register_listener(networkListener)

elementSpeler1 = layer.createElement("Speler1", x_speler1, y_speler1)

elementSpeler2 = layer.createElement("Speler2", x_speler2, y_speler2)

elementSpatie = layer.createElement("Spatie", 0, 0)
# elementSpatie.registerKeyListener(keyIntro)

elementBackground = layer.createElement('Background', 0, 0)

elementMeter = layer.createElement("Meter", 200, 200)

# layer.addElement(textIntro)

<<<<<<< Updated upstream
elementEind = layer.createElement("Eind", 0, 0)
=======
textEind = Text("TextEind", screenWidth / 2, screenHeight / 2 - 200, "")
textEind.setTextSize(34)
textEind.setColor(255)
>>>>>>> Stashed changes

textIntro = Text("TextIntro", screenWidth / 2, screenHeight / 2, "Welkom bij het Steekspel!\n\nIn deze minigame ga je tegen elkaar strijden door middel van liefde.\nU krijgt zo een liefde meter te zien met een hartje die snel heen en weer beweegt.\nDe bedoeling is om dat hartje zo dicht mogelijk in het midden te krijgen van de liefde meter.\nHoe dichter het hartje in het midden is, hoe meer liefde je heb en hoe groter de kans is dat je wint.\nOm het hartje stop te zetten drukt u met uw muisknop op de rode knop rechtsboven.\n\n\n\n\nDruk op spatie om verder te gaan.")
textIntro.setTextSize(26)

textEind = Text("TextEind", screenWidth / 2, screenHeight / 2, "De winnaar is speler 1!\n\n\nAls beloning krijgt de winnaar: ... Charisma en ... Dukaten")
textEind.setTextSize(30)

startSteekspel()