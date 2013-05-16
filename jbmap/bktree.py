from math import sqrt, fsum
from math import pow as fpow
from itertools import starmap, repeat
from operator import sub
from collections import deque

def euclidian(p, q):
    """Compute the euclidian distance between two tuples of numbers.

    The tuples must be of the same length, and should both be numbers.
    """
    assert len(p) == len(q), \
        "Distance between tuples of unequal length doesn't work."
    # This function basically computes (formula in LaTeX)
    # $\sqrt{(p_1 - q_1)^2 + (p_2 - q_2)^2 + \ldots + (p_n - p_n)^2}$

    # coordinate_pairs is an iterable of tuples, with each tuple being made up
    # of the i-th element of p an q. It's prep for doing the subtraction and
    # summation later.
    coordinate_pairs = zip(p, q)
    # differences is an iterable of the difference between the items of each
    # item in coordinate_pairs
    differences = starmap(sub, coordinate_pairs)
    # raise differences to the second power (square them)
    raised_differences = map(lambda x: fpow(x, 2), differences)
    # Sum raised_differences in preparation for...
    sum_coordinates = fsum(raised_differences)
    # ...finding the square root and returning.
    return sqrt(sum_coordinates)


def levenshtein(p, q):
    """Compute the Levenshtein distance between two strings.
    """
    # This is based on the pseudocode on the Wikipedia article "Levenshtein
    # Distance", which is sourced from the article "The String-to-string
    # correction problem" by Robert A. Wagner and Michael J. Fischer.

    # TODO Optimize for space by not storing the entire distance matrix, only
    # the parts used.

    # Optimize some simple cases out
    if p == q:
        return 0
    if not p:
        return len(q)
    if not q:
        return len(p)
    # Create a |p|+1 by |q|+1 matrix initialized to zeros
    distance = [[0 for x in range(len(q) + 1)] for x in range(len(p) + 1)]
    # Empty string to the substring is equal to the length of the substring
    for index_p in range(1, len(p) + 1):
        distance[index_p][0] = index_p
    for index_q in range(1, len(q) + 1):
        distance[0][index_q] = index_q
    # Magic!
    for index_p, char_p in enumerate(p, 1):
        for index_q, char_q in enumerate(q, 1):
            # If the characters are equal, the distance is the same as the
            # previous value
            if char_p == char_q:
                distance[index_p][index_q] = distance[index_p - 1][index_q - 1]
            else:
                deletion = distance[index_p - 1][index_q] + 1
                insertion = distance[index_p][index_q - 1] + 1
                substitution = distance[index_p - 1][index_q - 1] + 1
                distance[index_p][index_q] = min(deletion, insertion,
                        substitution)
    return distance[-1][-1]


# TODO Add a Damerau-Levenshtein distance function


class BKTree(object):

    def __init__(self, metric, *args):
        """Create a BKTree object.

        metric is a callable that takes two arguments. The callable must
        satisfy the definition of a metric (in the mathematical sense; ie a
        distance function. The euclidian and levenshtein functions in
        the bktree module are examples of metric functions.

        Arguments given after metric will be added to the tree.
        """
        assert callable(metric), "The metric provided is not callable."
        self.metric = metric
        self.value = None
        self.leaves = {}
        if len(args) > 0:
            iterator = iter(args)
            self.value = next(iterator)
            for item in iterator:
                self.add(item)

    def __bool__(self):
        """Return True if there are >=1 items in the tree."""
        if self.value is not None:
            return True
        else:
            for leaf in self.leaves.values():
                if leaf:
                    return True
        return False

    def __contains__(self, item):
        """Check membership of an item in the tree.

        Equivalent to calling tree.search(item, 0)
        """
        results = self.search(item, 0)
        try:
            next(results)
        except StopIteration:
            return False
        else:
            return True

    def __len__(self):
        """Return the number of values in the tree.

        Note: This is currently an ineffcient operation. If all you need to do
        is check if the tree is empty, use truth value testing.
        """
        if self.value is not None:
            length = 1
        else:
            length = 0
        for leaf in self.leaves.values():
            length += len(leaf)
        return length

    def add(self, value):
        """Add a value to the Tree.

        If the given value is already in the tree, it is ignored.
        """
        if self.value is None:
            self.value = value
        elif self.value == value:
            return
        else:
            distance = self.metric(self.value, value)
            try:
                leaf = self.leaves[distance]
            except KeyError:
                self.leaves[distance] = BKTree(self.metric, value)
            else:
                leaf.add(value)

    def search(self, query, max_distance):
        """Returns an iterator of matching items.

        query is the item to search for/against.

        max_distance is the maximum distance a returned item can be from
        query.
        """
        distance = self.metric(self.value, query)
        if distance <= max_distance:
            yield self.value
        between = lambda d: (d <= (max_distance + distance) and
                                     d >= (max_distance - distance))
        for key in filter(between, self.leaves.keys()):
            # yield from was added in Python 3.3
            # yield from self.leaves[key].search(query, max_distance)
            for result in self.leaves[key].search(query, max_distance):
                yield result

    def walk_breadth(self):
        """Returns an iterator to traverse the tree in breadth-first order.
        """
        queue = deque(self)
        while len(queue) > 0:
            node = queue.popleft()
            yield node
            queue.append(node.leaves.values())

    def walk_postorder(self):
        """Returns an iterator to traverse the tree in depth-first, post-order.
        """
        for value in self.leaves.values():
            # NOTE Again, yield from in Python 3.3
            #yield from value.walk_postorder()
            for leaf_value in value.walk_postorder():
                yield leaf_value

    def walk_preorder(self):
        """Return an iterator to traverse the tree in depth-first, pre-order.

        This is equivalen to calling iter(tree)
        """
        yield self.value
        for value in self.leaves.values():
            # NOTE if support for Python >3.3 is dropped, yield from can be
            # used
            #yield from value.walk_preorder()
            for leaf_value in value.walk_preorder():
                yield leaf_value

    __iter__ = self.walk_preorder

