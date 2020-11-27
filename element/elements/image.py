from manager.gameManager import gameManager

from element.element import Element

class Image(Element):

    def __init__(self, id, path="", x=0, y=0, width=0, height=0):
        Element.__init__(self, id, x, y)
        self.registerDrawListener(self.draw)

        self.path = path
        self.loaded = False

        self.width = width
        self.height = height

        if not gameManager.imageManager.isImage(path):
            print("Image " + path + " is not an image.")
            
            self.unregisterDrawListener(self.draw)

            return

        self.load()


    def load(self):
        if gameManager.imageManager.isImageLoaded(self.path):
            self.image = gameManager.imageManager.getImage(self.path)

            if self.width <= 0:
                self.width = self.image.width
            if self.height <= 0:
                self.height = self.image.height

            self.loaded = True

    def draw(self, event):
        if self.loaded:
            image(self.image, self.x, self.y, self.width, self.height)
        else:
            self.load()