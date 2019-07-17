from __future__ import print_function

import unittest

from pattern_for_tests import *
from pyembroidery import *


class TestWrites(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_write_png(self):
        file1 = "file.png"
        write_png(get_shift_pattern(), file1, {"background": "#F00", "linewidth": 5})
        self.addCleanup(os.remove, file1)

    def test_write_dst_read_dst(self):
        file1 = "file.dst"
        write_dst(get_big_pattern(), file1)
        dst_pattern = read_dst(file1)
        self.assertEqual(len(dst_pattern.threadlist), 0)
        self.assertEqual(dst_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(dst_pattern)
        self.assertEqual(dst_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(dst_pattern.stitches, 0, -1)
        print("dst: ", dst_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_exp_read_exp(self):
        file1 = "file.exp"
        write_exp(get_big_pattern(), file1)
        exp_pattern = read_exp(file1)
        self.assertEqual(len(exp_pattern.threadlist), 0)
        self.assertEqual(exp_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(exp_pattern)
        self.assertEqual(exp_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(exp_pattern.stitches, 0, -1)
        print("exp: ", exp_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_vp3_read_vp3(self):
        file1 = "file.vp3"
        write_vp3(get_big_pattern(), file1)
        vp3_pattern = read_vp3(file1)
        self.assertEqual(len(vp3_pattern.threadlist), vp3_pattern.count_stitch_commands(COLOR_CHANGE) + 1)
        self.assertEqual(vp3_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(vp3_pattern)
        self.assertEqual(vp3_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(vp3_pattern.stitches, 0, -1)
        print("vp3: ", vp3_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_jef_read_jef(self):
        file1 = "file.jef"
        write_jef(get_big_pattern(), file1)
        jef_pattern = read_jef(file1)
        self.assertEqual(len(jef_pattern.threadlist), jef_pattern.count_stitch_commands(COLOR_CHANGE) + 1)
        self.assertEqual(jef_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(jef_pattern)
        self.assertEqual(jef_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(jef_pattern.stitches, 0, -1)
        print("jef: ", jef_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_pec_read_pec(self):
        file1 = "file.pec"
        write_pec(get_big_pattern(), file1)
        pec_pattern = read_pec(file1)
        self.assertEqual(len(pec_pattern.threadlist), pec_pattern.count_stitch_commands(COLOR_CHANGE) + 1)
        self.assertEqual(pec_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(pec_pattern)
        self.assertEqual(pec_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(pec_pattern.stitches, 0, -1)
        print("pec: ", pec_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_pes_read_pes(self):
        file1 = "file.pes"
        write_pes(get_big_pattern(), file1)
        pes_pattern = read_pes(file1)
        self.assertEqual(len(pes_pattern.threadlist), pes_pattern.count_stitch_commands(COLOR_CHANGE) + 1)
        self.assertEqual(pes_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(pes_pattern)
        self.assertEqual(pes_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(pes_pattern.stitches, 0, -1)
        print("pes: ", pes_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_xxx_read_xxx(self):
        file1 = "file.xxx"
        write_xxx(get_big_pattern(), file1)
        pattern = read_xxx(file1)
        self.assertEqual(len(pattern.threadlist), pattern.count_stitch_commands(COLOR_CHANGE) + 1)
        self.assertEqual(pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(pattern)
        self.assertEqual(pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(pattern.stitches, 0, -1)
        print("xxx: ", pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_u01_read_u01(self):
        file1 = "file.u01"
        write_u01(get_big_pattern(), file1)
        u01_pattern = read_u01(file1)
        self.assertEqual(len(u01_pattern.threadlist), 0)
        self.assertEqual(u01_pattern.count_stitch_commands(NEEDLE_SET), 16)
        self.assertIsNotNone(u01_pattern)
        self.assertEqual(u01_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(u01_pattern.stitches, 0, -1)
        print("u01: ", u01_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_csv_read_csv(self):
        file1 = "file.csv"
        write_csv(get_big_pattern(), file1, {"encode": True})
        csv_pattern = read_csv(file1)
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(len(csv_pattern.threadlist), csv_pattern.count_stitch_commands(COLOR_CHANGE) + 1)
        self.assertEqual(csv_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_gcode_read_gcode(self):
        file1 = "file.gcode"
        write_gcode(get_big_pattern(), file1)
        gcode_pattern = read_gcode(file1)
        self.assertIsNotNone(gcode_pattern)
        thread_count = len(gcode_pattern.threadlist)
        change_count = gcode_pattern.count_stitch_commands(COLOR_CHANGE) + 1
        print(thread_count)
        print(change_count)

        self.assertEqual(thread_count, change_count)
        self.assertEqual(gcode_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(gcode_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(gcode_pattern.stitches, 0, -1)
        self.addCleanup(os.remove, file1)

    def test_write_txt(self):
        file1 = "file.txt"
        write_txt(get_big_pattern(), file1)
        write_txt(get_big_pattern(), file1, {"mimic": True})
        self.addCleanup(os.remove, file1)

    def test_write_pes_mismatched(self):
        file1 = "file.pes"
        pattern = EmbPattern()
        pattern += "red"
        pattern += "red"
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += COLOR_CHANGE
        pattern += (100, 0), (0, 100)
        pattern += COLOR_CHANGE
        pattern += (0, 0), (100, 100)
        pattern += COLOR_CHANGE
        pattern += (100, 0), (0, 100)
        write_pes(pattern, file1, {"version": "6t"})
        write_pes(pattern, file1)
        self.addCleanup(os.remove, file1)

    def test_pes_writes_stop(self):
        """Test if pes can read/write a stop command."""
        file1 = "file.pes"
        pattern = EmbPattern()
        pattern += "red"
        pattern += (0, 0), (100, 100)
        pattern += STOP
        pattern += (100, 0), (0, 100)
        pattern += "blue"
        pattern += (0, 0), (100, 100)
        pattern += STOP
        pattern += (100, 0), (0, 100)
        write_pes(pattern, file1, {"version": "6t"})
        loaded = read_pes(file1)
        self.assertEqual(pattern.count_stitch_commands(STOP), 2)
        self.assertEqual(pattern.count_stitch_commands(COLOR_CHANGE), 1)
        self.assertEqual(pattern.count_threads(), 2)
        self.assertEqual(loaded.count_stitch_commands(STOP), 2)
        self.assertEqual(loaded.count_stitch_commands(COLOR_CHANGE), 1)
        self.assertEqual(loaded.count_threads(), 2)
        self.addCleanup(os.remove, file1)

