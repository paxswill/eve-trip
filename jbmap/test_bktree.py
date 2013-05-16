import unittest
from jbmap import bktree

class TestMetric(unittest.TestCase):

    def assertTriangleInequality(self, a, b, c):
        # Identity
        self.assertAlmostEqual(bktree.euclidian(a, a), 0.0)
        self.assertAlmostEqual(bktree.euclidian(b, b), 0.0)
        self.assertAlmostEqual(bktree.euclidian(c, c), 0.0)
        # Reversal
        self.assertAlmostEqual(bktree.euclidian(a, b),
                               bktree.euclidian(b, a))
        self.assertAlmostEqual(bktree.euclidian(a, c),
                               bktree.euclidian(c, a))
        self.assertAlmostEqual(bktree.euclidian(c, b),
                               bktree.euclidian(b, c))
        # Combination
        self.assertGreaterEqual(bktree.euclidian(a, b) +
                                bktree.euclidian(b, c),
                                bktree.euclidian(a, c))
        self.assertGreaterEqual(bktree.euclidian(a, c) +
                                bktree.euclidian(c, b),
                                bktree.euclidian(a, b))
        self.assertGreaterEqual(bktree.euclidian(a, c) +
                                bktree.euclidian(a, b),
                                bktree.euclidian(c, b))


class TestEuclidian(TestMetric):

    def test_different_lengths(self):
        with self.assertRaises(AssertionError):
            bktree.euclidian((0, 0), (4, 4, 4))

    def test_one_dimensions(self):
        result = bktree.euclidian((0,), (5,))
        self.assertAlmostEqual(result, 5.0)

    def test_two_dimensions(self):
        result = bktree.euclidian((0, 0), (4, 4))
        self.assertAlmostEqual(result, 5.656854249)

    def test_three_dimensions(self):
        result = bktree.euclidian((0, 0, 0), (-2, -2, -4))
        self.assertAlmostEqual(result, 4.898979486)

    def test_triangle_inequality(self):
        a = (1, 2, 3)
        b = (4, 5, 6)
        c = (7, 8, 9)
        self.assertTriangleInequality(a, b, c)


class TestLevenshtein(unittest.TestCase):

    def test_identity(self):
        self.assertEqual(bktree.levenshtein('kitten', 'kitten'), 0)
        self.assertEqual(bktree.levenshtein('sitting', 'sitting'), 0)

    def test_substring(self):
        self.assertEqual(bktree.levenshtein('kitten', 'kittens'), 1)
        self.assertEqual(bktree.levenshtein('cat', 'catch'), 2)
        self.assertEqual(bktree.levenshtein('finding', 'fin'), 4)


if __name__ == '__main__':
    unittest.main()
