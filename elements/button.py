from manager.gameManager import gameManager

from elements.element import Element

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
        
    def draw(self, event):
        if (mouseX >= self.x and mouseX <= event.element.width + self.x) and (mouseY >= self.y and mouseY <= event.element.height + self.y):
            cursor(HAND)
            fill(self.highlightColor)
            gameManager.layerManager.customCursors.add(self)
        else:
            fill(self.baseColor)
            gameManager.layerManager.customCursors.discard(self)
            
        noStroke()
        rect(self.x, self.y, event.element.width, event.element.height)
        
    def mouse(self, event):
        # To check if the element is in focus. 
        if event.type == "click" and event.button == LEFT:
            if (event.x >= self.x and event.x <= event.element.width + self.x) and (event.y >= self.y and event.y <= event.element.height + self.y):
            
                if event.layer.name == "menu":
                    gameManager.layerManager.setActiveLayer("game")
                else:
                    gameManager.layerManager.setActiveLayer("menu")
