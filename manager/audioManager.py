# Note: This is NOT an error. This imports the minim library. 
from ddf.minim import Minim

class AudioManager:

    def __init__(self):
        self.minim = Minim(this)
        self.audioFiles = {}

    def loadAudio(self, path):
        soundFile = self.minim.loadFile(path)
        self.audioFiles[path] = soundFile

    def isAudio(self, path):
        return path in self.audioFiles
    
    def getAudio(self, path):
        if path in self.audioFiles:
            return self.audioFiles[path]
        return False

    def getAudioCount(self):
        return size(self.audioFiles)
