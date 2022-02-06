# Infinite List

A list that spans infinitely in both directions

Values can be set and retrieved using functions, subscripts, or slices.

Using slices with steps other e.g. `li[0:10:2]` is not implemented yet. 

## Usage
```python
from infinite_list import InfiniteList

li = InfiniteList()
li[0] = 'a'
li[1:4] = 'b', 'c', 'd'
li[-7] = 'z'
li[2:] = 'w'
li[:5] = 'q'
```