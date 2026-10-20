
"""Binary-search algorithms for an array-based collection (Part D).

Both read the collection only through count() and getAt(), so on ArrayRequestList 
each search is O(log n). Linear search and the sorts stay in the structure classes,
because they work on each structure's own storage.
"""


def binary_search_by_id(collection, request_id):
    """Position of request_id in a collection sorted by increasing request_id, or -1."""
    if type(request_id) != int:
        raise TypeError("request_id must be an int")
    if collection.count() == 0:
        return -1
    low = 0
    high = collection.count() - 1
    # Keep searching while request_id lies between the IDs at low and high.
    while collection.getAt(low).request_id <= request_id <= collection.getAt(high).request_id and low <= high:
        mid = (low + high) // 2
        mid_id = collection.getAt(mid).request_id
        if mid_id == request_id:
            return mid
        elif mid_id > request_id:
            high = mid - 1
        else:
            low = mid + 1
        # Two positions left: check both directly.
        if high - low == 1:
            if collection.getAt(high).request_id == request_id:
                return high
            if collection.getAt(low).request_id == request_id:
                return low
            return -1
    return -1


def first_occurrence_by_priority(collection, priority):
    """First position holding this priority in a collection sorted by priority, or -1."""
    if type(priority) != int:
        raise TypeError("priority must be an int")
    low = 0
    high = collection.count() - 1
    first = -1
    while low <= high:
        mid = (low + high) // 2
        mid_priority = collection.getAt(mid).priority
        if mid_priority == priority:
            first = mid          # a match, but an earlier one may exist: keep searching left
            high = mid - 1
        elif mid_priority > priority:
            high = mid - 1
        else:
            low = mid + 1
    return first