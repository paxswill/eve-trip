import unittest
from jbmap import bktree

class TestEuclidian(unittest.TestCase):

    def test_different_lengths(self):
        with self.assertRaises(AssertionError):
            bktree.euclidian_distance((0, 0), (4, 4, 4))

    def test_one_dimensions(self):
        result = bktree.euclidian_distance((0,), (5,))
        self.assertAlmostEqual(result, 5.0)

    def test_two_dimensions(self):
        result = bktree.euclidian_distance((0, 0), (4, 4))
        self.assertAlmostEqual(result, 5.656854249)

    def test_three_dimensions(self):
        result = bktree.euclidian_distance((0, 0, 0), (-2, -2, -4))
        self.assertAlmostEqual(result, 4.898979486)

    def test_triangle_inequality(self):
        a = (1, 2, 3)
        b = (4, 5, 6)
        c = (7, 8, 9)
        # Identity
        self.assertAlmostEqual(bktree.euclidian_distance(a, a), 0.0)
        self.assertAlmostEqual(bktree.euclidian_distance(b, b), 0.0)
        self.assertAlmostEqual(bktree.euclidian_distance(c, c), 0.0)
        # Reversal
        self.assertAlmostEqual(bktree.euclidian_distance(a, b),
                               bktree.euclidian_distance(b, a))
        self.assertAlmostEqual(bktree.euclidian_distance(a, c),
                               bktree.euclidian_distance(c, a))
        self.assertAlmostEqual(bktree.euclidian_distance(c, b),
                               bktree.euclidian_distance(b, c))
        # Combination
        self.assertGreaterEqual(bktree.euclidian_distance(a, b) +
                                bktree.euclidian_distance(b, c),
                                bktree.euclidian_distance(a, c))
        self.assertGreaterEqual(bktree.euclidian_distance(a, c) +
                                bktree.euclidian_distance(c, b),
                                bktree.euclidian_distance(a, b))
        self.assertGreaterEqual(bktree.euclidian_distance(a, c) +
                                bktree.euclidian_distance(a, b),
                                bktree.euclidian_distance(c, b))


if __name__ == '__main__':
    unittest.main()
