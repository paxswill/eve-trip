from math import sqrt, fsum
from math import pow as fpow
from itertools import starmap
from operator import sub

def euclidian_distance(p, q):
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
    # starmap is a variation on the standard map function. It feeds the tuples
    # form coordinate_pairs to the sub function (a function form of the
    # standard '-' operator). The output is then summed together with special
    # care taken to handling floating point values.
    sum_coordinates = fsum(starmap(sub, coordinate_pairs))
    # Square root the sum_coordinates and return 
    return sqrt(sum_coordinates)


class BKTree(object):
    def __init__(self, metric, initial=None):
        """Create a BKTree object.

        metric is a callable that takes two arguments. The callable must
        satisfy the definition of a metric (in the mathematical sense; ie a
        distance function. The euclidian_distance and levenshtein functions in
        the bktree module are examples of metric functions.

        initial is an iterable of objects to initialize the tree with.
        """
        self.metric = metric
        if initial:
            for item in initial:
                # TODO implement this
                pass
