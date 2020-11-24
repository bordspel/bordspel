import os

class ImageManager:

    def __init__(self):
        self.images = {}

    def getImage(self, path):
        if path in self.images:
            return self.images[path]
        return False

    def isImage(self, path):
        return path in self.images

    def isImageLoaded(self, path):
        if path in self.images:
            return self.images[path].width > 0
        return False

    def isAllImagesLoaded(self):
        for path, image in self.images.items():
            if image.width < 1:
                return False
        return True

    def getImageCount(self):
        return size(self.images)

    def loadImage(self, path):
        if path in self.images:
            return False

        if not os.path.isfile(path):
            return False

        image = requestImage(path)
        self.images[path] = image

        return True