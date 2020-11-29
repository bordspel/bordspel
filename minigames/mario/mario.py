from manager.gameManager import gameManager

class MarioMinigame:

    def __init__(self):
        self.layer = gameManager.layerManager.createLayer("minigame-mario")

        self.player1 = self.layer.createElement("player1", 50, 200)
        self.player2 = self.layer.createElement("player2", 450, 200)

        self.player1.registerDrawListener(self.drawListener)
        self.player2.registerDrawListener(self.drawListener)

    def drawPlayer(self, layer, element):
        rect(element.x, element.y, 100, 100)

marioMinigame = MarioMinigame()