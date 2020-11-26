"""
Helper Class to create Event objects. 
These event objects are used in every listener and always include the Element and Layer.
Custom variables may also be passed.
"""
class Event:

    def __init__(self, element, layer):
        self.element = element
        self.layer = layer

    def getElement(self):
        return self.element

    def getLayer(self):
        return self.layer

"""
The Element class is an abstract Element. Inherit this Class to be able to add this to a Layer.
"""
class Element:
    
    def __init__(self, id, x, y):
        self._mouseHandlers = []
        self._drawHandlers = []
        self._keyHandlers = []
        
        self.id = id
        self.hidden = False
        
        self.x = x
        self.y = y
        
    """
    Register the Listener functions.
    """
    def registerMouseListener(self, _callback = None):
        if _callback:
            self._mouseHandlers.append(_callback)  

        return self
    
    def unregisterMouseListener(self, _callback):
        self._mouseHandlers.remove(_callback)
        
        return self
            
    def registerDrawListener(self, _callback = None):
        if _callback:
            self._drawHandlers.append(_callback)
            
        return self
    
    def unregisterDrawListener(self, _callback):
        self._drawHandlers.remove(_callback)
        
        return self
    
    def registerKeyListener(self, _callback = None):
        if _callback:
            self._keyHandlers.append(_callback)
            
        return self
    
    def unregisterKeyListener(self, _callback):
        self._keyHandlers.remove(_callback)
        
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
            event = Event(self, layer)
            [function(event) for function in self._drawHandlers]
            
    def __callMouse__(self, layer, type):
        for function in self._mouseHandlers:
            event = Event(self, layer)
            event.type = type
            event.x = mouseX
            event.y = mouseY
            event.button = mouseButton
            
            function(event)
            
    def __callKey__(self, layer, type):
        for function in self._keyHandlers:
            event = Event(self, layer)
            event.type = type
            event.key = key
            event.keyCode = keyCode
            
            function(event)
