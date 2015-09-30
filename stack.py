class StackNode:
    def __init__(self, name):
        """Creates an object for the stack """
        self.name = name
        self.quantity = 1
        self.next = None

    def __str__(self):
        """returns the quantity and name of the object"""
        return str(self.name)

class Stack:
    def __init__(self):
        """ initializes stack with head variable set to None.
        Used for portal """
        self.head = None
        
    def push(self, item):
        """ pushes given item to top of stack """        
        if self.head == None:
            self.head = StackNode(item)
        else:
            self.head.next = self.head
            self.head = StackNode(item)
            
    def pop(self):
        """ pops item at head of stack and reassigns head pointer """
        if self.head == None:
            return 
        else:
            returnItem = self.head
            self.head = self.head.next
            return returnItem

    def peek(self):
        """ returns item on top of stack """
        if self.head != None:
            return self.head.name
