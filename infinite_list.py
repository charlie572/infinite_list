from __future__ import annotations

from copy import copy, deepcopy
from typing import Any

from binary_search_tree import BinarySearchTree


class FillValueList:
    """Manages InfiniteList fill values

    When the values of an InfiniteList are set using an unbounded slice e.g. li[5:] = 'a', this data structure manages
    that functionality.

    The __add__ method is implemented to concatenate two FillValueLists. The finite regions of the lists must not
    overlap. The finite region is the range of values inside FillValueList._indices.
    """
    def __init__(self, fill_value):
        # These lists store the fill values at every index. For the indices in between, use the first value to the left.
        # For example, if _indices = [0, 5, 10] and _fill_values = ['a', 'b', 'c'], then the value at index -1, 0, 1, 5,
        # 6, 10, and 11 are 'a', 'a', 'a', 'b', 'b', 'c' and 'c' respectively.
        self._indices = [0]
        self._fill_values = [fill_value]

    def get_fill_value_at_index(self, index: int):
        # check if index is in the finite region
        if index <= self._indices[0]:
            return self._fill_values[0]
        if index >= self._indices[-1]:
            return self._fill_values[-1]

        # find first index to the left
        for i, current_index in enumerate(self._indices):
            if index < current_index:
                break

        return self._fill_values[i - 1]

    def set_fill_values_to_left(self, index: int, fill_value: Any):
        """Set the value of all indices less than or equal to the given index"""
        if len(self._indices) == 1 and index == self._indices[-1]:
            # overwrite the only value in the list
            self._indices = [index, index + 1]
            self._fill_values = [fill_value, self._fill_values[0]]
        if len(self._indices) == 1 or index > self._indices[-1]:
            # index is all the way on the right of the finite region, or there is currently only one value
            self._indices = [index, index + 1]
            self._fill_values = [fill_value, self._fill_values[-1]]
            return

        for i, current_index in enumerate(self._indices):
            if index == current_index:
                # index is exactly on a value
                self._fill_values = [fill_value] + self._fill_values[i + 1:]
                return
            if index < current_index:
                # current index is the first index to the right of index
                self._indices = [index, index + 1] + self._indices[i + 1:]
                self._fill_values = [fill_value] + self._fill_values[i:]
                return

    def set_fill_values_to_right(self, index: int, fill_value: Any):
        """Set the value of all indices greater than or equal to the given index"""
        if len(self._indices) == 1 and index == self._indices[-1]:
            # overwrite the only value in the list
            self._indices = [index - 1, index]
            self._fill_values = [self._fill_values[0], fill_value]
        if len(self._indices) == 1 or index > self._indices[-1]:
            # index is all the way on the right of the finite region, or there is currently only one value
            self._indices.append(index)
            self._fill_values.append(fill_value)
            return

        for i, current_index in enumerate(self._indices):
            if index == current_index:
                # index is exactly on a value
                self._indices = self._indices[:i + 1]
                self._fill_values = self._fill_values[:i] + [fill_value]
                return
            if index < current_index:
                # current index is the first index to the right of index
                self._indices = self._indices[:i] + [index]
                self._fill_values = self._fill_values[:i] + [fill_value]
                return

    def set_fill_values_in_range(self, fill_value, start: int, stop: int):
        left = self.get_left_half(start, keep_indices=True)
        right = self.get_right_half(stop, keep_indices=True)
        left.set_fill_values_to_right(start, fill_value)
        result = left + right

        self._indices = result._indices
        self._fill_values = result._fill_values

    def get_left_half(self, index: int, keep_indices: bool = False) -> FillValueList:
        """Get a new FillValueList with all the values less than or equal to the given index

        :param index: Index on which to split the FillValueList
        :param keep_indices: If true, the indices of the result will match up to the original list. Else, the point
                             where the list was split will be at index 0.
        :return: Left half of list
        """
        if self._indices[0] > index:
            # Result is all the way on the left of the finite region. It only contains one value.
            result = FillValueList(None)
            result._indices = [index]
            result._fill_values = self._fill_values[:1]
            return result

        # find the first index to the right of the given index
        for i, current_index in enumerate(self._indices):
            if index < current_index:
                break
        else:
            i += 1

        # create result
        result = FillValueList(None)
        result._indices = self._indices[:i]
        result._fill_values = self._fill_values[:i]

        if not keep_indices:
            # shift indices so the point at which the list was split is at index 0
            result.shift(-index)

        return result

    def get_right_half(self, index: int, keep_indices: bool = False):
        """Get a new FillValueList with all the values greater than or equal to the given index

        :param index: Index on which to split the FillValueList
        :param keep_indices: If true, the indices of the result will match up to the original list. Else, the point
                             where the list was split will be at index 0.
        :return: Right half of list
        """
        if self._indices[0] > index:
            # Result contains whole of finite region.
            result = FillValueList(None)
            result._indices = [index] + self._indices[1:]
            result._fill_values = self._fill_values.copy()
            return result

        # find the first index to the right of the given index
        for i, current_index in enumerate(self._indices):
            if index < current_index:
                break
        else:
            i += 1

        # create result
        result = FillValueList(None)
        result._indices = [index] + self._indices[i:]
        result._fill_values = self._fill_values[i - 1:]

        if not keep_indices:
            # shift indices so the point at which the list was split is at index 0
            result.shift(-index)

        return result

    def shift(self, shift: int):
        """Shift all values right by the given amount"""
        for i in range(len(self._indices)):
            self._indices[i] += shift

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f'Tried to compare {type(self)} with {type(other)}.')

        return (self._indices == other._indices or len(self._indices) == len(other._indices) == 1) and \
               self._fill_values == other._fill_values

    def __add__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f'Cannot concatenate {type(self)} with {type(other)}.')
        if self._indices[-1] >= other._indices[0]:
            raise RuntimeError('Cannot concatenate overlapping fill value lists.')

        result = copy(self)
        result._indices += other._indices
        result._fill_values += other._fill_values

        return result

    def __copy__(self):
        result = FillValueList(None)
        result._indices = self._indices.copy()
        result._fill_values = self._fill_values.copy()
        return result


class InfiniteList:
    """A list that spans infinitely in both directions

    Values can be set and retrieved using functions, subscripts, or slices.

    Example:
    >>> li = InfiniteList()
    >>> li[0] = 'a'
    >>> li[1:4] = 'b', 'c', 'd'
    >>> li[-7] = 'z'
    >>> li[2:] = 'w'
    >>> li[:5] = 'q'

    :param fill_value: Every element of the list is initialised to this value.
    """

    def __init__(self, fill_value=None):
        self._tree = BinarySearchTree()
        self._fill_value_list = FillValueList(fill_value)

    def _prune_tree(self, index: int, half_to_keep: str):
        """Prune tree so it only contains values to the left or right of the given index

        :param index: Index at which to prune. This index will be included in the resulting tree.
        :param half_to_keep: 'left' or 'right'
        """
        new_tree = BinarySearchTree()
        for node in self._tree.traverse('pre', values_only=False):
            if half_to_keep == 'left' and node.key > index:
                continue
            if half_to_keep == 'right' and node.key < index:
                continue

            new_tree.set_item(node.key, node.value)

        self._tree = new_tree

    def set_value(self, index: int, value):
        """Set a single value

        li.set_value(index, value) is equivalent to li[index] = value.
        """
        self._tree.set_item(index, value)

    def set_all_values_to_left(self, index: int, value):
        """Set all values less than or equal to the given index to the same value

        li.set_all_values_to_left(index, value) is equivalent to li[:index + 1] = value.
        """
        self._prune_tree(index + 1, 'right')
        self._fill_value_list.set_fill_values_to_left(index, value)

    def set_all_values_to_right(self, index: int, value):
        """Set all values greater than or equal to the given index to the same value

        li.set_all_values_to_right(index, value) is equivalent to li[index:] = value.
        """
        self._prune_tree(index - 1, 'left')
        self._fill_value_list.set_fill_values_to_right(index, value)

    def set_all_values(self, value):
        """Set all values to the same value

        li.set_all_values(value) is equivalent to li[:] = value.
        """
        self._tree = BinarySearchTree()
        self._fill_value_list = FillValueList(value)

    def set_all_values_in_range(self, value, start, stop):
        # remove nodes of tree in the given range
        new_tree = BinarySearchTree()
        for node in self._tree.traverse('in'):
            if start <= node.key < stop:
                continue

            new_tree.set_item(node.key, node.value)

        self._tree = new_tree

        # update fill value list
        self._fill_value_list.set_fill_values_in_range(value, start, stop)


    def put_left_infinite_list_at_index(self, index: int, left_infinite_list: LeftInfiniteList):
        """Set all values less than or equal to the given index using a LeftInfiniteList

        Index 0 in the LeftInfiniteList will be put at the given index.

        li.put_left_infinite_list_at_index(index, left_infinite_list) is equivalent to
        li[:index + 1] = left_infinite_list.
        """
        self._prune_tree(index + 1, 'right')

        # traverse other tree and set values
        for node in left_infinite_list._tree.traverse('in', values_only=False):
            self._tree.set_item(index + node.key, node.value)

        # update fill value list
        self._fill_value_list = self._fill_value_list.get_right_half(index + 1, keep_indices=True)
        new_fill_value_list = copy(left_infinite_list._fill_value_list)
        new_fill_value_list.shift(index)
        self._fill_value_list = new_fill_value_list + self._fill_value_list

    def put_right_infinite_list_at_index(self, index: int, right_infinite_list: RightInfiniteList):
        """Set all values greater than or equal to the given index using a RightInfiniteList

        Index 0 in the RightInfiniteList will be put at the given index.

        li.put_right_infinite_list_at_index(index, right_infinite_list) is equivalent to
        li[index:] = right_infinite_list.
        """
        self._prune_tree(index - 1, 'left')

        # traverse other tree and set values
        for node in right_infinite_list._tree.traverse('in', values_only=False):
            self._tree.set_item(index + node.key, node.value)

        # update fill value list
        self._fill_value_list = self._fill_value_list.get_left_half(index - 1, keep_indices=True)
        new_fill_value_list = copy(right_infinite_list._fill_value_list)
        new_fill_value_list.shift(index)
        self._fill_value_list = self._fill_value_list + new_fill_value_list

    def copy_infinite_list_into_self(self, infinite_list: InfiniteList):
        """Set self to a shallow copy of the given InfiniteList

        li.copy_infinite_list_into_self(infinite_list) is equivalent to li[:] = infinite_list."""
        self._tree = copy(infinite_list._tree)
        self._fill_value_list = copy(infinite_list._fill_value_list)

    def get_value(self, index: int):
        """Get a single value"""
        return self._tree.get_item(index) or self._fill_value_list.get_fill_value_at_index(index)

    def get_all_values_to_left(self, index: int) -> LeftInfiniteList:
        """Get a LeftInfiniteList with all the values less than or equal to the given index"""
        result = LeftInfiniteList()
        result._fill_value_list = self._fill_value_list.get_left_half(index)
        for node in self._tree.traverse('in', values_only=False):
            if node.key > index:
                break

            result[node.key - index] = node.value

        return result

    def get_all_values_to_right(self, index: int) -> RightInfiniteList:
        """Get a RightInfiniteList with all the values greater than or equal to the given index"""
        result = RightInfiniteList()
        result._fill_value_list = self._fill_value_list.get_right_half(index)
        for node in self._tree.traverse('in reversed', values_only=False):
            if node.key < index:
                break

            result[node.key - index] = node.value

        return result

    def __setitem__(self, key, value):
        if not isinstance(key, slice):
            # set a single value
            self.set_value(key, value)
        elif key.start is key.stop is None:
            # left and right unbounded slice
            if isinstance(value, InfiniteList):
                self.copy_infinite_list_into_self(value)
            else:
                self.set_all_values(value)
        elif key.start is None:
            # left unbounded slice
            if isinstance(value, LeftInfiniteList):
                self.put_left_infinite_list_at_index(key.stop - 1, value)
            else:
                self.set_all_values_to_left(key.stop - 1, value)
        elif key.stop is None:
            # right unbounded slice
            if isinstance(value, RightInfiniteList):
                self.put_right_infinite_list_at_index(key.start, value)
            else:
                self.set_all_values_to_right(key.start, value)
        else:
            # bounded slice
            if hasattr(value, '__iter__'):
                for k, v in zip(range(key.start, key.stop, key.step or 1), value):
                    self.set_value(k, v)
            else:
                self.set_all_values_in_range(value, key.start, key.stop)

    def __getitem__(self, key):
        if not isinstance(key, slice):
            # get a single value
            return self.get_value(key)
        elif key.start is None and key.stop is None:
            # left and right unbounded slice
            return copy(self)
        elif key.start is not None and key.stop is not None:
            # bonded slice
            return [self.get_value(k) for k in range(key.start, key.stop, key.step or 1)]
        elif key.start is None:
            # left unbounded slice
            return self.get_all_values_to_left(key.stop - 1)
        else:
            # right unbounded slice
            return self.get_all_values_to_right(key.start)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            raise TypeError(f'Cannot compare {type(self)} with {type(other)}')
        if self._fill_value_list != other._fill_value_list:
            return False

        # check each node in self
        for node in self._tree.traverse('pre', values_only=False):
            if other.get_value(node.key) != node.value:
                return False

        # check each node in other
        for node in other._tree.traverse('pre', values_only=False):
            if node.value != self.get_value(node.key):
                return False

        return True

    def __copy__(self):
        result = self.__class__()
        result._tree = copy(self._tree)
        result._fill_value_list = copy(self._fill_value_list)
        return result

    def __deepcopy__(self, memodict=None):
        memodict = memodict or {}

        result = self.__class__()
        result._tree = deepcopy(self._tree, memodict)
        result._fill_value_list = deepcopy(self._fill_value_list, memodict)
        return result


class LeftInfiniteList(InfiniteList):
    """A list that extends infinitely to the left

    :param fill_value: Every element of the list is initialised to this value.
    """
    def __init__(self, fill_value=None):
        super().__init__(fill_value=fill_value)

    @staticmethod
    def _raise_errors(index):
        if index > 0:
            raise IndexError('Tried to access positive index of LeftInfiniteList.')

    def _prune_tree(self, index: int, half_to_keep: str):
        self._raise_errors(index)
        super()._prune_tree(index, half_to_keep)

    def set_value(self, index: int, value):
        self._raise_errors(index)
        super().set_value(index, value)

    def set_all_values_to_left(self, index: int, value):
        self._raise_errors(index)
        super().set_all_values_to_left(index, value)

    def set_all_values_to_right(self, index: int, value):
        self._raise_errors(index)
        super().set_all_values_to_right(index, value)

    def put_left_infinite_list_at_index(self, index: int, left_infinite_list: LeftInfiniteList):
        self._raise_errors(index)
        super().put_left_infinite_list_at_index(index, left_infinite_list)

    def put_right_infinite_list_at_index(self, index: int, left_infinite_list: LeftInfiniteList):
        self._raise_errors(index)
        super().put_left_infinite_list_at_index(index, left_infinite_list)

    def get_value(self, index: int):
        self._raise_errors(index)
        return super().get_value(index)

    def get_all_values_to_left(self, index: int) -> LeftInfiniteList:
        self._raise_errors(index)
        return super().get_all_values_to_left(index)

    def get_all_values_to_right(self, index: int) -> RightInfiniteList:
        return self[index:1]


class RightInfiniteList(InfiniteList):
    """A list that extends infinitely to the right

    :param fill_value: Every element of the list is initialised to this value.
    """
    def __init__(self, fill_value=None):
        super().__init__(fill_value=fill_value)

    @staticmethod
    def _raise_errors(index):
        if index < 0:
            raise IndexError('Tried to access negative index of RightInfiniteList.')

    def _prune_tree(self, index: int, half_to_keep: str):
        self._raise_errors(index)
        super()._prune_tree(index, half_to_keep)

    def set_value(self, index: int, value):
        self._raise_errors(index)
        super().set_value(index, value)

    def set_all_values_to_left(self, index: int, value):
        self._raise_errors(index)
        super().set_all_values_to_left(index, value)

    def set_all_values_to_right(self, index: int, value):
        self._raise_errors(index)
        super().set_all_values_to_right(index, value)

    def put_left_infinite_list_at_index(self, index: int, left_infinite_list: LeftInfiniteList):
        self._raise_errors(index)
        super().put_left_infinite_list_at_index(index, left_infinite_list)

    def put_right_infinite_list_at_index(self, index: int, left_infinite_list: LeftInfiniteList):
        self._raise_errors(index)
        super().put_left_infinite_list_at_index(index, left_infinite_list)

    def get_value(self, index: int):
        self._raise_errors(index)
        return super().get_value(index)

    def get_all_values_to_left(self, index: int) -> LeftInfiniteList:
        self._raise_errors(index)
        return self[0:index + 1]

    def get_all_values_to_right(self, index: int) -> RightInfiniteList:
        return super().get_all_values_to_right(index)
