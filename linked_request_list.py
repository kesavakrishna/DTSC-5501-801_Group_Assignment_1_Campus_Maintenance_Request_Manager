"""
LinkedRequestList design (Ben)
Pretty simple. Don't have many notes to say. If you see something wrong let me know. For findById I am returning -1 if not found.
I'm not using a tail pointer or a cached size. I used a temporary class for the maintentance request. 

- Each node holds one maintenance request.
- Singly linked list.
- The list stores only head.
- Therefore, the list is empty only when head is none.
- In the linked list, the last node points to None.
- There should be no duplicate IDs, checks for duplicates will be added to push, append and insertAt.
- To check for duplicates, findById is used within push, append and insertAt.
- findById with return the position or -1 if None.
- If a call is not appropriate and fails, the list will remain unchanged through out of bounds checks.
- No tail pointer or cached size is used for simplicity.
- Complexity is as follows: push: O(n), getAt: O(n), append: O(n), insertAt: O(n), removeAt: O(n), findById: O(n), `__str__`: O(n), count: O(n).
-
"""

class Node:
    def __init__(self, request):
        self.request = request
        self.next = None

class FakeRequest: #Temporary stand in
    def __init__(self, request_id, priority, reported_time):
        self.request_id = request_id
        self.priority = priority
        self.reported_time = reported_time

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
        if isinstance(index, int) is False:
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
        if isinstance(index, int) is False:
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
        if isinstance(index, int) is False:
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
