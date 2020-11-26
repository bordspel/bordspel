"""
Helper Class to create empty objects.
"""
class Empty:
    pass

"""
The Element class is an abstract Element. Inherit this Class to be able to add this to a Layer.
"""
class Element:
    
    def __init__(self, id, x, y):
        self.mouseFunctions = []
        self.drawFunctions = []
        self.keyFunctions = []
        
        self.id = id
        self.hidden = False
        
        self.x = x
        self.y = y
        
    """
    Register the Listener functions.
    """
    def registerMouseListener(self, _callback = None):
        if _callback:
            self.mouseFunctions.append(_callback)  

        return self
    
    def unregisterMouseListener(self, _callback):
        self.mouseFunctions.remove(_callback)
        
        return self
            
    def registerDrawListener(self, _callback = None):
        if _callback:
            self.drawFunctions.append(_callback)
            
        return self
    
    def unregisterDrawListener(self, _callback):
        self.drawFunctions.remove(_callback)
        
        return self
    
    def registerKeyListener(self, _callback = None):
        if _callback:
            self.keyFunctions.append(_callback)
            
        return self
    
    def unregisterKeyListener(self, _callback):
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
    def __callDraw__(self, layer):
        self.layer = layer
        if not self.hidden:
            [function(self, layer) for function in self.drawFunctions]
            
    def __callMouse__(self, layer, type):
        for function in self.mouseFunctions:
            event = Empty()
            event.type = type
            event.x = mouseX
            event.y = mouseY
            event.button = mouseButton
            
            function(self, layer, event)
            
    def __callKey__(self, layer, type):
        for function in self.keyFunctions:
            event = Empty()
            event.type = type
            event.key = key
            event.keyCode = keyCode
            
            function(self, layer, event)
