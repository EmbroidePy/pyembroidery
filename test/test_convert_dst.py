from __future__ import print_function

import unittest
from pyembroidery import *
from pattern_for_tests import *


class TestConverts(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_convert_dst_to_u01(self):
        file1 = "convert_u01.dst"
        file2 = "converted_dst.u01"
        write_dst(get_big_pattern(), file1)
        f_pattern = read_dst(file1)
        write_u01(f_pattern, file2)
        t_pattern = read_u01(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(NEEDLE_SET), 16)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("dst->u01: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_dst_to_csv(self):
        file1 = "convert_csv.dst"
        file2 = "converted_dst.csv"
        write_dst(get_big_pattern(), file1)
        f_pattern = read_dst(file1)
        write_csv(f_pattern, file2)
        t_pattern = read_csv(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("dst->csv: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_dst_to_exp(self):
        file1 = "convert_exp.dst"
        file2 = "converted_dst.exp"
        write_dst(get_big_pattern(), file1)
        f_pattern = read_dst(file1)
        write_exp(f_pattern, file2)
        t_pattern = read_exp(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("dst->exp: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_dst_to_pes(self):
        file1 = "convert_pes.dst"
        file2 = "converted_dst.pes"
        write_dst(get_big_pattern(), file1)
        f_pattern = read_dst(file1)
        write_pes(f_pattern, file2)
        t_pattern = read_pes(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("dst->pes: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_dst_to_jef(self):
        file1 = "convert_jef.dst"
        file2 = "converted_dst.jef"
        write_dst(get_big_pattern(), file1)
        f_pattern = read_dst(file1)
        write_jef(f_pattern, file2)
        t_pattern = read_jef(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("dst->jef: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_dst_to_pec(self):
        file1 = "convert_pec.dst"
        file2 = "converted_dst.pec"
        write_dst(get_big_pattern(), file1)
        f_pattern = read_dst(file1)
        write_pec(f_pattern, file2)
        t_pattern = read_pec(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("dst->pec: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_dst_to_vp3(self):
        file1 = "convert_vp3.dst"
        file2 = "converted_dst.vp3"
        write_dst(get_big_pattern(), file1)
        f_pattern = read_dst(file1)
        write_vp3(f_pattern, file2)
        t_pattern = read_vp3(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("dst->vp3: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_dst_to_dst(self):
        file1 = "convert_dst.dst"
        file2 = "converted_dst.dst"
        write_dst(get_big_pattern(), file1)
        f_pattern = read_dst(file1)
        write_dst(f_pattern, file2)
        t_pattern = read_dst(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("dst->dst: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_dst_to_gcode(self):
        file1 = "convert_gcode.dst"
        file2 = "converted_dst.gcode"
        write_dst(get_big_pattern(), file1)
        f_pattern = read_dst(file1)
        write_gcode(f_pattern, file2)
        t_pattern = read_gcode(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("dst->gcode: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)
        
    def test_convert_dst_to_xxx(self):
        file1 = "convert_xxx.dst"
        file2 = "converted_dst.xxx"
        write_dst(get_big_pattern(), file1)
        f_pattern = read_dst(file1)
        write_xxx(f_pattern, file2)
        t_pattern = read_xxx(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("dst->xxx: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)