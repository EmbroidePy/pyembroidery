from __future__ import print_function

import unittest

from pattern_for_tests import *


class TestOverloads(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_pattern_equal(self):
        shift0 = get_shift_pattern()
        shift1 = get_shift_pattern()
        self.assertIsNot(shift0, shift1)
        self.assertEqual(shift0, shift1)

    def test_pattern_merge(self):
        shift0 = get_shift_pattern()
        shift1 = get_shift_pattern()
        shift0.add_command(END)
        last_pos = len(shift0) - 1
        self.assertEqual(shift0[last_pos][2], END)
        shift0 += shift1
        self.assertNotEqual(shift0[last_pos][2], END)

        shift2 = get_shift_pattern()
        shift3 = get_shift_pattern()
        shift2 += shift3

        self.assertEqual(shift0, shift2)

        shift4 = get_shift_pattern()

        self.assertEqual(shift4, shift3)
        self.assertEqual(shift4, shift1)
        shift1["name"] = "shifty"

        self.assertNotEqual(shift4, shift1)

    def test_pattern_merge_color(self):
        p0 = EmbPattern()
        p0 += "blue"
        p0 += ((0, 0), (1, 1), (2, 2))
        p0 += "red"
        p0 += ((4, 4))

        p1 = EmbPattern()
        p1 += "red"
        p1 += ((0, 0), (1, 1), (2, 2)) * 10
        p1 += "yellow"
        p1 += ((4, 4))

        p0 += p1
        self.assertEqual(p0.count_color_changes(), 2)

    def test_pattern_merge_color2(self):
        p0 = EmbPattern()
        p0 += COLOR_BREAK
        p0 += "blue"
        p0 += ((0, 0), (1, 1), (2, 2))
        p0 += "red"
        p0 += ((4, 4))

        p1 = EmbPattern()
        p1 += COLOR_BREAK
        p1 += "red"
        p1 += ((0, 0), (1, 1), (2, 2))
        p1 += "yellow"
        p1 += ((4, 4))

        p0 += p1
        self.assertEqual(p0.count_color_changes(), 2)

    def test_thread_equal(self):
        t0 = EmbThread("red")
        t1 = EmbThread("#F00")
        self.assertEqual(t0, t1)

    def test_matrix(self):
        m0 = EmbMatrix()
        m1 = EmbMatrix()
        m0.post_scale(2)
        m1.post_rotate(30)
        catted = m0.__matmul__(m1)  # might run in 2.7
        m2 = EmbMatrix()
        m2.post_scale(2)
        m2.post_rotate(30)
        self.assertEqual(catted, m2)


