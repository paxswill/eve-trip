import unittest
from jbmap import bktree

class TestMetric(unittest.TestCase):

    def assertTriangleInequality(self, metric, a, b, c):
        # Identity
        self.assertAlmostEqual(metric(a, a), 0.0)
        self.assertAlmostEqual(metric(b, b), 0.0)
        self.assertAlmostEqual(metric(c, c), 0.0)
        # Reversal
        self.assertAlmostEqual(metric(a, b), metric(b, a))
        self.assertAlmostEqual(metric(a, c), metric(c, a))
        self.assertAlmostEqual(metric(c, b), metric(b, c))
        # Combination
        self.assertGreaterEqual(metric(a, b) + metric(b, c), metric(a, c))
        self.assertGreaterEqual(metric(a, c) + metric(c, b), metric(a, b))
        self.assertGreaterEqual(metric(a, c) + metric(a, b), metric(c, b))


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
        self.assertTriangleInequality(bktree.euclidian, a, b, c)


class TestLevenshtein(TestMetric):

    def test_identity(self):
        self.assertEqual(bktree.levenshtein('kitten', 'kitten'), 0)
        self.assertEqual(bktree.levenshtein('sitting', 'sitting'), 0)

    def test_substring(self):
        self.assertEqual(bktree.levenshtein('kitten', 'kittens'), 1)
        self.assertEqual(bktree.levenshtein('cat', 'catch'), 2)
        self.assertEqual(bktree.levenshtein('finding', 'fin'), 4)

    def test_nothing_in_common(self):
        self.assertEqual(bktree.levenshtein('', 'foobarbaz'), 9)

    def test_wikipedia_examples(self):
        self.assertEqual(bktree.levenshtein('kitten', 'sitting'), 3)
        self.assertEqual(bktree.levenshtein('Sunday', 'Saturday'), 3)

    def test_triangle_inequality(self):
        a = 'kitten'
        b = 'mitten'
        c = 'sitting'
        self.assertTriangleInequality(bktree.levenshtein, a, b, c)


if __name__ == '__main__':
    unittest.main()
