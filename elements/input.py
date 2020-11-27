from element import Element
from layer import layerManager

"""
Allows you to add a functioning input field to a Layer.
"""
class Input(Element):
    
    def __init__(self, id, x=0, y=0, w=0, h=0, placeholder="", textColor="#000000", textSize=16):
        Element.__init__(self, id, x, y)
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
        self.padding = 5
        self.textColor = textColor
        self.textSize = textSize
        self.placeholder = placeholder
        self.caretPos = 0
        self.caretVisible = False
        self.viewOffset = 0
        
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

            if self.counter >= frameRate * 0.6:
                self.caretVisible = True
                self.counter = 0 if self.counter >= 2 * frameRate * 0.6 else self.counter
            else:
                self.caretVisible = False
        
        # Actually create the text.
        start = 0
        while textWidth(self.text[start:]) > self.width - 2 * self.padding:
            start += 1
        self.viewOffset = start
        s = self.text[self.viewOffset:] if len(
            self.text) > 0 else self.placeholder
        text(s, self.x + self.padding, self.y + (self.height / 2))
        
        # Draw caret
        if self.caretVisible:
            # if textWidth(self.text[:self.caretPos]) < self.width - 2 * self.padding:
            caretX = textWidth(self.text[self.viewOffset:self.caretPos])
            # else:
            # caretX = self.width - 2 * self.padding
            stroke("#000000")
            line(self.x + self.padding + caretX, self.y + self.padding, self.x +
                 self.padding + caretX, self.y - 2 * self.padding + self.height)
        
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
                self.counter = frameRate * 0.6
            else:
                self.focused = False
                self.caretVisible = False
                        
    def key(self, element, layer, event):
        if self.focused:
            if event.type == "typed":
                # print(layerManager.controlPressed)
                
                if event.key == BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                        self.caretPos -= 1
                    self.counter = frameRate * 0.6
                    return
            
                if event.key == TAB or event.key == ENTER or event.key == CONTROL:
                    return
            
                self.text = self.text[:self.caretPos] + \
                    event.key + self.text[self.caretPos:]
                self.caretPos += 1
                self.counter = frameRate * 0.6
