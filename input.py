from element import *
from layer import layerManager

"""
Allows you to add a functioning input field to a Layer.
"""
class Input(Element):
    
    def __init__(self, id, x=0, y=0, w=0, h=0, placeholder="", maxLength=14, textColor="#000000", textSize=16):
        Element.__init__(self, id)
        self.drawFunction(self.draw)
        self.mouseFunction(self.mouse)
        self.keyFunction(self.key)
        
        self.focused = False
        self.text = ""
        self.counter = 0
        
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.textColor = textColor
        self.textSize = textSize
        self.placeholder = placeholder
        self.maxLength = maxLength
        
    def draw(self, element, layer):
        # Create the rectangle.
        stroke("#000000") if self.focused else stroke("#CCCCCC")
            
        fill("#FFFFFF")
        rect(self.x, self.y, element.width, element.height)
        
        # Create the text inside of the input.
        textSize(self.textSize)
        textAlign(LEFT, CENTER)
        fill(self.textColor)
        
        # Update the counter, this is used to display the | at the end.
        character = ""
        if self.focused:
            self.counter += 1

            if len(self.text) < self.maxLength:
                if self.counter >= frameRate * 0.9:
                    character = "|"
                    self.counter = 0 if self.counter >= 2 * frameRate * 0.9 else self.counter
                        
        
        # Actually create the text.
        s = self.text + character if len(self.text) > 0 else self.placeholder + character
        text(s, self.x + 5, self.y + (self.height / 2))
        
        # Update the pointer.
        if (mouseX >= self.x and mouseX <= element.width + self.x) and (mouseY >= self.y and mouseY <= element.height + self.y):
            cursor(TEXT)
            layer.customCursors.add(self)
        else:
            layer.customCursors.discard(self)
        
    def mouse(self, element, layer, event):
        # To check if the element is in focus. 
        if event.type == "click" and event.button == LEFT:
            if (event.x >= self.x and event.x <= element.width + self.x) and (event.y >= self.y and event.y <= element.height + self.y):
                self.focused = True
                self.counter = frameRate * 0.9
            else:
                self.focused = False
                        
    def key(self, element, layer, event):
        if self.focused:            
            if event.key == BACKSPACE:
                self.text = self.text[:-1]
                return
            
            if event.key == TAB:
                return
            
            self.text += event.key if len(self.text) < self.maxLength else ""
