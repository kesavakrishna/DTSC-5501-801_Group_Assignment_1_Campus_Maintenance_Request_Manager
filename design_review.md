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

_To be added._

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