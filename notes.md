# Test results — Oct 18 (before fixes)

Run all tests:   `python -m unittest -v test_project`

| Structure | Tests | Passing | Failing |
|---|---|---|---|
| ArrayRequestList | 32 | 23 | 9 |
| LinkedRequestList | 27 | 27 | 0 |
| MaintenanceRequest + dataset | 4 | 4 | 0 |
| **Total** | **63** | **54** | **9** |
  
Run only your own tests while fixing:
- `python -m unittest -v test_project.ArrayTests`
- `python -m unittest -v test_project.LinkedTests`
- One test: `python -m unittest -v test_project.ArrayTests.test_remove_at_beginning`

---

## ArrayRequestList (12 failing tests)

### 1. `removeAt` should take a position, not an ID (UPDATE: Done)
- **Now:** `removeAt(0)` looks for a request whose ID is 0, prints
  "That ID # was not found", and returns `None`.
- **Expected:** `removeAt(0)` removes **and returns** the first request
  (same as Ben's list and the spec: `removeAt(index)`).
- **Fixes:** test_remove_at_beginning, test_remove_in_middle,
  test_remove_at_end, test_remove_only_element,
  test_shrink_after_removal_keeps_contents

### 2. Raise `IndexError` for bad positions (don't print)
- `getAt(i)` and `removeAt(i)`: valid when `0 <= i < size`
- `insertAt(i, ...)`: valid when `0 <= i <= size` (`i == size` adds at the end)
- **Now:** prints a message and returns `None`; `getAt(-1)` quietly returns `False`.
- **Fixes:** test_empty, test_negative_indexes, test_out_of_range_indexes,
  test_remove_from_empty

### 3. Raise `TypeError` for non-integer positions
- Should fail for `1.0`, `"1"`, `None` and `True`
  (Python treats `True` as `1`, so check for it explicitly):
  `if isinstance(index, bool) or not isinstance(index, int): raise TypeError("index must be an int")`
- **Fixes:** test_noninteger_indexes

### 4. Reject duplicate IDs with `ValueError`
- In `push`, `append` and `insertAt`, if the ID is already stored.
- Check **before** changing anything (before `expand()`), so a failed call
  leaves the array exactly as it was.
- **Fixes:** test_duplicate_id_rejected

### 5. Remove every `print` from the methods
- `findById` miss → just `return -1` (no "not found" / "array is empty" message)
-  findById_Binary: prints That ID # was not found on a miss and The array is empty! on an empty array. Just return -1.
- `print(a)` inside `is_it_a_power_of_two` prints `8 4 2` whenever the array shrinks
- **Fixes:** test_methods_do_not_print, and the last check in
  test_shrink_after_removal_keeps_contents, test_binary_search_does_not_print

**Already working:** resizing (8 → 16 → 32, insert/push when full), insert at
beginning/middle/end, push/append, `findById` return values.

---

## LinkedRequestList (1 failing test)

### 1. `True` is accepted as an index
- `isinstance(True, int)` is `True` in Python, so `getAt(True)` returns item 1.
- Use the same check as above in `getAt`, `insertAt` and `removeAt`:
  `if isinstance(index, bool) or not isinstance(index, int): raise TypeError(...)`
- **Fixes:** test_noninteger_indexes (index=True)

### 2. Housekeeping: two copies of the class
- `linked_request_list.py` and `linked_request_list_sort.py`. Please keep one
  (the version with the sorts) and tell Kesava the file name; the tests
  import `linked_request_list_sort`.

**Already working:** everything else, including both sorts.

---