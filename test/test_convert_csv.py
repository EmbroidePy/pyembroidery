from __future__ import print_function

import unittest

from pattern_for_tests import *


class TestConverts(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_convert_csv_to_u01(self):
        file1 = "convert_u01.csv"
        file2 = "converted_csv.u01"
        write_csv(get_big_pattern(), file1)
        f_pattern = read_csv(file1)
        write_u01(f_pattern, file2)
        t_pattern = read_u01(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(NEEDLE_SET), 16)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("csv->u01: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_csv_to_csv(self):
        file1 = "convert_csv.csv"
        file2 = "converted_csv.csv"
        write_csv(get_big_pattern(), file1, {"encode": True})
        f_pattern = read_csv(file1)
        write_csv(f_pattern, file2)
        t_pattern = read_csv(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("csv->csv: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_csv_to_exp(self):
        file1 = "convert_exp.csv"
        file2 = "converted_csv.exp"
        write_csv(get_big_pattern(), file1)
        f_pattern = read_csv(file1)
        write_exp(f_pattern, file2)
        t_pattern = read_exp(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("csv->exp: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_csv_to_pes(self):
        file1 = "convert_pes.csv"
        file2 = "converted_csv.pes"
        write_csv(get_big_pattern(), file1)
        f_pattern = read_csv(file1)
        write_pes(f_pattern, file2)
        t_pattern = read_pes(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("csv->pes: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_csv_to_jef(self):
        file1 = "convert_jef.csv"
        file2 = "converted_csv.jef"
        write_csv(get_big_pattern(), file1)
        f_pattern = read_csv(file1)
        write_jef(f_pattern, file2)
        t_pattern = read_jef(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("csv->jef: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_csv_to_pec(self):
        file1 = "convert_pec.csv"
        file2 = "converted_csv.pec"
        write_csv(get_big_pattern(), file1)
        f_pattern = read_csv(file1)
        write_pec(f_pattern, file2)
        t_pattern = read_pec(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("csv->pec: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_csv_to_vp3(self):
        file1 = "convert_vp3.csv"
        file2 = "converted_csv.vp3"
        write_csv(get_big_pattern(), file1)
        f_pattern = read_csv(file1)
        write_vp3(f_pattern, file2)
        t_pattern = read_vp3(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("csv->vp3: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_csv_to_dst(self):
        file1 = "convert_dst.csv"
        file2 = "converted_csv.dst"
        write_csv(get_big_pattern(), file1)
        f_pattern = read_csv(file1)
        write_dst(f_pattern, file2)
        t_pattern = read_dst(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("csv->dst: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_csv_to_gcode(self):
        file1 = "convert_gcode.csv"
        file2 = "converted_csv.gcode"
        write_csv(get_big_pattern(), file1)
        f_pattern = read_csv(file1)
        write_gcode(f_pattern, file2)
        t_pattern = read_gcode(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("csv->gcode: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_csv_to_xxx(self):
        file1 = "convert_xxx.csv"
        file2 = "converted_csv.xxx"
        write_csv(get_big_pattern(), file1)
        f_pattern = read_csv(file1)
        write_xxx(f_pattern, file2)
        t_pattern = read_xxx(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("csv->xxx: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)