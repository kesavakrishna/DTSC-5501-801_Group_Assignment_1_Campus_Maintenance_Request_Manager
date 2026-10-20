# Design Review

## 1. MaintenanceRequest

MaintenanceRequest: a plain record containing request_id (int, unique), building, category, priority (1 to 4), reported_time (int), status.

Key decisions:
- No validation inside the record: We considered checking types and the 1–4 range in __init__, but Part A only asks for the attributes, and unique IDs cannot be checked by a single record.
- Uniqueness is enforced by the structures, which raise ValueError when an inserted request_id already exists. Invariant: no two requests stored in one structure share an ID.
- reported_time is a plain integer, so comparing two times when sorting is a simple <=

- Complexity: Creating a request and __str__ are O(1).

## 2. Dataset generator

generate_requests(n, seed=42, first_id=1000) returns a list of n requests.
- it uses its own random.Random(seed). We rejected random.seed() because any other code calling random would change the data.
- Unique IDs with gaps: IDs are sampled without replacement from a range ten times larger than n. So searches for missing IDs are realistic, and IDs never equal their positions.
- Six buildings (CASE, ECNW, ECCR, AERO, ATLAS, NORLIN).
- The same list is used to build both structures, so experiments use the same data. Generating n requests is O(n).

## 3. ArrayRequestList

Hi there. Orion here. I did my very best to design the Dynamic Array based on how arrays work in C. This is *quite* different from how
they work in Python, so it was a little "blocky" and obtuse-feeling to try and port that over to Python. That being said, all I really
did was construct it as *though* I were in C, and just kinda pretended to myself that the Lists were of completely fixed size.

Like a C array, I let my dynamic array have a capacity of empty slots, only some of which are filled. The array stores both its
capacity and its size separately. I began it with a capacity of 8, somewhat randomly. Maybe powers of 2 have a certain asthetic appeal.
When someone tries to fill it with a 9th element, it copies all its data into a NEW Python list but with double the capacity.
In C you have to remember to delete the old one, but thankfully Python does that automatically. It always doubles in size, 8 then
16, then 32, etc. And whenever it finds itself removing an element and *then* landing on size is a power of 2, it shrinks back
down by copying itself into a half-as-large-capacity Python list again.

Size must always, of course, be lower than capacity. Both of which must always be non-negative integers.
Unlike the Linked List version, no special care need be paid to keep track of where the tail is. Python lists can index to [-1] easily.

Since this is a group project, I chose to be fairly verbose with commenting my code. In case anyone else (collaborator or grader) felt
the need to read it and follow along for any reason. That was, honestly, the main design choice. Another design choice was when the
assignment said to insertAt "in the middle", I interpretted this as meaning that it should go kinda randomly somewhere in the interior
of the list. That we are not to use Push or Append. Not that it should be literally in the middle middle (length // 2).

I think? That most of my operations will be of runtime O(n) due to them having to often shuffle the entire list over by 1.
These are my predictions:
push -> O(n) (due to shuffling)
append -> O(1)
count -> O(1)
getAt -> O(1)
expand -> O(n)
removeAt -> O(n)
insertAt -> O(n)
shrink -> O(n)
findById_Linear -> O(n)
findById_Binary -> O(log(n))
__str__ -> O(n)
sort_by_priority -> O(n^2) (just like Insert Sort)
sort_by_reported_time -> O(n log(n)) (just like Merge Sort)

The biggest risk, to me, is that I programmed something badly / dumb that will break but not on my watch! I hope
if I got anything wrong that it doesn't mess up my partners. Group projects are stressful.

## 4. LinkedRequestList

Design review:
- The linked list will be made of node objects. Each node will hold a maintenance request as well as a reference to the next node.
- This list is empty if head is None.
- The last node's next will always be None.
- No two nodes will have the same request ID, duplicates will be prevented.
- A failed call, such as a duplicate, out of bounds index or a wrong type will be caught and leave the list unchanged.
- No cached size is used. count() will walk the entirety of the list. This keeps methods simpler but causes every method that uses count() to be O(n). If a cached size was used, count() would be O(1).
- No tail pointer exists. append() walks to the last node making it O(n).
- Checks are done before changing anything. Each method, where relevant, checks the type, the range and if a duplicate exists before making any changes to the linked list.
- To do duplicate checks, findById will be reused.
- findById returns the position if found and -1 if not found.
- Expected complexity is as follows: getAt: O(n), findById: O(n), push: O(n), append: O(n), insertAt O(n), removeAt O(n), count: O(n), insertion sort: O(n^2), merge sort: O(nlogn).

Planned tests and major risks:
- Duplicate ID's potentially slipping through.
- Non integer indexes slipping through.
- Changing arrows in the wrong order and inturn loosing the rest of the chain.
- Disruption caused by empty lists or one node lists. Must add checks to deal with these cases.
- When inserting or removing at index 0, making sure that head is correctly changed as changing the head requires a different approach.
- Removing the last node or the only node. 

## 5. Planned tests and major risks

One shared set of tests runs against both structures, plus array-only resize tests and linked-only structure tests.

| Kind | Cases |
|---|---|
| Normal | multiple elements; push/append; insert and remove at beginning, middle, end; successful search |
| Boundary | sizes 0, 1, 2; insertAt(n); removing the only element; growth from capacity 8 → 16 → 32; insert/push exactly when full; shrinking after removal |
| Invalid | duplicate ID (push, append, insertAt); indexes −1, n, n+1, 10; non-integers 1.0, "1", None, True; reading or removing from empty; unsuccessful search returns −1 |

Every invalid case also checks that the structure is unchanged. One test checks that no method prints.

Invariants checked after operations:
- Array: size ≤ capacity, the buffer length equals capacity, every slot past size is empty.
- Linked list: empty exactly when head is None; the chain ends in None (no cycle); count() equals the number of reachable nodes.
