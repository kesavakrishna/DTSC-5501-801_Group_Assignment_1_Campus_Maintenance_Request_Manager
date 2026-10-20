# DTSC-5501-801_Group_Assignment_1_Campus_Maintenance_Request_Manager

DTSC 5501-801, Group Assignment 1. Team 4 (workload Profile D: audit and cleanup).

## Team
- Kesava Sai Krishna Kondepudi: MaintenanceRequest, dataset generator, tests (Part F), performance experiment (Part G), README
- Orion Haunstrup: ArrayRequestList with its searching and sorting, workload (Part K), recommendation (Part I), README
- Ben Weakley: LinkedRequestList with its searching and sorting, complexity analysis (Part H), README

## How to run
We used Python 3.13. The notebook also needs pandas and matplotlib.

- Tests: python -m unittest -v test_project
- Notebook: open analysis.ipynb and run the cells from top to bottom. The benchmark cell takes several minutes.

## Files and main classes
| File | Contents |
|---|---|
| `maintenance_request.py` | `MaintenanceRequest` class and `generate_requests(n, seed)` the reproducible dataset |
| `array_request_list.py` | `ArrayRequestList`: a dynamic array built on a fixed-size Python list |
| `linked_request_list.py` | `Node` and `LinkedRequestList`: a singly linked list |
| `algorithms.py` | _To be added_ |
| `workload.py` | Profile D: generates an operation sequence from a seed and replays it on either structure |
| `test_project.py` | Unit tests, which are also our demonstration  |
| `analysis.ipynb` | Predictions, complexity analysis, benchmarks, plots and the recommendation |
| `design_review.md` | The design review written before implementing |

## Design decisions
- One shared interface: Both structures have push, append, count, getAt, insertAt, removeAt, findById and __str__ with the same behaviour, so the same tests and benchmarks run on both.
- Errors: IndexError for an index out of range (getAt/removeAt: 0 ≤ i < n; insertAt: 0 ≤ i ≤ n), TypeError for a non-integer index (including True/False, which Python otherwise treats as 1 and 0), ValueError for a duplicate request_id. Every check happens before anything changes, so a failed call leaves the structure as it was. Methods return results and never print.
- Not found: findById returns the request's position, or −1 if the ID is not stored. Binary search uses the same convention.

- Dynamic Array: 

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

- Linked list: No cached size or tail pointer were used for simplicity. The input is validated through out of bounds checks to ensure the structure remans unchanged after a failed operation. -1 is returned if the ID is not stored. 
- Sorting: All four sorts are stable: requests with equal keys keep their original order (test_sort_by_priority and test_sort_by_reported_time check this).
- Records: MaintenanceRequest does no validation; unique IDs are enforced by the structures (see design_review.md, section 1).
- Dataset: generate_requests uses its own random.Random(seed), so the same seed always produces the same requests.

## Assumptions
- request_id is a positive integer. reported_time is an integer where smaller means older; no date/time library is used.
- priority is 1 (urgent) to 4 (low) and is not validated.
- Every new request has status "OPEN".
- Binary search is only called on an array already in increasing request_id order.
- "Middle" means index n // 2.

## Changes since the design review
- Linked list: A boolean check was added to the type index check after it was shown in testing that True was returning 1.

## Testing (Part F)

### Test plan
The full list is in design_review.md, section 5.
- Normal: several elements; push and append; insert and remove at the
  beginning, middle and end; a successful search.
- Boundary: sizes 0, 1 and 2; insertAt(n) (adds at the end); removing the only element; array growth 8 → 16 → 32; insert or push exactly when the array is full; shrinking after a removal.
- Invalid: duplicate IDs; indexes −1, n and n+1; non-integer indexes (1.0, '1', None, True); reading or removing from an empty structure; a missing ID returns −1. Every invalid case also checks the structure is unchanged.

Pitfalls and the tests that cover them:
- Index versus stored value: the removal tests; test_unsuccessful_search (1 is a valid index but not an ID).
- Off-by-one at sizes 0, 1, 2: test_empty, test_one_element,  test_two_elements, test_remove_only_element.
- Printing instead of returning: test_methods_do_not_print.
- Inconsistent not-found: test_unsuccessful_search, test_search_empty (always −1).

### Failure-mode analysis: duplicate request IDs
1. What could go wrong: an insert stores a request whose `request_id` is already in the structure. `findById` only finds the first copy, so the second request can never be found by its ID.
2. Invariant violated: every request_id in one structure is unique.
3. Input that exposes it: build [1004, 1011, 1019], then push, append or insertAt another request with ID 1011.
4. Test designed to detect it: test_duplicate_id_rejected expects a ValueError from push, append and insertAt, then checks the contents are still exactly [1004, 1011, 1019].

Result on Oct 18: LinkedRequestList passed, because it calls findById
before every insert. ArrayRequestList failed:

```
FAIL: test_duplicate_id_rejected (test_project.ArrayTests.test_duplicate_id_rejected)
    with self.assertRaises(ValueError):
AssertionError: ValueError not raised
```
Appending a second 1011 gave [1004, 1011, 1019, 1011], and findById(1011) returned 1, the first copy.

### A test that initially failed: `test_remove_at_beginning`

```
ERROR: test_remove_at_beginning (test_project.ArrayTests.test_remove_at_beginning)
  File "test_project.py", line 75, in test_remove_at_beginning
    self.assertEqual(removed.request_id, 1004)
AttributeError: 'NoneType' object has no attribute 'request_id'
```

It also printed 'That ID # was not found in the array!'

What it revealed: ArrayRequestList.removeAt treated its argument as a
request ID, not a position. So removeAt(0) looked for a request with
ID 0, printed a message and returned None. Full output: the last run in test_output.txt.

### Demonstration
Our demonstration is `test_project.py`: every required operation has at least one
successful example there, checked with assertions. Run
`python -m unittest -v test_project` to see each test listed with `ok`.
Unless marked, each test runs on both `ArrayRequestList` and `LinkedRequestList`.

| Operation | Tests that show it working |
|---|---|
| `push` | `test_push_and_append`, `test_push_when_full` (array) |
| `append` | `test_push_and_append`, `test_one_element`, `test_multiple_elements` |
| `count` | `test_empty`, `test_one_element`, `test_multiple_elements` |
| `getAt` | `test_one_element`, `test_two_elements` (every test reads the contents through `getAt`) |
| `insertAt` | `test_insert_at_beginning`, `test_insert_in_middle`, `test_insert_at_end`, `test_insert_in_middle_when_full` (array) |
| `removeAt` | `test_remove_at_beginning`, `test_remove_in_middle`, `test_remove_at_end`, `test_remove_only_element` |
| `findById` (linear search) | `test_successful_search`, `test_unsuccessful_search`, `test_search_empty` |
| `__str__` | `test_str_shows_ids_in_order` |
| Binary search (array) | `test_binary_search_trace_array`, `test_binary_search_every_size` |
| First occurrence by priority | _To be added_ |
| Insertion sort by priority | `test_sort_by_priority` |
| Merge sort by reported time | `test_sort_by_reported_time` |
| Array resizing | `test_growth_doubles_and_keeps_order`, `test_push_when_full`, `test_insert_in_middle_when_full`, `test_shrink_after_removal_keeps_contents` |
| `MaintenanceRequest` | `test_fields_and_default_status` |
| Dataset | `test_same_seed_gives_same_requests`, `test_ids_are_unique_at_largest_size`, `test_fields_are_valid_and_cover_every_building` |
