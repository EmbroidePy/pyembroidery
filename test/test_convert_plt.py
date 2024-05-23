from __future__ import print_function

import unittest

from test.pattern_for_tests import *


class TestConverts(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_convert_plt_to_u01(self):
        file1 = "convert_u01.plt"
        file2 = "converted_plt.u01"
        get_big_pattern().write(file1)
        f_pattern = EmbPattern(file1)
        f_pattern.write(file2)
        t_pattern = EmbPattern(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 16)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("plt->u01: ", t_pattern.stitches)
        # self.addCleanup(os.remove, file1)
        # self.addCleanup(os.remove, file2)

    def test_convert_plt_to_csv(self):
        file1 = "convert_csv.plt"
        file2 = "converted_plt.csv"
        get_big_pattern().write(file1)
        f_pattern = EmbPattern(file1)
        f_pattern.write(file2)
        t_pattern = EmbPattern(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("plt->csv: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_plt_to_exp(self):
        file1 = "convert_exp.plt"
        file2 = "converted_plt.exp"
        get_big_pattern().write(file1)
        f_pattern = EmbPattern(file1)
        f_pattern.write(file2)
        t_pattern = EmbPattern(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("plt->exp: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_plt_to_pes(self):
        file1 = "convert_pes.plt"
        file2 = "converted_plt.pes"
        get_big_pattern().write(file1)
        f_pattern = EmbPattern(file1)
        f_pattern.write(file2)
        t_pattern = EmbPattern(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("plt->pes: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_plt_to_jef(self):
        file1 = "convert_jef.plt"
        file2 = "converted_plt.jef"
        get_big_pattern().write(file1)
        f_pattern = EmbPattern(file1)
        f_pattern.write(file2)
        t_pattern = EmbPattern(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("plt->jef: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_plt_to_pec(self):
        file1 = "convert_pec.plt"
        file2 = "converted_plt.pec"
        get_big_pattern().write(file1)
        f_pattern = EmbPattern(file1)
        f_pattern.write(file2)
        t_pattern = EmbPattern(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("plt->pec: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_plt_to_vp3(self):
        file1 = "convert_vp3.plt"
        file2 = "converted_plt.vp3"
        get_big_pattern().write(file1)
        f_pattern = EmbPattern(file1)
        f_pattern.write(file2)
        t_pattern = EmbPattern(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("plt->vp3: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_plt_to_dst(self):
        file1 = "convert_dst.plt"
        file2 = "converted_plt.dst"
        get_big_pattern().write(file1)
        f_pattern = EmbPattern(file1)
        f_pattern.write(file2)
        t_pattern = EmbPattern(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("plt->dst: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_plt_to_gcode(self):
        file1 = "convert_gcode.plt"
        file2 = "converted_plt.gcode"
        get_big_pattern().write(file1)
        f_pattern = EmbPattern(file1)
        f_pattern.write(file2)
        t_pattern = EmbPattern(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("plt->gcode: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)
        
    def test_convert_plt_to_xxx(self):
        file1 = "convert_xxx.plt"
        file2 = "converted_plt.xxx"
        get_big_pattern().write(file1)
        f_pattern = EmbPattern(file1)
        f_pattern.write(file2)
        t_pattern = EmbPattern(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("plt->xxx: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_convert_plt_to_tbf(self):
        file1 = "convert_tbf.plt"
        file2 = "converted_plt.tbf"
        get_big_pattern().write(file1)
        f_pattern = EmbPattern(file1)
        f_pattern.write(file2)
        t_pattern = EmbPattern(file2)

        self.assertIsNotNone(t_pattern)
        self.assertEqual(t_pattern.count_stitch_commands(NEEDLE_SET), 16)
        self.assertEqual(t_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.position_equals(t_pattern.stitches, 0, -1)
        print("plt->tbf: ", t_pattern.stitches)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_plt_stop_write_large(self):
        file = "stop2.plt"
        pattern = get_shift_stop_pattern()
        n_pattern = pattern.get_normalized_pattern()
        self.assertEqual(n_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(n_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.assertEqual(n_pattern.count_stitch_commands(STOP), 5)

        pattern.write(file)
        f_pattern = EmbPattern(file)

        self.assertIsNotNone(f_pattern)

        with open(file, "rb") as f:
            f.seek(0x18)
            colors = f.read(1)
            self.assertEqual(ord(colors), f_pattern.count_color_changes() + f_pattern.count_stitch_commands(STOP) + 1)

        self.assertEqual(f_pattern.count_stitch_commands(COLOR_CHANGE), 15)
        self.assertEqual(f_pattern.count_stitch_commands(STITCH), 16 * 5)
        self.assertEqual(f_pattern.count_stitch_commands(STOP), 5)
        self.addCleanup(os.remove, file)