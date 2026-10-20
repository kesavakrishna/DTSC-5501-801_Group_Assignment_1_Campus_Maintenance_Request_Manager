"""python -m unittest -v test_project"""

import unittest
import io
import contextlib
from maintenance_request import MaintenanceRequest
from array_request_list import ArrayRequestList
from linked_request_list_sort import LinkedRequestList
from dataset import generate_requests, BUILDINGS, CATEGORIES

TRACE_IDS = [1004, 1011, 1019, 1027, 1033, 1048, 1052, 1066]

def req(request_id, priority=3, reported_time=0):
    """A small request for tests; usually only the ID matters."""
    return MaintenanceRequest(request_id, "CASE", "HVAC", priority, reported_time)


def ids(structure):
    """The IDs in order, read through the public interface (count + getAt)."""
    return [structure.getAt(i).request_id for i in range(structure.count())]


class SharedTests:
    """Tests every structure must pass. Each subclass says which structure to build."""

    def make(self):
        raise NotImplementedError

    def sort_priority(self, s):
        raise NotImplementedError

    def sort_time(self, s):
        raise NotImplementedError
    
    def build(self, id_list):
        s = self.make()
        for request_id in id_list:
            s.append(req(request_id))
        return s

    def test_empty(self):
        s = self.make()
        self.assertEqual(s.count(), 0)
        with self.assertRaises(IndexError):
            s.getAt(0)

    def test_one_element(self):
        s = self.make()
        s.append(req(1004))
        self.assertEqual(s.count(), 1)
        self.assertEqual(s.getAt(0).request_id, 1004)

    def test_two_elements(self):
        s = self.build([1004, 1011])
        self.assertEqual(ids(s), [1004, 1011])
    
    def test_insert_at_beginning(self):
        s = self.build([1011, 1019])
        s.insertAt(0, req(1004))
        self.assertEqual(ids(s), [1004, 1011, 1019])

    def test_insert_in_middle(self):
        s = self.build([1004, 1011, 1027, 1033])
        s.insertAt(2, req(1019))          # goes BEFORE the item now at index 2
        self.assertEqual(ids(s), [1004, 1011, 1019, 1027, 1033])

    def test_insert_at_end(self):
        s = self.build([1004, 1011])
        s.insertAt(2, req(1019))          # index == n is allowed: adds at the end
        self.assertEqual(ids(s), [1004, 1011, 1019])

    def test_push_and_append(self):
        s = self.build([1011])
        s.push(req(1004))
        s.append(req(1019))
        self.assertEqual(ids(s), [1004, 1011, 1019])

    # ----- removal: beginning, middle, end -----

    def test_remove_at_beginning(self):
        s = self.build([1004, 1011, 1019])
        removed = s.removeAt(0)
        self.assertEqual(removed.request_id, 1004)
        self.assertEqual(ids(s), [1011, 1019])

    def test_remove_in_middle(self):
        s = self.build([1004, 1011, 1019, 1027, 1033])
        removed = s.removeAt(2)
        self.assertEqual(removed.request_id, 1019)
        self.assertEqual(ids(s), [1004, 1011, 1027, 1033])

    def test_remove_at_end(self):
        s = self.build([1004, 1011, 1019])
        removed = s.removeAt(2)
        self.assertEqual(removed.request_id, 1019)
        self.assertEqual(ids(s), [1004, 1011])

    def test_remove_only_element(self):
        s = self.build([1004])
        removed = s.removeAt(0)
        self.assertEqual(removed.request_id, 1004)
        self.assertEqual(s.count(), 0)


    # ----- invalid input: must raise, and leave the structure unchanged -----

    def test_duplicate_id_rejected(self):
        s = self.build([1004, 1011, 1019])
        with self.assertRaises(ValueError):
            s.push(req(1011))
        with self.assertRaises(ValueError):
            s.append(req(1011))
        with self.assertRaises(ValueError):
            s.insertAt(1, req(1011))
        self.assertEqual(ids(s), [1004, 1011, 1019])

    def test_remove_from_empty(self):
        s = self.make()
        with self.assertRaises(IndexError):
            s.removeAt(0)

    def test_out_of_range_indexes(self):
        s = self.build([1004, 1011, 1019])
        for bad in (3, 10):
            with self.subTest(index=bad):
                with self.assertRaises(IndexError):
                    s.getAt(bad)
                with self.assertRaises(IndexError):
                    s.removeAt(bad)
        with self.assertRaises(IndexError):
            s.insertAt(4, req(2000))      # insertAt allows 0..n, so n + 1 is invalid
        self.assertEqual(ids(s), [1004, 1011, 1019])

    def test_negative_indexes(self):
        s = self.build([1004, 1011, 1019])
        with self.assertRaises(IndexError):
            s.getAt(-1)
        with self.assertRaises(IndexError):
            s.removeAt(-1)
        with self.assertRaises(IndexError):
            s.insertAt(-1, req(2000))
        self.assertEqual(ids(s), [1004, 1011, 1019])

    def test_noninteger_indexes(self):
        s = self.build([1004, 1011, 1019])
        for bad in (1.0, "1", None, True):
            with self.subTest(index=bad):
                with self.assertRaises(TypeError):
                    s.getAt(bad)
                with self.assertRaises(TypeError):
                    s.removeAt(bad)
                with self.assertRaises(TypeError):
                    s.insertAt(bad, req(2000))
        self.assertEqual(ids(s), [1004, 1011, 1019])

    def test_multiple_elements(self):
        id_list = [1004, 1011, 1019, 1027, 1033, 1048, 1052, 1066, 1071, 1085]
        s = self.build(id_list)
        self.assertEqual(s.count(), 10)
        self.assertEqual(ids(s), id_list)

    # ----- search: findById returns the position, or -1 if missing -----

    def test_successful_search(self):
        s = self.build([1048, 1004, 1033])
        self.assertEqual(s.findById(1048), 0)     # positions, not IDs
        self.assertEqual(s.findById(1004), 1)
        self.assertEqual(s.findById(1033), 2)

    def test_unsuccessful_search(self):
        s = self.build([1048, 1004, 1033])
        for missing in (1000, 1005, 9999, 1):    # 1 is a valid index, but not an ID
            with self.subTest(request_id=missing):
                self.assertEqual(s.findById(missing), -1)

    def test_search_empty(self):
        self.assertEqual(self.make().findById(1004), -1)

    # ----- methods must return their results, never print -----

    def test_methods_do_not_print(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            s = self.make()
            s.push(req(1011))
            s.append(req(1019))
            s.insertAt(0, req(1004))
            s.count()
            s.getAt(1)
            s.findById(1019)
            s.findById(9999)               # a miss must not print either
            s.removeAt(1)
            str(s)
        self.assertEqual(output.getvalue(), "")

    def test_str_shows_ids_in_order(self):
        s = self.build([1004, 1011, 1019])
        text = str(s)
        self.assertIsInstance(text, str)
        self.assertLess(text.index("1004"), text.index("1011"))
        self.assertLess(text.index("1011"), text.index("1019"))
        self.assertIsInstance(str(self.make()), str)      # an empty structure works too

    # ----- sorting: priority 1 first; oldest reported_time first -----

    def check_sort(self, requests, sort, key):
        """Build from requests, sort, and compare with Python's sorted():
        same order, and requests that tie keep their original order."""
        s = self.make()
        for r in requests:
            s.append(r)
        sort(s)
        expected = [r.request_id for r in sorted(requests, key=key)]
        self.assertEqual(ids(s), expected)

    def test_sort_by_priority(self):
        inputs = {
            "empty": [],
            "one element": [req(1004, priority=2)],
            "already sorted": [req(1004, priority=1), req(1011, priority=2), req(1019, priority=3)],
            "reverse sorted": [req(1004, priority=3), req(1011, priority=2), req(1019, priority=1)],
            "random, with ties": generate_requests(50),
        }
        for name, requests in inputs.items():
            with self.subTest(input=name):
                self.check_sort(requests, self.sort_priority, key=lambda r: r.priority)

    def test_sort_by_reported_time(self):
        inputs = {
            "empty": [],
            "one element": [req(1004, reported_time=50)],
            "already sorted": [req(1004, reported_time=10), req(1011, reported_time=20), req(1019, reported_time=30)],
            "reverse sorted": [req(1004, reported_time=30), req(1011, reported_time=20), req(1019, reported_time=10)],
            "random, with ties": generate_requests(50),
        }
        for name, requests in inputs.items():
            with self.subTest(input=name):
                self.check_sort(requests, self.sort_time, key=lambda r: r.reported_time)

class ArrayTests(SharedTests, unittest.TestCase):
   
    def make(self):
        return ArrayRequestList()

    def sort_priority(self, s):
        s.sort_by_priority()

    def sort_time(self, s):
        s.sort_by_reported_time()

    def check_array(self, s):
        """The array's own rules: size fits in capacity, the buffer is exactly
        capacity long, and every slot past size is empty (False)."""
        self.assertLessEqual(s.size, s.capacity)
        self.assertEqual(len(s.THE_LIST), s.capacity)
        for i in range(s.size, s.capacity):
            self.assertIs(s.THE_LIST[i], False)

    def test_growth_doubles_and_keeps_order(self):
        s = self.make()
        capacities = []
        for i in range(17):
            s.append(req(1000 + i))
            capacities.append(s.capacity)
            self.check_array(s)
        self.assertEqual(capacities, [8] * 8 + [16] * 8 + [32])
        self.assertEqual(ids(s), [1000 + i for i in range(17)])

    def test_insert_in_middle_when_full(self):
        s = self.build([1000 + i for i in range(8)])     # exactly full
        self.assertEqual(s.capacity, 8)
        s.insertAt(4, req(2000))
        self.assertEqual(s.capacity, 16)
        self.assertEqual(ids(s), [1000, 1001, 1002, 1003, 2000, 1004, 1005, 1006, 1007])
        self.check_array(s)

    def test_push_when_full(self):
        s = self.build([1000 + i for i in range(8)])
        s.push(req(2000))
        self.assertEqual(s.capacity, 16)
        self.assertEqual(ids(s), [2000] + [1000 + i for i in range(8)])
        self.check_array(s)

    def test_shrink_after_removal_keeps_contents(self):
        s = self.build([1000 + i for i in range(9)])     # 9 items, capacity 16
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            removed = s.removeAt(0)                      # size 9 -> 8 should shrink
        self.assertEqual(removed.request_id, 1000)
        self.assertEqual(s.capacity, 8)
        self.assertEqual(ids(s), [1001 + i for i in range(8)])
        self.check_array(s)
        self.assertEqual(output.getvalue(), "")
    
    def test_rules_after_sorting(self):
        s = self.make()
        for r in generate_requests(50):
            s.append(r)
        s.sort_by_priority()
        self.check_array(s)
        s.sort_by_reported_time()
        self.check_array(s)

    # ----- binary search (array only; IDs must be in increasing order) -----

    def test_binary_search_trace_array(self):
        s = self.build(TRACE_IDS)
        self.assertEqual(s.findById_Binary(1048), 5)     # found: returns the position, not the ID
        self.assertEqual(s.findById_Binary(1030), -1)    # missing: between 1027 and 1033

    def test_binary_search_every_size(self):
        for size in range(len(TRACE_IDS) + 1):           # 0 to 8 elements
            id_list = TRACE_IDS[:size]
            s = self.build(id_list)
            with self.subTest(size=size):
                for position, request_id in enumerate(id_list):
                    self.assertEqual(s.findById_Binary(request_id), position)
                for missing in (1000, 1008, 1030, 1070, 3):  # below, between, between, above, an index
                    self.assertEqual(s.findById_Binary(missing), -1)

    def test_binary_search_does_not_print(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            s = self.build(TRACE_IDS)
            s.findById_Binary(1048)
            s.findById_Binary(1030)
            self.make().findById_Binary(1004)            # empty array
        self.assertEqual(output.getvalue(), "")
                         
class LinkedTests(SharedTests, unittest.TestCase):
    def make(self):
        return LinkedRequestList()

    def sort_priority(self, s):
        s.insertionSortPriority()

    def sort_time(self, s):
        s.mergeSortByTime()
    def check_linked(self, s):
        """Empty exactly when head is None, the chain ends in None,
        and count() matches the nodes reachable from head."""
        nodes = 0
        node = s.head
        while node is not None:
            nodes += 1
            self.assertLessEqual(nodes, 1000, "the chain never reaches None (a cycle?)")
            node = node.next
        self.assertEqual(s.head is None, nodes == 0)
        self.assertEqual(s.count(), nodes)

    def test_rules_through_empty_and_back(self):
        s = self.make()
        self.check_linked(s)                 # empty: head is None
        s.push(req(1004))
        self.check_linked(s)                 # one node, and its next is None
        s.removeAt(0)
        self.check_linked(s)                 # empty again: head back to None
        s.append(req(1011))                  # append onto an empty list
        self.check_linked(s)
        s.insertAt(0, req(1004))
        self.check_linked(s)

    def test_rules_after_each_insert_and_remove(self):
        s = self.build([1004, 1011, 1019])
        s.insertAt(0, req(1000))             # beginning
        self.check_linked(s)
        s.insertAt(2, req(1008))             # middle
        self.check_linked(s)
        s.insertAt(5, req(1030))             # end (n is 5 here)
        self.check_linked(s)
        s.removeAt(5)                        # end
        self.check_linked(s)
        s.removeAt(2)                        # middle
        self.check_linked(s)
        s.removeAt(0)                        # beginning
        self.check_linked(s)
        self.assertEqual(ids(s), [1004, 1011, 1019])

    def test_rules_after_sorting(self):
        requests = generate_requests(50)
        s = self.make()
        for r in requests:
            s.append(r)
        s.insertionSortPriority()
        self.check_linked(s)
        s.mergeSortByTime()
        self.check_linked(s)
        self.assertEqual(set(ids(s)), {r.request_id for r in requests})

class MaintenanceRequestTests(unittest.TestCase):
    def test_fields_and_default_status(self):
        r = MaintenanceRequest(1042, "CASE", "HVAC", 2, 184)
        self.assertEqual(r.request_id, 1042)
        self.assertEqual(r.building, "CASE")
        self.assertEqual(r.category, "HVAC")
        self.assertEqual(r.priority, 2)
        self.assertEqual(r.reported_time, 184)
        self.assertEqual(r.status, "OPEN")
        self.assertEqual(str(r), "#1042 CASE HVAC P2 t=184 OPEN")


class DatasetTests(unittest.TestCase):
    def test_same_seed_gives_same_requests(self):
        first = [str(r) for r in generate_requests(100, seed=7)]
        again = [str(r) for r in generate_requests(100, seed=7)]
        other = [str(r) for r in generate_requests(100, seed=8)]
        self.assertEqual(first, again)
        self.assertNotEqual(first, other)

    def test_ids_are_unique_at_largest_size(self):
        requests = generate_requests(25_000)              # the largest benchmark size
        self.assertEqual(len({r.request_id for r in requests}), 25_000)

    def test_fields_are_valid_and_cover_every_building(self):
        requests = generate_requests(200)
        for r in requests:
            self.assertIn(r.building, BUILDINGS)
            self.assertIn(r.category, CATEGORIES)
            self.assertIn(r.priority, (1, 2, 3, 4))
            self.assertEqual(r.status, "OPEN")
        self.assertEqual({r.building for r in requests}, set(BUILDINGS))
        
if __name__ == "__main__":
    unittest.main()