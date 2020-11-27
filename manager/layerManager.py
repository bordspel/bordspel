"""
This class manages the Layers. Use this to add, remove and select the active Layer.
"""
class LayerManager:
    
    def __init__(self):
        self.layers = []
        self.activeLayer = None

        self.customCursors = set()
        
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
            self.customCursors.clear()

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