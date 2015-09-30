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
