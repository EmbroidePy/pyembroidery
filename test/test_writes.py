from __future__ import print_function

import unittest

from pyembroidery import *
from pattern_for_tests import *


class TestWrites(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_write_dst_read_dst(self):
        file1 = "file.dst"
        write_dst(get_big_pattern(), file1)
        dst_pattern = read_dst(file1)
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
        self.assertEqual(pes_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertIsNotNone(pes_pattern)
        self.assertEqual(pes_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(pes_pattern.stitches, 0, -1)
        print("pes: ", pes_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_u01_read_u01(self):
        file1 = "file.u01"
        write_u01(get_big_pattern(), file1)
        u01_pattern = read_u01(file1)
        self.assertEqual(u01_pattern.count_stitch_commands(NEEDLE_SET), 16)
        self.assertIsNotNone(u01_pattern)
        self.assertEqual(u01_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(u01_pattern.stitches, 0, -1)
        print("u01: ", u01_pattern.stitches)
        self.addCleanup(os.remove, file1)

    def test_write_csv_read_csv(self):
        file1 = "file.csv"
        write_csv(get_big_pattern(), file1)
        csv_pattern = read_csv(file1)
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(csv_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 5 * 16)
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)
        self.addCleanup(os.remove, file1)
