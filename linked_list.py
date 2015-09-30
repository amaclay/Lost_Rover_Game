class Node:
    def __init__(self, name):
        """Creates an object for the linked list"""
        self.name = name
        self.quantity = 1
        self.next = None

    def __str__(self):
        """returns the quantity and name of the object"""
        return str(self.quantity) + ' ' + str(self.name)

class linkedList:
    def __init__(self):
        """Creates the linked list with default values for head and size"""
        self.head = None
        self._size = 0

    def __str__(self):
        """returns inventory of string type"""
        currentNode = self.head
        output = ''
        while currentNode != None:
            output += currentNode.__str__()
            output += '\n'
            currentNode = currentNode.next
        return output
        
    def remove(self, item):
        """removes selected item form inventory """
        itemNode = self.head
        prevItem = None
        
        # find item in inventory
        while itemNode.name != item:
            assert itemNode.next != None, "Item not in inventory"
            prevItem = itemNode
            itemNode = itemNode.next
            
        if itemNode.quantity > 1:
            itemNode.quantity -= 1 # Decrease quantity
        else:
            if prevItem == None:
                self.head = itemNode.next
            else:
                prevItem.next = itemNode.next # Delete from list

            itemNode = None
        self._size -= 1
            
    def add(self, item):
        """adds item to list. If item is already present, increments quantity"""
        item = self.translateItem(item)
        currentNode = self.head
        itemPresent = False
        
        #if list empty, create node and assign head
        if self.head == None:
            self.head = Node(item)
        else:
            #find last
            lastNode = currentNode
            if lastNode != None:
                if lastNode.next != None:
                    while lastNode.next != None:
                        lastNode = lastNode.next
                    
            #check for item
            checkNode = currentNode
            while checkNode != None:
                if checkNode.name == item:
                    itemPresent = True
                checkNode = checkNode.next
            
            #add item
            itemNode = currentNode
            if itemPresent:
                while itemNode.name != item:
                    itemNode = itemNode.next
                itemNode.quantity += 1
            else:
                lastNode.next = Node(item)
            
        self._size += 1

    def translateItem(self, item):
        """translates item from object to string name"""
        return item.image[:-4]

    def peek(self):
        """ returns the name of the item at the head node """
        return self.head.name

    def checkInventory(self, itemsNeeded):
        counter = 0
        for i in itemsNeeded:
            if self.checkItem(i) == True:
                counter += 1
        if counter == 3:    return True
        else:               return False

    def checkItem(self, item):
        currentNode = self.head
        while currentNode != None:
            if currentNode.name == item[1]:
                if currentNode.quantity >= int(item[0]):
                    return True
                else:
                    currentNode = currentNode.next
            else:
                currentNode = currentNode.next
        return False
