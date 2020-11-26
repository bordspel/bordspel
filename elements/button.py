from elements.element import Element
from elements.layer import layerManager

"""
Allows you to add a functioning button to a Layer.
"""
class Button(Element):
    
    def __init__(self, id, x=0, y=0, w=0, h=0, baseColor="#4CAF50", highlightColor="#3e8e41"):
        Element.__init__(self, id, x, y)
        self.registerDrawListener(self.draw)
        self.registerMouseListener(self.mouse)
        
        self.width = w
        self.height = h
        self.baseColor = baseColor
        self.highlightColor = highlightColor
        
    """
    Helper functions to create buttons more easily.
    """
    def base(self, color):
        self.baseColor = color
        return self
    
    def highlight(self, color):
        self.highlightColor = color
        return self
        
    def draw(self, element, layer):
        if (mouseX >= self.x and mouseX <= element.width + self.x) and (mouseY >= self.y and mouseY <= element.height + self.y):
            cursor(HAND)
            fill(self.highlightColor)
            layer.customCursors.add(self)
        else:
            fill(self.baseColor)
            layer.customCursors.discard(self)
            
        noStroke()
        rect(self.x, self.y, element.width, element.height)
        
    def mouse(self, element, layer, event):
        # To check if the element is in focus. 
        if event.type == "click" and event.button == LEFT:
            if (event.x >= self.x and event.x <= element.width + self.x) and (event.y >= self.y and event.y <= element.height + self.y):
            
                if layer.name == "menu":
                    layerManager.setActiveLayer("game")
                else:
                    layerManager.setActiveLayer("menu")
