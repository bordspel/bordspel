from settings import *

"""
This class manages the Layers. Use this to add, remove and select the active Layer.
"""
class LayerManager:
    
    def __init__(self):
        self.layers = []
        self.activeLayer = None
        
    # Add a Layer.
    def addLayer(self, layer):
        self.layers.append(layer)
    
    # Remove a layer.
    def removeLayer(self, layer):
        return self.layers.remove(layer)
        
    # Remove a Layer by name.
    def removeLayerByName(self, name):
        def remove(layer):
            self.layers.remove(layer)

            return layer
        
        return len([remove(layer) for layer in self.layers if layer.name == name]) != 0
        
    # Set the active Layer by name.
    def setActiveLayer(self, name):
        def setActive(layer):
            self.activeLayer = layer

            return layer

        return len([setActive(layer) for layer in self.layers if layer.name == name]) != 0
        
    # Get the current active Layer.
    def getActiveLayer(self):
        return self.activeLayer
    
    # Get the current active Layer's name
    def getActiveLayerName(self):
        if self.hasActiveLayer():
            return self.activeLayer.name
        return ""
    
    # Check if a Layer is active.
    def hasActiveLayer(self):
        return self.activeLayer != None
    
    """
    Do not call these functions manually, it might break the whole system.
    """
    def __callDraw__(self):
        if self.hasActiveLayer():
            for element in self.getActiveLayer().elements:
                element.__callDraw__(self.getActiveLayer())
        
    def __callMouse__(self, type):
        if self.hasActiveLayer():
            for element in self.getActiveLayer().elements:
                element.__callMouse__(self.getActiveLayer(), type)
            
    def __callKey__(self, type):
        if self.hasActiveLayer():
            for element in self.getActiveLayer().elements:
                element.__callKey__(self.getActiveLayer(), type)

# Define the LayerManager.
layerManager = LayerManager()

"""
This class represents a Layer. You can add and remove elements from this.
"""
class Layer:
    
    def __init__(self, name):
        self.name = name
        self.elements = []
        self.customCursors = set()
        
    # Add an element to the Layer.
    def addElement(self, element):
        self.elements.append(element)
        
        return self
    
    # Remove an element from the Layer.
    def removeElement(self, element):
        self.elements.remove(element)
    
        return self
    
    # Returns the Element by the id.
    def getElementByID(self, id):
        return [element for element in self.elements if element.id == id]


"""
Do not use these functions. Use the Element and Layer system.
These functions listen for the various events in the window and fire the correct event handlers.
"""
def draw():
    global layerManager
    background(255)
    
    # Used for debug.
    if DEBUG:
        textSize(12)
        textAlign(RIGHT, BOTTOM)
        fill(0)
        s = "Layer: " + str(layerManager.getActiveLayerName())
        text(s, screenWidth, screenHeight)
        
    # Used to reset the cursor.
    if len(layerManager.getActiveLayer().customCursors) == 0:
        cursor(ARROW)
    
    layerManager.__callDraw__()

def mouseClicked():
    layerManager.__callMouse__("click")
    
def mouseMoved():
    layerManager.__callMouse__("move")
        
def mousePressed():
    layerManager.__callMouse__("pressed")
       
def mouseReleased():
    layerManager.__callMouse__("released")
    
def keyTyped():
    layerManager.__callKey__("typed")
    
# This doesn't work for some reason.
# https://py.processing.org/reference/keyPressed.html
def keyPressed():
    layerManager.__callKey__("pressed")
    
def keyReleased():
    layerManager.__callKey__("released")
