from __future__ import print_function

import unittest

from pattern_for_tests import *


class TestEmbpattern(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_needle_count_limited_set(self):
        needle_file = "needle-ls.u01"
        shift = get_shift_pattern()
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, None, 3, 1))
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, 4, 6, 7))
        write_u01(shift, needle_file, {"needle_count": 7})
        needle_pattern = read_u01(needle_file)
        self.assertEqual(needle_pattern.count_stitch_commands(NEEDLE_SET), 16)
        first = True
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            print(cmd)
            if first:
                self.assertEqual(cmd[2], 3)
                first = False
            self.assertLessEqual(cmd[2], 7)
        self.addCleanup(os.remove, needle_file)

    def test_needle_count_limit1(self):
        needle_file = "needle-1.u01"
        write_u01(get_shift_pattern(), needle_file, {"needle_count": 1})
        needle_pattern = read_u01(needle_file)
        self.assertEqual(needle_pattern.count_stitch_commands(STOP), 16)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLess(cmd[2], 1)
        self.addCleanup(os.remove, needle_file)

    def test_needle_count_limit2(self):
        needle_file = "needle.u01"
        write_u01(get_shift_pattern(), needle_file, {"needle_count": 2})
        needle_pattern = read_u01(needle_file)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 2)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.addCleanup(os.remove, needle_file)

    def test_needle_count_limit3(self):
        needle_file = "needle.u01"
        write_u01(get_shift_pattern(), needle_file, {"needle_count": 3})
        needle_pattern = read_u01(needle_file)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 3)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.addCleanup(os.remove, needle_file)

    def test_needle_count_limit4(self):
        needle_file = "needle.u01"
        write_u01(get_shift_pattern(), needle_file, {"needle_count": 4})
        needle_pattern = read_u01(needle_file)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 4)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.addCleanup(os.remove, needle_file)

    def test_needle_count_limit5(self):
        needle_file = "needle.u01"
        write_u01(get_shift_pattern(), needle_file, {"needle_count": 5})
        needle_pattern = read_u01(needle_file)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 5)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.addCleanup(os.remove, needle_file)

    def test_needle_count_limit6(self):
        needle_file = "needle.u01"
        write_u01(get_shift_pattern(), needle_file, {"needle_count": 6})
        needle_pattern = read_u01(needle_file)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 6)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.addCleanup(os.remove, needle_file)

    def test_needle_count_limit7(self):
        needle_file = "needle.u01"
        write_u01(get_shift_pattern(), needle_file, {"needle_count": 7})
        needle_pattern = read_u01(needle_file)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 7)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.addCleanup(os.remove, needle_file)

    def test_needle_count_limit8(self):
        needle_file = "needle.u01"
        write_u01(get_shift_pattern(), needle_file, {"needle_count": 8})
        needle_pattern = read_u01(needle_file)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 8)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.addCleanup(os.remove, needle_file)

    def test_needle_count_limit9(self):
        needle_file = "needle.u01"
        write_u01(get_shift_pattern(), needle_file, {"needle_count": 9})
        needle_pattern = read_u01(needle_file)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 9)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.addCleanup(os.remove, needle_file)

    def test_needle_count_limit10(self):
        needle_file = "needle.u01"
        write_u01(get_shift_pattern(), needle_file, {"needle_count": 10})
        needle_pattern = read_u01(needle_file)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 10)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.addCleanup(os.remove, needle_file)

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
