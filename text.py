from element import *

"""
Allows you to display text to a Layer.
"""
class Text(Element):
    
    #TODO: Implement fonts.
    def __init__(self, id, x=0, y=0, text="", textSize=18, color="#000000", horizontalAlignment=CENTER, verticalAlignment=CENTER):
        Element.__init__(self, id)
        self.drawFunction(self.draw)
        
        self.x = x
        self.y = y
        
        self.text = text
        self.textSize = textSize
        self.horizontalAlignment = horizontalAlignment
        self.verticalAlignment = verticalAlignment
        
        self.color = color
        
    """
    Helper functions to create text more easily.
    """
    def horizontal(self, alignment):
        self.horizontalAlignment = alignment
        return self
    
    def vertical(self, alignment):
        self.verticalAlignment = alignment
        return self
    
    def textcolor(self, color):
        self.color = color
        return self
    
    def textsize(self, size):
        self.textSize = size
        return self
        
    def draw(self, element, layer):
        textSize(self.textSize)
        textAlign(self.horizontalAlignment, self.verticalAlignment)
        
        fill(self.color)
        text(self.text, self.x, self.y)
