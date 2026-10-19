# DTSC-5501-801_Group_Assignment_1_Campus_Maintenance_Request_Manager

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