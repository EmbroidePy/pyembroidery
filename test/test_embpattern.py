from __future__ import print_function

import unittest

from pattern_for_tests import *


class TestEmbpattern(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_needle_count_limit(self):
        pattern = EmbPattern()
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "red")
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "blue")
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "green")

    def test_write_dst_read_dst_long_jump(self):
        pattern = EmbPattern()
        pattern.add_block([(0, 0), (0, 200)], "red")

        write_dst(pattern, "file3.dst")
        dst_pattern = read_dst("file3.dst")
        self.assertIsNotNone(dst_pattern)
        self.assertEqual(dst_pattern.count_stitch_commands(STITCH), 2)
        self.assertEqual(dst_pattern.stitches[1][1], 100)
        print("dst: ", dst_pattern.stitches)

    def test_write_dst_read_dst_divide(self):
        pattern = EmbPattern()
        pattern.add_block([(0, 0), (0, 2)], "red")

        write_dst(pattern, "file3.dst", {"scale": 100, "long_stitch_contingency": CONTINGENCY_LONG_STITCH_SEW_TO})
        dst_pattern = read_dst("file3.dst")
        self.assertIsNotNone(dst_pattern)
        self.assertEqual(dst_pattern.count_stitch_commands(STITCH), 3)
        self.assertEqual(dst_pattern.stitches[1][1], 100)
        print("dst: ", dst_pattern.stitches)

    def test_write_csv_read_csv_raw(self):
        write_csv(get_simple_pattern(), "file.csv", {"encode": False})
        csv_pattern = read_csv("file.csv")
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(csv_pattern.count_stitch_commands(COLOR_BREAK), 3)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)

    def test_write_csv_read_csv_needle(self):
        write_csv(get_simple_pattern(), "file2.csv", {"thread_change_command": NEEDLE_SET})
        csv_pattern = read_csv("file2.csv")
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(csv_pattern.count_stitch_commands(NEEDLE_SET), 3)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        print("csv: ", csv_pattern.stitches)

    def test_write_csv_read_csv_color(self):
        write_csv(get_simple_pattern(), "file3.csv", {"thread_change_command": COLOR_CHANGE})
        csv_pattern = read_csv("file3.csv")
        self.assertEqual(csv_pattern.count_stitch_commands(COLOR_CHANGE), 2)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)
