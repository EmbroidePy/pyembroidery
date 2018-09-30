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
        file1 = "file3.dst"
        pattern = EmbPattern()
        pattern.add_block([(0, 0), (0, 200)], "red")

        write_dst(pattern, file1)
        dst_pattern = read_dst(file1)
        self.assertIsNotNone(dst_pattern)
        self.assertEqual(dst_pattern.count_stitch_commands(STITCH), 2)
        self.assertEqual(dst_pattern.stitches[1][1], 100)
        print("dst: ", dst_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_dst_read_dst_divide(self):
        file1 = "file3.dst"
        pattern = EmbPattern()
        pattern.add_block([(0, 0), (0, 2)], "red")

        write_dst(pattern, file1, {"scale": 100, "long_stitch_contingency": CONTINGENCY_LONG_STITCH_SEW_TO})
        dst_pattern = read_dst(file1)
        self.assertIsNotNone(dst_pattern)
        self.assertEqual(dst_pattern.count_stitch_commands(STITCH), 3)
        self.assertEqual(dst_pattern.stitches[1][1], 100)
        print("dst: ", dst_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_csv_read_csv_raw(self):
        file1 = "file.csv"
        write_csv(get_simple_pattern(), file1, {"encode": False})
        csv_pattern = read_csv(file1)
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(csv_pattern.count_stitch_commands(COLOR_BREAK), 3)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_csv_read_csv_needle(self):
        file1 = "file2.csv"
        write_csv(get_simple_pattern(), "file2.csv", {"thread_change_command": NEEDLE_SET})
        csv_pattern = read_csv(file1)
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(csv_pattern.count_stitch_commands(NEEDLE_SET), 3)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        print("csv: ", csv_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_csv_read_csv_color(self):
        file1 = "file3.csv"
        write_csv(get_simple_pattern(), "file3.csv", {"thread_change_command": COLOR_CHANGE})
        csv_pattern = read_csv(file1)
        self.assertEqual(csv_pattern.count_stitch_commands(COLOR_CHANGE), 2)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)
        self.addCleanup(os.remove, file1)
