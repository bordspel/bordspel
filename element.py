"""
Helper Class to create empty objects.
"""
class Empty:
    pass

"""
The Element class is an abstract Element. Inherit this Class to be able to add this to a Layer.
"""
class Element:
    
    def __init__(self, id):
        self.mouseFunctions = []
        self.drawFunctions = []
        self.keyFunctions = []
        
        self.id = id
        self.hidden = False
        
    """
    Register the Listener functions.
    """
    def mouseFunction(self, _callback = None):
        if _callback:
            self.mouseFunctions.append(_callback)  

        return self
    
    def removeMouseFunction(self, _callback):
        self.mouseFunctions.remove(_callback)
        
        return self
            
    def drawFunction(self, _callback = None):
        if _callback:
            self.drawFunctions.append(_callback)
            
        return self
    
    def removeDrawFunction(self, _callback):
        self.drawFunctions.remove(_callback)
        
        return self
    
    def keyFunction(self, _callback = None):
        if _callback:
            self.keyFunctions.append(_callback)
            
        return self
    
    def removeKeyFunction(self, _callback):
        self.keyFunctions.remove(_callback)
        
        return self
    
    """
    Functions that get information or manipulates the Element.
    """
    def getID(self):
        return self.id
        
    def isHidden(self):
        return self.hidden
    
    def hide(self):
        self.hidden = True
        
    def show(self):
        self.hidden = False
        
    def remove(self):
        if self.layer != None:
            self.layer.removeElement(self)
        
    """
    Do not call these functions manually, it might break the whole system.
    """
    def callDraw(self, layer):
        self.layer = layer
        if not self.hidden:
            for function in self.drawFunctions:
                function(self, layer)
            
    def callMouse(self, layer, type):
        for function in self.mouseFunctions:
            event = Empty()
            event.type = type
            event.x = mouseX
            event.y = mouseY
            event.button = mouseButton
            
            function(self, layer, event)
            
    def callKey(self, layer):
        for function in self.keyFunctions:
            event = Empty()
            event.key = key
            event.keyCode = keyCode
            
            function(self, layer, event)
