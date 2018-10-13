from __future__ import print_function

import unittest

from pattern_for_tests import *


class TestEmbpattern(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_thread_reorder(self):
        test_file = "reorder.pes"
        shift = get_shift_pattern()
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, 0, None, 1))
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, 1, None, 0))
        self.assertEqual(0xFFFFFF & shift.threadlist[0].color, 0xFF0000)
        self.assertEqual(0xFFFFFF & shift.threadlist[1].color, 0x0000FF)
        write_pes(shift, test_file, {"pes version": 6})
        read_pattern = read_pes(test_file)
        for thread in read_pattern.threadlist:
            print(0xFFFFFF & thread.color)
        self.assertEqual((0xFFFFFF & read_pattern.threadlist[0].color), 0x0000FF)
        self.assertEqual((0xFFFFFF & read_pattern.threadlist[1].color), 0xFF0000)
        self.addCleanup(os.remove, test_file)

    def test_needle_count_limited_set(self):
        needle_file = "needle-ls.u01"
        shift = get_shift_pattern()
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, None, 6, 0))
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, 4, 6, 7))
        shift.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, None, 3, 0))
        write_u01(shift, needle_file, {"needle_count": 7})
        needle_pattern = read_u01(needle_file)
        self.assertEqual(needle_pattern.count_stitch_commands(NEEDLE_SET), 16)
        first = True
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            print(cmd)
            if first:
                # self.assertEqual(cmd[2], 3)
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

    def test_u01_tie_on(self):
        needle_file = "tie_on.u01"
        write_u01(get_shift_pattern(), needle_file, {"needle_count": 10, "tie_on": CONTINGENCY_TIE_ON_THREE_SMALL})
        needle_pattern = read_u01(needle_file)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 10)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.assertEqual(needle_pattern.count_stitch_commands(STITCH), 16 * (5 + 4))
        # 5 for the actual stitch pattern. 3 small, and 1 extra tieon, start.
        self.addCleanup(os.remove, needle_file)

    def test_u01_tie_off(self):
        needle_file = "tie_on.u01"
        write_u01(get_shift_pattern(), needle_file, {"needle_count": 10, "tie_off": CONTINGENCY_TIE_OFF_THREE_SMALL})
        needle_pattern = read_u01(needle_file)
        for stitch in needle_pattern.get_match_commands(NEEDLE_SET):
            cmd = decode_embroidery_command(stitch[2])
            self.assertLessEqual(cmd[2], 10)
        self.assertEqual(needle_pattern.count_needle_sets(), 16)
        self.assertEqual(needle_pattern.count_stitch_commands(STITCH), 16 * (5 + 4))
        # 5 for the actual stitch pattern. 3 small, and 1 extra tieoff, end.
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
        write_csv(get_simple_pattern(), file1)
        csv_pattern = read_csv(file1)
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(csv_pattern.count_stitch_commands(COLOR_BREAK), 3)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_csv_read_csv_needle(self):
        file1 = "file2.csv"
        write_csv(get_simple_pattern(), "file2.csv", {"thread_change_command": NEEDLE_SET, "encode": True})
        csv_pattern = read_csv(file1)
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(csv_pattern.count_stitch_commands(NEEDLE_SET), 3)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        print("csv: ", csv_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_csv_read_csv_color(self):
        file1 = "file3.csv"
        write_csv(get_simple_pattern(), "file3.csv", {"thread_change_command": COLOR_CHANGE, "encode": True})
        csv_pattern = read_csv(file1)
        self.assertEqual(csv_pattern.count_stitch_commands(COLOR_CHANGE), 2)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_csv_read_csv_encoded_command(self):
        file1 = "file-encoded.csv"
        pattern = EmbPattern()
        encoded_command = encode_thread_change(SET_CHANGE_SEQUENCE, 3, 4, 1)
        pattern.add_command(encoded_command)
        write_csv(pattern, file1)
        csv_pattern = read_csv(file1)
        self.assertIsNotNone(csv_pattern)
        print("csv-encoded: ", csv_pattern.stitches)
        self.assertEqual(encoded_command, csv_pattern.stitches[-1][2])
        self.addCleanup(os.remove, file1)

    def test_transcode_to_self(self):
        pattern = get_shift_pattern()
        from pyembroidery.EmbEncoder import Transcoder
        encoder = Transcoder()
        encoder.transcode(pattern, pattern)
        self.assertNotEquals(len(pattern.stitches), 0)
