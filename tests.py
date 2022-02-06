import unittest
from copy import copy, deepcopy

import infinite_list


def contains_duplicates(iterable):
    seen_values = set()
    for item in iterable:
        if item in seen_values:
            return True

        seen_values.add(item)

    return False


class InfiniteListTestCase(unittest.TestCase):
    def test_read_from_empty_list(self):
        li = infinite_list.InfiniteList()

        actual = li[0]

        expected = None
        self.assertEqual(expected, actual)

    def test_changing_fill_value(self):
        li = infinite_list.InfiniteList(fill_value='hello')

        actual = li[0]

        expected = 'hello'
        self.assertEqual(expected, actual)

    def test_get_item_at_index_0(self):
        li = infinite_list.InfiniteList()
        li[0] = 1

        actual = li[0]

        expected = 1
        self.assertEqual(expected, actual)

    def test_get_item_at_negative_index(self):
        li = infinite_list.InfiniteList()
        li[-1] = 1

        actual = li[-1]

        expected = 1
        self.assertEqual(expected, actual)

    def test_get_item_at_large_index(self):
        li = infinite_list.InfiniteList()
        li[99999999] = 1

        actual = li[99999999]

        expected = 1
        self.assertEqual(expected, actual)

    def test_get_item_at_large_negative_index(self):
        li = infinite_list.InfiniteList()
        li[-99999999] = 1

        actual = li[-99999999]

        expected = 1
        self.assertEqual(expected, actual)

    def test_bounded_list_slice(self):
        li = infinite_list.InfiniteList()
        li[1:4] = 'a', 'b', 'c'
        li[5] = 'd'

        actual = li[0:7]

        expected = [None, 'a', 'b', 'c', None, 'd', None]
        self.assertEqual(expected, actual)

    def test_comparing_two_equal_lists(self):
        list_1 = infinite_list.InfiniteList()
        list_1[0:3] = 'a', 'b', 'c'
        list_1[5] = 'd'

        list_2 = infinite_list.InfiniteList()
        list_2[0:3] = 'a', 'b', 'c'
        list_2[5] = 'd'

        actual = list_1 == list_2

        expected = True
        self.assertEqual(expected, actual)

    def test_comparing_two_unequal_lists(self):
        list_1 = infinite_list.InfiniteList()
        list_1[0:3] = 'a', 'b', 'c'
        list_1[5] = 'd'

        list_2 = infinite_list.InfiniteList()
        list_2[0:3] = 'a', 'b', 'c'
        list_2[5] = 'e'

        actual = list_1 == list_2

        expected = False
        self.assertEqual(expected, actual)

    def test_left_unbounded_list_slice(self):
        li = infinite_list.InfiniteList()
        li[-7:-4] = 'a', 'b', 'c'
        li[2] = 'd'
        li[-2] = 'e'

        actual = li[:3]

        expected = infinite_list.LeftInfiniteList()
        expected[-9:1] = 'a', 'b', 'c', None, None, 'e', None, None, None, 'd'
        self.assertEqual(expected, actual)

    def test_right_unbounded_list_slice(self):
        li = infinite_list.InfiniteList()
        li[0:3] = 'a', 'b', 'c'
        li[5] = 'd'
        li[-2] = 'e'

        actual = li[1:]

        expected = infinite_list.RightInfiniteList()
        expected[0:2] = 'b', 'c'
        expected[4] = 'd'
        self.assertEqual(expected, actual)

    def test_left_and_right_unbounded_slice(self):
        li = infinite_list.InfiniteList()
        li[0:3] = 'a', 'b', 'c'
        li[5] = 'd'
        li[-2] = 'e'

        actual = li[:]

        expected = copy(li)
        self.assertEqual(expected, actual)

    def test_set_items_using_left_unbounded_slice_and_infinite_list(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li[-1] = 'w'
        li[-2] = 'x'
        li[-4] = 'y'
        li[:-7] = 'z'
        li_2 = infinite_list.InfiniteList(fill_value='b')
        li_2[-2] = 'c'
        li_2[-5] = 'd'
        li_2[:-6] = 'e'
        li[:-1] = li_2[:-1]

        actual = li[-9:1]

        expected = ['e', 'e', 'e', 'b', 'd', 'b', 'b', 'c', 'w', 'a']
        self.assertListEqual(expected, actual)

    def test_set_items_using_left_unbounded_slice_and_infinite_list_edge_case(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li[-1] = 'b'
        li[-5] = 'c'
        li[-2] = 'd'
        li_2 = infinite_list.InfiniteList(fill_value='x')
        li_2[-4] = 'y'
        li_2[-7] = 'z'
        li[:-2] = li_2[:-2]

        actual = li[-10:1]

        expected = ['x', 'x', 'x', 'z', 'x', 'x', 'y', 'x', 'd', 'b', 'a']
        self.assertListEqual(expected, actual)

    def test_set_items_using_right_unbounded_slice_and_infinite_list(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li[1] = 'w'
        li[2] = 'x'
        li[4] = 'y'
        li[8:] = 'z'
        li_2 = infinite_list.InfiniteList(fill_value='b')
        li_2[2] = 'c'
        li_2[5] = 'd'
        li_2[7:] = 'e'
        li[2:] = li_2[2:]

        actual = li[0:10]

        expected = ['a', 'w', 'c', 'b', 'b', 'd', 'b', 'e', 'e', 'e']
        self.assertListEqual(expected, actual)

    def test_set_items_using_right_unbounded_slice_and_infinite_list_edge_case(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li[1] = 'b'
        li[5] = 'c'
        li[2] = 'd'
        li_2 = infinite_list.RightInfiniteList(fill_value='x')
        li_2[1] = 'y'
        li_2[4] = 'z'
        li[3:] = li_2

        actual = li[0:10]

        expected = ['a', 'b', 'd', 'x', 'y', 'x', 'x', 'z', 'x', 'x']
        self.assertListEqual(expected, actual)

    def test_set_items_using_left_unbounded_slice_and_single_value(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li_2 = infinite_list.LeftInfiniteList(fill_value='b')
        li_3 = infinite_list.RightInfiniteList(fill_value='a')
        li[:5] = 'b'

        actual = li[:5], li[5:]

        expected = li_2, li_3
        self.assertTupleEqual(expected, actual)

    def test_set_items_using_right_unbounded_slice_and_single_value(self):
        li = infinite_list.InfiniteList(fill_value='b')
        li_2 = infinite_list.LeftInfiniteList(fill_value='b')
        li_3 = infinite_list.RightInfiniteList(fill_value='a')
        li[5:] = 'a'

        actual = li[:5], li[5:]

        expected = li_2, li_3
        self.assertTupleEqual(expected, actual)

    def test_set_items_using_right_unbounded_slice_twice(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li[5:] = 'b'
        li[10:] = 'c'

        actual = li[0:15]

        expected = ['a'] * 5 + ['b'] * 5 + ['c'] * 5
        self.assertListEqual(expected, actual)

    def test_overwrite_fill_value_right(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li[10:] = 'c'
        li[5:] = 'b'

        actual = li[0:15]

        expected = ['a'] * 5 + ['b'] * 10
        self.assertListEqual(expected, actual)

    def test_overwrite_fill_value_exactly_right(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li[5:] = 'b'
        li[5:] = 'c'

        actual = li[0:15]

        expected = ['a'] * 5 + ['c'] * 10
        self.assertListEqual(expected, actual)
        self.assertFalse(contains_duplicates(li._fill_value_list._indices))

    def test_overwrite_fill_value_exactly_right_with_more_values(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li[5:] = 'b'
        li[10:] = 'd'
        li[5:] = 'c'

        actual = li[0:15]

        expected = ['a'] * 5 + ['c'] * 10
        self.assertListEqual(expected, actual)
        self.assertFalse(contains_duplicates(li._fill_value_list._indices))

    def test_set_items_using_left_unbounded_slice_twice(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li[:-4] = 'b'
        li[:-9] = 'c'

        actual = li[-14:1]

        expected = ['c'] * 5 + ['b'] * 5 + ['a'] * 5
        self.assertListEqual(expected, actual)

    def test_overwrite_fill_value_left(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li[:-9] = 'c'
        li[:-4] = 'b'

        actual = li[-14:1]

        expected = ['b'] * 10 + ['a'] * 5
        self.assertListEqual(expected, actual)

    def test_overwrite_fill_value_exactly_left(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li[:-4] = 'b'
        li[:-4] = 'c'

        actual = li[-14:1]

        expected = ['c'] * 10 + ['a'] * 5
        self.assertListEqual(expected, actual)
        self.assertFalse(contains_duplicates(li._fill_value_list._indices))

    def test_overwrite_fill_value_exactly_left_with_more_values(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li[:-4] = 'b'
        li[:-9] = 'd'
        li[:-4] = 'c'

        actual = li[-14:1]

        expected = ['c'] * 10 + ['a'] * 5
        self.assertListEqual(expected, actual)
        self.assertFalse(contains_duplicates(li._fill_value_list._indices))

    def test_set_items_using_left_and_right_unbounded_slice_and_infinite_list(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li_2 = infinite_list.InfiniteList(fill_value='b')
        li[:] = li_2

        actual = li

        expected = li_2
        self.assertEqual(expected, actual)

    def test_set_items_using_left_and_right_unbounded_slice_and_single_value(self):
        li = infinite_list.InfiniteList(fill_value='a')
        li_2 = infinite_list.InfiniteList(fill_value='b')
        li[:] = 'b'

        actual = li

        expected = li_2
        self.assertEqual(expected, actual)

    def test_copy(self):
        li = infinite_list.InfiniteList()
        li[0] = 'a'
        li[100] = 'b'
        li[-100] = 'c'

        li_copy = copy(li)
        li_copy[0] = 'd'

        actual = li[0]

        expected = 'a'
        self.assertEqual(expected, actual)

    def test_deepcopy(self):
        li = infinite_list.InfiniteList()
        li[0] = 'a'
        li[100] = 'b'
        li[-100] = ['c', 'd', 'e']

        li_copy = deepcopy(li)
        li_copy[-100][0] = 'z'

        actual = li[-100][0]

        expected = 'c'
        self.assertEqual(expected, actual)

    def test_deepcopy_on_fill_values(self):
        li = infinite_list.InfiniteList()
        li[0:] = ['f', 'g', 'h']

        li_copy = deepcopy(li)
        li_copy[5][0] = 'z'

        actual = li[5][0]

        expected = 'f'
        self.assertEqual(expected, actual)

    def test_accessing_positive_index_of_left_infinite_list(self):
        li = infinite_list.LeftInfiniteList()

        with self.assertRaises(IndexError):
            li[1]

    def test_accessing_negative_index_of_left_infinite_list(self):
        li = infinite_list.LeftInfiniteList()
        li[-1] = 'a'

        actual = li[-1]

        expected = 'a'
        self.assertEqual(expected, actual)

    def test_iterate(self):
        li = infinite_list.RightInfiniteList()
        li[0] = 'a'
        li[1] = 'b'
        li[2] = 'c'

        actual = []
        li_iterable = iter(li)
        for _ in range(5):
            actual.append(next(li_iterable))

        expected = ['a', 'b', 'c', None, None]
        self.assertListEqual(expected, actual)

    def test_get_item_from_empty_list(self):
        li = infinite_list.InfiniteList()

        actual = li[0]

        expected = None
        self.assertEqual(expected, actual)

    def test_access_slice_containing_positive_values_from_left_infinite_list(self):
        li = infinite_list.LeftInfiniteList()

        with self.assertRaises(IndexError) as cm:
            li[-2:2]

        actual = cm.exception.args[0]
        expected = 'Tried to access positive index of LeftInfiniteList.'
        self.assertEqual(expected, actual)

    def test_access_slice_containing_negative_values_from_right_infinite_list(self):
        li = infinite_list.RightInfiniteList()

        with self.assertRaises(IndexError) as cm:
            li[-2:2]

        actual = cm.exception.args[0]
        expected = 'Tried to access negative index of RightInfiniteList.'
        self.assertEqual(expected, actual)

    def test_set_items_using_right_then_left_unbounded_slice(self):
        li = infinite_list.InfiniteList('a')
        li[2:] = 'b'
        li[:5] = 'c'

        actual = li[-7:7]

        expected = ['c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'b', 'b']
        self.assertListEqual(expected, actual)

    def test_overwrite_values_with_left_unbounded_slice(self):
        li = infinite_list.InfiniteList('a')
        li[-5] = 'b'
        li[:0] = 'c'

        actual = li[-5]

        expected = 'c'
        self.assertEqual(expected, actual)

    def test_overwrite_values_with_right_unbounded_slice(self):
        li = infinite_list.InfiniteList('a')
        li[5] = 'b'
        li[0:] = 'c'

        actual = li[5]

        expected = 'c'
        self.assertEqual(expected, actual)

    def test_set_using_bounded_slice_and_single_value(self):
        li = infinite_list.InfiniteList(0)
        li[0:5] = 1

        actual = li[0:10]

        expected = [1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
        self.assertListEqual(expected, actual)

    # TODO: Add functionality for slices with steps other than 1.
    # def test_set_using_bounded_slice_with_different_step_and_single_value(self):
    #     li = infinite_list.InfiniteList(1)
    #     li[0:10:2] = 0
    #
    #     actual = li[0:10]
    #
    #     expected = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]
    #     self.assertListEqual(expected, actual)

    def test_overwrite_only_value_in_fill_value_list_left(self):
        li = infinite_list.InfiniteList('a')
        li[0:] = 'b'

        actual = li[-2:2]

        expected = ['a', 'a', 'b', 'b']
        self.assertListEqual(expected, actual)

    def test_overwrite_only_value_in_fill_value_list_right(self):
        li = infinite_list.InfiniteList('a')
        li[:1] = 'b'

        actual = li[-2:2]

        expected = ['b', 'b', 'b', 'a']
        self.assertListEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
