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
        for layer in self.layers:
            if layer.name == name:
                self.layers.remove(layer)
                
                # TODO: Clear the screen.
                
                return True
            
        return False
        
    # Set the active Layer by name.
    def setActiveLayer(self, name):
        for layer in self.layers:
            if layer.name == name:                
                self.activeLayer = layer
                
                # TODO: Clear the screen.
                
                return True
            
        return False
        
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
    
    def getElementByID(self, id):
        return [x for x in self.elements if x.id == id]
    
    """
    Do not call these functions manually, it might break the whole system.
    """
    def draw(self):
        for element in self.elements:
            element.callDraw(self)
        
    def mouse(self, type):
        for element in self.elements:
            element.callMouse(self, type)
            
    def key(self):
        for element in self.elements:
            element.callKey(self)


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
    
    layerManager.getActiveLayer().draw()
    
def mouseClicked():
    layerManager.getActiveLayer().mouse("click")
    
def mouseMoved():
    layerManager.getActiveLayer().mouse("move")
        
def mousePressed():
    layerManager.getActiveLayer().mouse("pressed")
       
def mouseReleased():
    layerManager.getActiveLayer().mouse("released")
    
def keyTyped(event):
    layerManager.getActiveLayer().key()
