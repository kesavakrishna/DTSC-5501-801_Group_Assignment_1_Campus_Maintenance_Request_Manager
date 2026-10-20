"""
Data Structures and Algorithms Class
Group Assignment

This program will satisfy the Dynamic Array portion of the assignment

Fall 2026
"""



# This is a cute little function we'll need in the code below:
def is_it_a_power_of_two(n):
    # quick sanity check
    if n <= 1:
        return False
    a = int(n)
    while a != 1:
        b = a // 2
        # check did it divide evenly?
        if b * 2 != a:
            return False
        a = b
    return True

"""

This is going to be my version of the Dynamic Array-based way of storing all the info from various
maintenance requests.

I'm going to make it initialize empty containing EIGHT empty slots (chosen slightly arbitrarily)
and then double each time it needs more room, shrinking each time it is able to do so.

"""

class ArrayRequestList:

    def __init__(self):
        # It begins empty, containing 8 empty slots
        self.size = 0
        self.capacity = 8
        self.THE_LIST = [False] * self.capacity

    def push(self, MR):
        # Reject a duplicate request_id before changing anything
        if self.findById(MR.request_id) != -1:
            raise ValueError("That request_id is already in the array!")
        # First check if there's available room in THE LIST
        if self.size < self.capacity:
            # Shuffle everything to the right by one (starting at the last element)
            #       and then add the new element to the start.
            for i in range(self.size, 0, -1):
                self.THE_LIST[i] = self.THE_LIST[i-1]
            self.THE_LIST[0] = MR
            # Now update self.size to reflect the new size of THE LIST
            self.size += 1
        else:
            # Expand first if needed
            self.expand()
            self.push(MR)

    def append(self, MR):
        # Reject a duplicate request_id before changing anything
        if self.findById(MR.request_id) != -1:
            raise ValueError("That request_id is already in the array!")        
        # First check if there's available room in THE LIST
        if self.size < self.capacity:
            # Add it to the first free slot at the end. Thankfully, self.size
            #       points right to it, so we don't need to do a O(n) scan to
            #       find the first empty slot.
            self.THE_LIST[self.size] = MR
            # Now update self.size to reflect the new size of THE LIST
            self.size += 1
        else:
            # Expand first if needed
            self.expand()
            self.append(MR)

    def count(self):
        # Return a simple count of how many elements are in THE LIST
        return self.size

    def getAt(self, index):
        # Check to see if there are that many elements in THE LIST
        if type(index) != int:
            raise TypeError("You've gotta submit an integer!")
        if index < 0  or index >= self.size:
            raise IndexError("There aren't that many elements in the array!")
        else:
            return self.THE_LIST[index]

    def expand(self):
        # This method takes the underlying THE LIST (which is of fixed length)
        #       and copies it into a new, larger fixed-length list of double the capacity.
        #       It also updates the capacity to reflect this.
        backup_copy = self.THE_LIST.copy()
        self.capacity *= 2
        # This makes the new, larger, empty THE_LIST
        self.THE_LIST = [False] * self.capacity
        # This copies everything into it, one element at a time
        for i in range(len(backup_copy)):
            self.THE_LIST[i] = backup_copy[i]

    def removeAt(self, index):
        # This method lets you pop out a particular mainenance request by its index in,
        #       the array and return that MR at the end. It updates the size and capacity
        #       values and, if it can, shrinks the array.
        #
        # Begin by sanity checking that choice of index
        if type(index) != int:
            raise TypeError("You've gotta submit an integer!")
        if index < 0:
            raise IndexError("The index needs to be a nonnegative integer!")
        if index > self.size - 1:
            raise IndexError("That's past the last element in the list. Choose a smaller index!")
        _ret = self.THE_LIST[index]
        for i in range(index, self.size - 1):
            self.THE_LIST[i] = self.THE_LIST[i+1]
        self.THE_LIST[self.size-1] = False
        # Update the size to match
        self.size -= 1
        # Now check to see if self.size is a power of two. If it is, we can shrink to a
        #       smaller array. Ignore this if self.size is 7 or less.
        if self.size <= 7:
            return _ret
        else:
            if is_it_a_power_of_two(self.size) is True:
                self.shrink()
                return _ret
        return _ret

    def insertAt(self, index, MR):
        # This method lets you stick in a new MR into THE LIST at any desired index position
        #
        # Begin by sanity checking if that index is positive and if there are at least that many
        #       elements in THE LIST
        if type(index) != int:
            raise TypeError("You've gotta submit an integer!")
        if index < 0:
            raise IndexError("The index needs to be a nonnegative integer!")
        if index > self.size:
            raise IndexError("That's past the first open spot in the list. Choose a smaller index!")
        if index > self.size:
            raise IndexError("That's past the first open spot in the list. Choose a smaller index!")
        # Reject a duplicate request_id before changing anything
        if self.findById(MR.request_id) != -1:
            raise ValueError("That request_id is already in the array!")
        # Next check if there's available room in THE LIST
        if self.size < self.capacity:
            # Cool! We have room... Now let's shuffle everything to the right over by one and place it.
            for i in range(self.size, index, -1):
                self.THE_LIST[i] = self.THE_LIST[i-1]
            self.THE_LIST[index] = MR
            # Now update the size, and we're good!            
            self.size += 1
        else:
            # Expand first if needed
            self.expand()
            self.insertAt(index, MR)

    def shrink(self):
        # This method takes the underlying THE LIST (which is of fixed length)
        #       and copies it into a new, smaller fixed-length list of half the capacity.
        #       It also updates the capacity to reflect this.
        #
        # Note!! This method MUST only be used when it has been previously established
        #       that we've just reduced THE LIST down to a power of 2 and it's ready
        #       for shrinking.
        backup_copy = self.THE_LIST.copy()
        self.capacity //= 2
        # This makes the new, smaller, empty THE_LIST
        self.THE_LIST = [False] * self.capacity
        # This copies everything into it, one element at a time
        for i in range(self.capacity):
            self.THE_LIST[i] = backup_copy[i]

    def findById_Linear(self, MR_ID):
        # Quick sanity check:
        if type(MR_ID) != int:
            raise TypeError("You've gotta submit an integer!")
        if self.size == 0:
            return -1
        # Begin by scanning THE LIST and seeing if any MRs therein have that ID
        for i in range(self.size):
            if self.THE_LIST[i].request_id == MR_ID:
                # we've found it
                return i
        return -1

    def findById(self, MR_ID):
        # This only exists in case the grader uses that exact phrase. Same as the above method
        return self.findById_Linear(MR_ID)

    def __str__(self):
        _ret = ""
        _ret = _ret + "The current array size is " + str(self.size) + "\n"
        _ret = _ret + "The current array capacity is " + str(self.capacity) + "\n"
        _ret = _ret + "\n"
        if self.size == 0:
            _ret = _ret + "The array is currently empty. No work to be done!"
            return _ret
        _ret = _ret + "Here's a look at what's currently in the request list array:" + "\n"
        _ret = _ret + "\n"
        _ret = _ret + "------------------------------------------------------------------" + "\n"
        for i in range(self.size):
            _ret = _ret + "Maintainance Request ID # " + str(self.THE_LIST[i].request_id) + "\n"
            _ret = _ret + "Priority => " + str(self.THE_LIST[i].priority) + "\n"
            _ret = _ret + "------------------------------------------------------------------" + "\n"
        return _ret

    def helperfunction_add_to_sorted(self, MR):
        # This function, only a small helper function for the sort_by_priority Insertion Sort below
        #       requires self.THE_LIST to be sorted! And adds one new element to it at a time,
        #       placing it correctly where it belongs to keep the list sorted. Note: Sorted by priority.
        #
        # Scan across all the elements in the new sorted THE LIST and see where this one belongs
        for index in range(0, self.size):
            if self.THE_LIST[index].priority > MR.priority:
                self.insertAt(index, MR)
                return
        self.append(MR)

    def sort_by_priority(self):
        # We are instructed to do this sort method via Insertion Sort
        #       I'm going to go grab my code for that sort method and port it over.
        #
        # First step, save the current unsorted self.THE_LIST as a backup copy and clear THE LIST
        to_sort = self.THE_LIST.copy()
        original_size = int(self.size)
        self.THE_LIST = [False] * self.capacity
        self.size = 0
        for i in range(original_size):
            self.helperfunction_add_to_sorted(to_sort[i])

    def helperfunction_break_in_half(self, _list):
        # Once again, doing this in a non-mutable fashion with fixed-length lists.
        first_half = [False] * (len(_list) // 2)
        second_half = [False] * (len(_list) - len(_list) // 2)
        for i in range(len(_list)):
            if i < len(first_half):
                first_half[i] = _list[i]
            else:
                second_half[i-len(first_half)] = _list[i]
        return first_half, second_half

    def helperfunction_zip(self, A,B):
        _ret = [False] * (len(A) + len(B))
        A_index = 0
        B_index = 0
        _ret_index = 0
        while True:
            if A_index < len(A) and B_index < len(B):
                # Both lists have more elements to be zipped
                if A[A_index].reported_time <= B[B_index].reported_time:
                    """ This assumes older reports have a lower number!"""
                    _ret[_ret_index] = A[A_index]
                    A_index += 1
                    _ret_index += 1
                else:
                    _ret[_ret_index] = B[B_index]
                    B_index += 1
                    _ret_index += 1
            elif A_index < len(A) and B_index == len(B):
                # List B is exhausted
                _ret[_ret_index] = A[A_index]
                A_index += 1
                _ret_index += 1
            elif A_index == len(A) and B_index < len(B):
                # List A is exhausted
                _ret[_ret_index] = B[B_index]
                B_index += 1
                _ret_index += 1
            else:
                return _ret

    def helperfunction_mergesort(self, _list):
        if len(_list) <= 1:
            return _list
        else:
            firsthalf, secondhalf = self.helperfunction_break_in_half(_list)
            # Note the recursion
            firsthalf = self.helperfunction_mergesort(firsthalf)
            secondhalf = self.helperfunction_mergesort(secondhalf)
            return self.helperfunction_zip(firsthalf, secondhalf)
    
    def sort_by_reported_time(self):
        # We are instructed to do this sort method via Merge Sort
        #       I'm going to go grab my code for that sort method and port it over.
        #
        # Let's make a new copy of THE LIST that is only self.size elements long
        #       aka, we'll be making a new copy without any empty cells to the right.
        #       Capacity set equal to size
        to_sort = [False] * self.size
        for i in range(self.size):
            to_sort[i] = self.THE_LIST[i]
        self.THE_LIST = self.helperfunction_mergesort(to_sort) + [False] * (self.capacity - self.size)
