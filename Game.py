""" Game to play 'Lost Rovers'.
"""

from gameboard import *
from random import *
from linked_list import *
from stack import *

masterItemList = ["cake","screw","bagel","gear"]

class Game:
    SIZE = 15 # rooms are 15x15
    def __init__(self):
        """ Initializes the room, gameboard, contents, inventory, and portal stack"""
        self.room = Room()
        self.room.setupStartRoom()
        self.rover = Rover()
        self.inventory = linkedList()
        self.portalStack = Stack()

        #initialize task queue
        brokenItems = []
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                if isinstance(self.room.grid[i][j], Ship):
                    if self.room.grid[i][j].working == False:
                        brokenItems += [self.room.getItem(Point(i,j)).name()]
        self.taskQueue = Queue(brokenItems)

        self.gui = GameBoard("Lost Rover", self, Game.SIZE)

    def startGame(self):
        """"starts game"""
        self.gui.run()

    def goUp(self):
        """ Called by GUI when button clicked.
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        if self.rover.location.y > 0:
            self.rover.changeLocation(0,-1)
            self.checkIfPortal()
            self.checkIfComponent()

    def goDown(self):
        """ Called by GUI when button clicked. 
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        if self.rover.location.y < Game.SIZE -1:
            self.rover.changeLocation(0,1)
            self.checkIfPortal()
            self.checkIfComponent()

    def goLeft(self):
        """ Called by GUI when button clicked. 
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        if self.rover.location.x > 0:
            self.rover.changeLocation(-1,0)
            self.checkIfPortal()
            self.checkIfComponent()

    def goRight(self):
        """ Called by GUI when button clicked. 
            If legal, moves rover. If the robot lands
            on a portal, it will teleport. """
        if self.rover.location.x < Game.SIZE -1:
            self.rover.changeLocation(1,0)
            self.checkIfPortal()
            self.checkIfComponent()

    def checkIfPortal(self):
        """ Checks to see if rover is on top of a portal"""
        if isinstance(self.room.getItem(self.rover.location), Portal):
            self.teleport()

    def checkIfComponent(self):
        """ Checks to see if rover is on top of a portal"""
        component = self.room.getItem(self.rover.location)
        if isinstance(component, Ship):
            if component.isBroken() == True:
                currentTaskItem = self.taskQueue.peek()[0]
                if component.getName() != currentTaskItem:
                    self.taskQueue.requeue(component.getName())

    def teleport(self):
        """ Creates new room and links the portals"""

        portal = self.room.getItem(self.rover.location)

        # Revert all portals to normal before leaving room
        for i in range(self.SIZE):
            for j in range(self.SIZE):
                location = Point(i,j)
                if isinstance(self.room.grid[i][j], Portal):
                    if self.room.grid[i][j].image == 'portal-flashing.ppm':
                        self.room.grid[i][j].resetPortal()
                        
        # pop stack if going through portal lead to ship
        if portal.isSecondary() is True:
            self.portalStack.pop()

        if portal.sisterPortal != None:
            self.room = portal.sisterPortal.room
            
            # Add portal to stack if route to ship
            for x in range(self.SIZE):
                for y in range(self.SIZE):
                    location = Point(x,y)
                    if isinstance(self.room.grid[x][y], Portal):
                        if self.room.grid[x][y].isSecondary() == False:
                            self.portalStack.push(self.room.grid[portal.location.x][portal.location.y])
            
        else:
            newRoom = Room()        #Create new room
            
            #place sister portal in new room
            newRoom.grid[portal.location.x][portal.location.y] = Portal(newRoom, portal.location, self.room.getItem(portal.location), 2)

            #replace old portal with one that is linked to the new portal
            self.room.setItem(portal.location, Portal(self.room, portal.location, newRoom.getItem(portal.location)))
            self.room = newRoom

            # Add portal to stack
            self.portalStack.push(self.room.grid[portal.location.x][portal.location.y])
            
    def getImage(self, p):
        """ Called by GUI when screen updates.
            Returns image name (as a string) of the rover. 
		(Likely 'rover.ppm') """
        item = self.room.getItem(p)
        if item == None:
            return None
        else:
            return item.getImage()

    def getRoverImage(self):
        """ Called by GUI when screen updates.
            Returns image name (as a string) or None for the 
		part, ship component, or portal at the given 
		coordinates. ('engine.ppm' or 'cake.ppm' or 
		'portal.ppm', etc) """
        return self.rover.getImage()

    def getRoverLocation(self):
        """ Called by GUI when screen updates.
            Returns location (as a Point). """
        return self.rover.location

    def showWayBack(self):
        """ Called by GUI when button clicked.
            Flash the portal leading towards home. """
        for x in range(self.SIZE):
            for y in range(self.SIZE):
                location = Point(x,y)
                if isinstance(self.room.grid[x][y], Portal):
                    if self.room.grid[x][y].isSecondary() == True:
                        self.room.grid[x][y].flashPortal()
    
    def pickUp(self):
        """ Called by GUI when button clicked. 
		If rover is standing on a part (not a portal 
		or ship component), pick it up and add it
		to the inventory. """
        item = self.room.getItem(self.rover.location)
        if isinstance(item, Part) == True:
            self.inventory.add(item)
            self.room.remove(self.rover.location)
    
    def performTask(self):
        """ Called by the GUI when button clicked.
            If necessary parts are in inventory, and rover
            is on the relevant broken ship piece, then fixes
            ship piece and removes parts from inventory. If
            we run out of tasks, we win. """

        assert self.taskQueue.head != None, "The game is already over."
        
        itemAtLocation = self.room.getItem(self.rover.location)
        currentTaskItem = self.taskQueue.peek()[0]
        taskItems = self.taskQueue.peek()[1:]
        
        if isinstance(itemAtLocation, Ship):
            if itemAtLocation.getName() == currentTaskItem:
                if self.inventory.checkInventory(taskItems) == True:
                    #
                    items = self.taskQueue.peek()
                    component = items[0]
                    items = items[1:]
                    self.taskQueue.dequeue()
                    for i in items:
                        for j in range(int(i[0])):
                            self.inventory.remove(i[1])
                    itemAtLocation.fix()
                    
    def getCurrentTask(self):
        """ Called by GUI when task updates.
            Returns top task (as a string). 
		'Fix the engine using 2 cake, 3 rugs' or
		'You win!' 
 	  """
        a = self.taskQueue.peek()
        if a == None:
            return "You win!"
        else:
            itemList = a[1:]
            component = a[0]
            outputList = []
            for i in range(len(itemList)):
                element = ' '.join(itemList[i])
                outputList += [element]
            return "Fix the " + str(component) + " using: " + '\n' + '\n'.join(outputList)

    def getInventory(self):
        """ Called by GUI when inventory updates.
            Returns entire inventory (as a string). 
		3 cake
		2 screws
		1 rug
	  """
        return self.inventory.__str__()

class Rover:
    def __init__(self):
        """ Initializes the location and image for the rover"""
        self.location = Point(randint(0,Game.SIZE-1),randint(0,Game.SIZE-1))
        self.image = 'rover.ppm'

    def getImage(self):
        """ returns the rover's image """
        return self.image

    def changeLocation(self, changeX, changeY):
        """ Sets rover's location to given coordinates """
        self.location.x += changeX
        self.location.y += changeY

class Room:
    MAXPORTALS = 4

    def __init__(self):
        """ Sets up room geometry, calls methods to place portals and items """
        self.setupGrid()
        self.setupPortals()
        self.setupItems()

    def setupGrid(self):
        """ Setup a SIZE x SIZE grid full of None"""
        self.grid = []
        for x in range(Game.SIZE):
            self.grid.append([])
            for y in range(Game.SIZE):
                self.grid[x].append(None)

    def setupStartRoom(self):
        """ Fill a room with the starting ship components """
        self.grid[Game.SIZE//2][Game.SIZE//2] = Ship('cabin')
        self.grid[Game.SIZE//2][Game.SIZE//2-1] = Ship('exhaust')
        self.grid[Game.SIZE//2-1][Game.SIZE//2-1] = Ship('engine')
        self.grid[Game.SIZE//2+1][Game.SIZE//2+1] = Ship('engine')
        self.grid[Game.SIZE//2][Game.SIZE//2+1] = Ship('engine')

    def setupPortals(self):
        """ Populate room with portals"""
        for p in range(Room.MAXPORTALS):
            pt = self.getEmptyLocation()
            self.grid[pt.x][pt.y] = Portal(self,pt,None)

    def setupItems(self):
        """ Populate room with items"""
        for p in range(0,randint(5,20)):
            pt = self.getEmptyLocation()
            self.grid[pt.x][pt.y] = Part()

    def getEmptyLocation(self):
        """ Find empty element in grid"""
        while(True):
            p = Point(randint(0,Game.SIZE-1), randint(0,Game.SIZE-1))
            if self.grid[p.x][p.y] == None:
                return p

    def getItem(self, p):
        """ returns item at given point p"""
        return self.grid[p.x][p.y]

    def remove(self, p):
        """ removes item at given point p"""
        self.grid[p.x][p.y] = None

    def setItem(self, location, item):
        """ places item at location in room """
        self.grid[location.x][location.y] = item
        

class Item:
    def __init__(self):
        """ initializes object image to None"""
        self.image = None

    def getImage(self):
        """ returns object image"""
        return self.image

    def name(self):
        return self.image[:-4]

class Part(Item):
    def __init__(self):
        """ sets object image to randomized item image """
        itemList = masterItemList
        r = randint(0,len(itemList)-1)
        self.image = itemList[r] + '.ppm'

class Portal(Item):
    def __init__(self, room, location, sisterPortal, secondary = 1):
        """ Initializes a portal so that it is aware of its room, location
            in that room, image, linked (sister) portal, and whether it is a
            sister portal at creation (secondary) """
        self.room = room
        self.location = location
        self.image = 'portal.ppm'
        self.sisterPortal = sisterPortal
        self.secondary = secondary

    def getImage(self):
        """ returns object image """
        return self.image

    def flashPortal(self):
        """ sets image to flashing portal """
        self.image = 'portal-flashing.ppm'

    def resetPortal(self):
        """ sets image to non-flashing portal """
        self.image = 'portal.ppm'

    def isSecondary(self):
        """ tests whether the portal had a sister portal at its creation"""
        if self.secondary == 2:
            return True
        else:
            return False
        
class Ship(Item):
    def __init__(self, component):
        self.working = False
        self.component = component
        self.imageBroken = component + 'broken.ppm'
        self.image = component + '.ppm'

    def getImage(self):
        if self.working:
            return self.image
        else: return self.imageBroken

    def isBroken(self):
        return not self.working

    def getName(self):
        return self.component

    def fix(self):
        self.working = True


        

class Queue:
    def __init__(self, brokenItems):
        """ Sets up queue with size zero, creates necessary variables and
           creates tasks for all broken items. Used for tasks."""
        # O(1)
        
        self.head = None
        self.size = 0
        self.array = []
        self.addTasks(brokenItems)

    def enqueue(self, item):
        """ adds one item to end of the queue. Queue loops as a
        circular array. """
        # O(len(self.array))
        
        if self.head == None:
            self.array = [item]
            self.head = 0
        else:
            if self.size == len(self.array):
                self.double()
            head = self.head
            while self.array[head] != None:
                if head > len(self.array):
                    head = 0
                else:
                    head += 1
            self.array[head] = item

        self.size += 1

    def dequeue(self):
        """ Pops the head off of the queue. """
        # O(1)
        
        if self.head == None:
            return None
        else:
            returnItem = self.array[self.head]
            self.head += 1
            if self.head > len(self.array):
                self.head = 0
            self.size -= 1
            return returnItem

    def peek(self):
        """ returns top of queue without removing it """
        # O(1)
        return self.array[self.head]

    def double(self):
        """ Doubles array size and places the head in the first index """
        # O(1)
        
        p = self.head
        self.array = self.array[p:] + self.array[:p] + [None] * self.size

    def addTasks(self, brokenItems):
        """ Adds one queue item for each broken ship component. Each task
        requires 1-3 of 3 different items. """
        # O(n * len(itemList))
        
        for brokenItem in brokenItems:
            itemList = masterItemList
            taskList = [brokenItem]

            for item in itemList:               #O(3)
                while len(itemList) > 3:        #O(len(itemList)-3)
                    a = randint(0,len(itemList)-1)
                    itemList.pop(a)
                quantity = randint(1,3)
                taskList += [[str(quantity),item]]
            self.enqueue(taskList)
            
    def requeue(self, component):
        """ Reassigns head so that the head item reflects the given
        component"""
        
        # Find index of task of interest
        i = self.head
        while self.array[i] != None and self.array[i][0] != component:
            i += 1
        # Swap tasks
        self.array[self.head], self.array[i] = self.array[i], self.array[self.head]
        
def testQueue():
    """ Tests Queue class for functionality """
    queue = Queue()
    print(queue.dequeue())      #test dequeue when queue is empty
    queue.enqueue('a')          #test enqueue method
    queue.enqueue('b')
    queue.enqueue('c')
    print(queue.peek())         #test peek method and queue order
    print(queue.dequeue())      #test dequeue method
    queue.enqueue('d')
    print(queue.dequeue(), queue.dequeue(), queue.dequeue())


        
"""Launch the game. """
g = Game()
g.startGame() # This does not return until the game is over
