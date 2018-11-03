from __future__ import print_function

import unittest

from pattern_for_tests import *


class TestConverts(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_convert_xxx_to_u01(self):
        file1 = "convert_u01.xxx"
        file2 = "converted_xxx.u01"
        write_xxx(get_big_pattern(), file1)
        f_pattern = read_xxx(file1)
        write_u01(f_pattern, file2)
        t_pattern = read_u01(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(NEEDLE_SET), 16)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("xxx->u01: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_xxx_to_csv(self):
        file1 = "convert_csv.xxx"
        file2 = "converted_xxx.csv"
        write_xxx(get_big_pattern(), file1)
        f_pattern = read_xxx(file1)
        write_csv(f_pattern, file2)
        t_pattern = read_csv(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("xxx->csv: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_xxx_to_exp(self):
        file1 = "convert_exp.xxx"
        file2 = "converted_xxx.exp"
        write_xxx(get_big_pattern(), file1)
        f_pattern = read_xxx(file1)
        write_exp(f_pattern, file2)
        t_pattern = read_exp(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("xxx->exp: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_xxx_to_vp3(self):
        file1 = "convert_vp3.xxx"
        file2 = "converted_xxx.vp3"
        write_xxx(get_big_pattern(), file1)
        f_pattern = read_xxx(file1)
        write_vp3(f_pattern, file2)
        t_pattern = read_vp3(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("xxx->vp3: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_xxx_to_jef(self):
        file1 = "convert_jef.xxx"
        file2 = "converted_xxx.jef"
        write_xxx(get_big_pattern(), file1)
        f_pattern = read_xxx(file1)
        write_jef(f_pattern, file2)
        t_pattern = read_jef(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("xxx->jef: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_xxx_to_pec(self):
        file1 = "convert_pec.xxx"
        file2 = "converted_xxx.pec"
        write_xxx(get_big_pattern(), file1)
        f_pattern = read_xxx(file1)
        write_pec(f_pattern, file2)
        t_pattern = read_pec(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("xxx->pec: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_xxx_to_xxx(self):
        file1 = "convert_xxx.xxx"
        file2 = "converted_xxx.xxx"
        write_xxx(get_big_pattern(), file1)
        f_pattern = read_xxx(file1)
        write_xxx(f_pattern, file2)
        t_pattern = read_xxx(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("xxx->xxx: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_xxx_to_dst(self):
        file1 = "convert_dst.xxx"
        file2 = "converted_xxx.dst"
        write_xxx(get_big_pattern(), file1)
        f_pattern = read_xxx(file1)
        write_dst(f_pattern, file2)
        t_pattern = read_dst(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("xxx->dst: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_xxx_to_gcode(self):
        file1 = "convert_gcode.xxx"
        file2 = "converted_xxx.gcode"
        write_xxx(get_big_pattern(), file1)
        f_pattern = read_xxx(file1)
        write_gcode(f_pattern, file2)
        t_pattern = read_gcode(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("xxx->gcode: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_xxx_to_pes(self):
        file1 = "convert_pes.xxx"
        file2 = "converted_xxx.pes"
        write_xxx(get_big_pattern(), file1)
        f_pattern = read_xxx(file1)
        write_pes(f_pattern, file2)
        t_pattern = read_pes(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("xxx->pes: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)
