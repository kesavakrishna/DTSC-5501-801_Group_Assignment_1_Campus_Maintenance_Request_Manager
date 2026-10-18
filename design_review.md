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

_To be added._

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
