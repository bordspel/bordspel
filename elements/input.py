from manager.gameManager import gameManager

from elements.element import Element

"""
Allows you to add a functioning input field to a Layer.
"""
class Input(Element):
    
    def __init__(self, id, x=0, y=0, w=0, h=0, placeholder="", textColor="#000000", textSize=16):
        Element.__init__(self, id, x, y)
        self.registerDrawListener(self.draw)
        self.registerMouseListener(self.mouse)
        self.registerKeyListener(self.key)
        
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
        self.caretVisible = False
        
    def draw(self, event):
        element = event.element
        layer = event.layer

        # Create the rectangle.
        stroke("#000000") if self.focused else stroke("#CCCCCC")
            
        fill("#FFFFFF")
        rect(self.x, self.y, element.width, element.height)
        
        # Create the text inside of the input.
        textSize(self.textSize)
        textAlign(LEFT, CENTER)
        fill(self.textColor if len(self.text) > 0 else "#AAAAAA")
        
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
        s = self.text[start:] if len(
            self.text) > 0 else self.placeholder
        text(s, self.x + self.padding, self.y + (self.height / 2))
        
        # Draw caret
        if self.caretVisible:
            caretX = textWidth(self.text[start:])
            stroke("#000000")
            line(self.x + self.padding + caretX, self.y + self.padding, self.x +
                 self.padding + caretX, self.y - 2 * self.padding + self.height)
        
        # Update the pointer.
        if (mouseX >= self.x and mouseX <= element.width + self.x) and (mouseY >= self.y and mouseY <= element.height + self.y):
            cursor(TEXT)
            gameManager.layerManager.customCursors.add(self)
        else:
            gameManager.layerManager.customCursors.discard(self)
        
    def mouse(self, event):
        # To check if the element is in focus. 
        if event.type == "click" and event.button == LEFT:
            if (event.x >= self.x and event.x <= event.element.width + self.x) and (event.y >= self.y and event.y <= event.element.height + self.y):
                self.focused = True
                self.counter = frameRate * 0.6
            else:
                self.focused = False
                self.caretVisible = False
                        
    def key(self, event):
        if self.focused:
            if event.type == "typed":
                # print(gameManager.layerManager.controlPressed)
                
                if event.key == BACKSPACE:
                    if len(self.text) > 0:
                        self.text = self.text[:-1]
                    self.counter = frameRate * 0.6
                    return
            
                elif event.key == TAB or event.key == ENTER or event.key == CONTROL:
                    return
            
                elif 31 < ord(event.key) < 127 or 160 < ord(event.key) < 384:
                    self.text += event.key
                self.counter = frameRate * 0.6
