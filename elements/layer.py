from settings import *

"""
This class represents a Layer. You can add and remove elements from this.
"""
class Layer:
    
    def __init__(self, name):
        self.name = name
        self.elements = []
        
    # Add an element to the Layer.
    def addElement(self, element):
        self.elements.append(element)
        
        return self
    
    # Remove an element from the Layer.
    def removeElement(self, element):
        self.elements.remove(element)
    
        return self
    
    # Returns the Element by the id.
    def getElementByID(self, id):
        return [element for element in self.elements if element.id == id]
