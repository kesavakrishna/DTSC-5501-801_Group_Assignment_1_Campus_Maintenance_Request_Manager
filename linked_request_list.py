"""
LinkedRequestList design (Ben)
"""

class Node:
    def __init__(self, request):
        self.request = request
        self.next = None

class LinkedRequestList:
    def __init__(self):
        self.head = None
    def count(self):
        countNode = 0
        if self.head is None:
          return countNode
        tempNode = self.head
        while tempNode is not None:
          tempNode = tempNode.next
          countNode += 1
        return countNode
    def push(self, request):
        if self.findById(request.request_id) != -1:
            raise ValueError("ID already exists")
        tempNode = Node(request)
        tempNode.next = self.head
        self.head = tempNode
    def getAt(self, index):
        tempNode = self.head
        countIndex = 0
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError("Index is not an int")
        if index < 0 or index >= self.count():
            raise IndexError("Index is out of range")
        while tempNode is not None:
          if index == countIndex:
            return tempNode.request
          tempNode = tempNode.next
          countIndex += 1
    def append(self, request):
        if self.findById(request.request_id) != -1:
            raise ValueError("Id already exists")
        if self.head is None:
          self.push(request)
          return
        prevNode = self.head
        while prevNode.next is not None:
            prevNode = prevNode.next
        lastNode = Node(request)
        prevNode.next = lastNode
    def insertAt(self, index, request):
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError("Index is not an int")
        if index < 0 or index > self.count():
            raise IndexError("Index is out of range")
        if self.findById(request.request_id) != -1:
            raise ValueError("ID already exists")
        if index == 0:
          self.push(request)
          return

        tempNode = self.head
        countIndex = 0
        while tempNode is not None:
          if index-1 == countIndex:
            newNode = Node(request)
            newNode.next = tempNode.next
            tempNode.next = newNode
            return
          tempNode = tempNode.next
          countIndex += 1
    def removeAt(self, index):
        if isinstance(index, bool) or not isinstance(index, int):
            raise TypeError("Index is not an int")
        if index < 0 or index >= self.count():
            raise IndexError("Index is out of range")
        if index == 0:
            removedValue = self.head.request
            self.head = self.head.next
            return removedValue

        tempNode = self.head
        countIndex = 0
        while tempNode is not None:
            if index - 1 == countIndex:
                removedValue = tempNode.next.request
                tempNode.next = tempNode.next.next
                return removedValue
            tempNode = tempNode.next
            countIndex += 1
    def findById(self, request_id):
        tempNode = self.head
        countIndex = 0
        if request_id is None:
            return -1
        while tempNode is not None:
            if tempNode.request.request_id == request_id:
                return countIndex
            tempNode = tempNode.next
            countIndex += 1
        return -1
    def __str__(self):
        strList = []
        if self.head is None:
            return "None"

        tempNode = self.head
        while tempNode is not None:
            strList.append(str(tempNode.request.request_id))
            tempNode = tempNode.next
        strList.append("None")
        return ' -> '.join(strList)
     
    def insertionSortPriority(self):
        sortedHead = None
        current = self.head

        while current is not None:
            nextNode = current.next
            if sortedHead is None or current.request.priority < sortedHead.request.priority:
                current.next = sortedHead
                sortedHead = current
            else:
                walker = sortedHead
                while walker.next is not None and walker.next.request.priority <= current.request.priority:
                    walker = walker.next
                current.next = walker.next
                walker.next = current
            
            
            current = nextNode

        self.head = sortedHead

  
    
    def mergeSortByTime(self):
        self.head = self.sortChainByTime(self.head)

    def sortChainByTime(self, headNode):
        if headNode is None or headNode.next is None:
            return headNode
        secondHalf = self.splitMiddle(headNode)
        leftSorted = self.sortChainByTime(headNode)
        rightSorted = self.sortChainByTime(secondHalf)
        return self.mergeByTime(leftSorted, rightSorted)
    
    def splitMiddle(self, headNode):
        walkerSlow = headNode
        walkerFast = headNode.next
        while walkerFast is not None and walkerFast.next is not None:
            walkerSlow = walkerSlow.next
            walkerFast = walkerFast.next.next
        firstNodeSecondHalf = walkerSlow.next
        walkerSlow.next = None
        return firstNodeSecondHalf
    
    def mergeByTime(self, leftNode, rightNode):
        if leftNode is None:
            return rightNode
        if rightNode is None:
            return leftNode

        if leftNode.request.reported_time <= rightNode.request.reported_time:
            mergedHead = leftNode
            leftNode = leftNode.next
        else:
            mergedHead = rightNode
            rightNode = rightNode.next
        lastNode = mergedHead
        while leftNode is not None and rightNode is not None:
            if leftNode.request.reported_time <= rightNode.request.reported_time:
                lastNode.next = leftNode
                leftNode = leftNode.next
            else:
                lastNode.next = rightNode
                rightNode = rightNode.next
            lastNode = lastNode.next
        if leftNode is not None:
            lastNode.next = leftNode
        if rightNode is not None:
            lastNode.next = rightNode
    
        return mergedHead



