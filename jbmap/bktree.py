from math import sqrt, fsum
from math import pow as fpow
from itertools import starmap, repeat
from operator import sub

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

    # Create a |p|+1 by |q|+1 matrix initialized to zeros
    distance = list(repeat(list(repeat(0, len(q) + 1)), len(p) + 1))
    # Empty string to the substring is equal to the length of the substring
    for index_p in range(1, len(p) + 1):
        distance[index_p][0] = index_p
    for index_q in range(1, len(q) + 1):
        distance[0][index_q] = index_q
    # Magic!
    for index_p, char_p in enumerate(1, p):
        for index_q, char_q in enumerate(1, q):
            # If the characters are equal, the distance is the same as the
            # previous value
            if char_p == char_q:
                distance[index_p][index_q] = distance[index_p - 1][index_q - 1]
            else:
                deletion = distance[index_p - 1][index_j] + 1
                insertion = distance[index_p, index_q - 1] + 1
                substitution = distance[index_p - 1][index_1 - 1] + 1
                distance[index_p][index_q] = min(deletion, insertion,
                        substitution)
    return distance[-1][-1]


# TODO Add a Damerau-Levenshtein distance function


class BKTree(object):
    def __init__(self, metric, initial=None):
        """Create a BKTree object.

        metric is a callable that takes two arguments. The callable must
        satisfy the definition of a metric (in the mathematical sense; ie a
        distance function. The euclidian and levenshtein functions in
        the bktree module are examples of metric functions.

        initial is an iterable of objects to initialize the tree with.
        """
        assert callable(metric), "The metric provided is not callable."
        self.metric = metric
        if initial:
            for item in initial:
                # TODO implement this
                pass
