from __future__ import print_function

import unittest
from pyembroidery import *


class TestEmbpattern(unittest.TestCase):

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_write(self):
        pattern = EmbPattern()
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "red")
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "blue")
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "green")

        write_dst(pattern, "file.dst")
        dst_pattern = read_dst("file.dst")
        self.assertIsNotNone(dst_pattern)
        self.assertEqual(dst_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(dst_pattern.stitches, 0, -1)
        print("dst: ", dst_pattern.stitches)

        write_exp(pattern, "file.exp")
        exp_pattern = read_exp("file.exp")
        self.assertIsNotNone(exp_pattern)
        self.assertEqual(exp_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(exp_pattern.stitches, 0, -1)
        print("exp: ", exp_pattern.stitches)

        write_vp3(pattern, "file.vp3")
        vp3_pattern = read_vp3("file.vp3")
        self.assertIsNotNone(vp3_pattern)
        self.assertEqual(vp3_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(vp3_pattern.stitches, 0, -1)
        print("vp3: ", vp3_pattern.stitches)

        write_jef(pattern, "file.jef")
        jef_pattern = read_jef("file.jef")
        self.assertIsNotNone(jef_pattern)
        self.assertEqual(jef_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(jef_pattern.stitches, 0, -1)
        print("jef: ", jef_pattern.stitches)

        write_pec(pattern, "file.pec")
        pec_pattern = read_pec("file.pec")
        self.assertIsNotNone(pec_pattern)
        self.assertEqual(pec_pattern.count_stitch_commands(STITCH), 16)  # 5
        self.position_equals(pec_pattern.stitches, 0, -1)
        print("pec: ", pec_pattern.stitches)

        write_pes(pattern, "file.pes")
        pes_pattern = read_pes("file.pes")
        self.assertIsNotNone(pes_pattern)
        self.assertEqual(pes_pattern.count_stitch_commands(STITCH), 16)  # 5
        self.position_equals(pes_pattern.stitches, 0, -1)
        print("pes: ", pes_pattern.stitches)

        write_u01(pattern, "file.u01")
        u01_pattern = read_u01("file.u01")
        self.assertIsNotNone(u01_pattern)
        self.assertEqual(u01_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(u01_pattern.stitches, 0, -1)
        print("u01: ", u01_pattern.stitches)

        write_csv(pattern, "file.csv")
        csv_pattern = read_csv("file.csv")
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 15)
        self.position_equals(csv_pattern.stitches, 0, -1)
        print("csv: ", csv_pattern.stitches)

    def test_matrix(self):
        matrix = EmbMatrix()
        matrix.post_rotate(90, 100, 100)
        p = matrix.point_in_matrix_space(50, 50)
        self.assertAlmostEqual(p[0], 150)
        self.assertAlmostEqual(p[1], 50)

        matrix.reset()
        matrix.post_scale(2, 2, 50, 50)
        p = matrix.point_in_matrix_space(50, 50)
        self.assertAlmostEqual(p[0], 50)
        self.assertAlmostEqual(p[1], 50)

        p = matrix.point_in_matrix_space(25, 25)
        self.assertAlmostEqual(p[0], 0)
        self.assertAlmostEqual(p[1], 0)
        matrix.post_rotate(45, 50, 50)

        p = matrix.point_in_matrix_space(25, 25)
        self.assertAlmostEqual(p[0], 50)

        matrix.reset()
        matrix.post_scale(0.5, 0.5)
        p = matrix.point_in_matrix_space(100, 100)
        self.assertAlmostEqual(p[0], 50)
        self.assertAlmostEqual(p[1], 50)
        matrix.reset()
        matrix.post_scale(2, 2, 100, 100)
        p = matrix.point_in_matrix_space(50, 50)
        self.assertAlmostEqual(p[0], 0)
        self.assertAlmostEqual(p[1], 0)

    def test_matrix_commands(self):
        pattern = EmbPattern()
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "red")
        pattern.add_command(MATRIX_ROTATE, 45)
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "blue")
        pattern.add_command(MATRIX_ROTATE, 45)
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "aqua")
        pattern = pattern.get_normalized_pattern()
        print("rotate:", pattern.stitches)
        self.assertAlmostEqual(pattern.stitches[4][0], pattern.stitches[6][0])
        self.assertAlmostEqual(pattern.stitches[4][1], pattern.stitches[6][1])
        self.assertAlmostEqual(pattern.stitches[10][0], pattern.stitches[12][0])
        self.assertAlmostEqual(pattern.stitches[10][1], pattern.stitches[12][1])
        self.assertAlmostEqual(pattern.stitches[4][0], pattern.stitches[12][0])
        self.assertAlmostEqual(pattern.stitches[4][1], pattern.stitches[12][1])

        write_svg(pattern, "file.svg")

        pattern = EmbPattern()
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "red")
        pattern.add_command(MATRIX_TRANSLATE, 20, 40)
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "blue")
        pattern.add_command(MATRIX_TRANSLATE, -20, -40)
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "aqua")
        pattern = pattern.get_normalized_pattern()
        print("translate:", pattern.stitches)
        self.assertIsNotNone(pattern.stitches)
        self.assertEqual(pattern.count_stitch_commands(MATRIX_TRANSLATE), 0)

        self.assertAlmostEqual(pattern.stitches[4][0], pattern.stitches[12][0])
        self.assertAlmostEqual(pattern.stitches[4][1], pattern.stitches[12][1])
        write_svg(pattern, "file2.svg")

        pattern = EmbPattern()
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "red")
        pattern.add_command(MATRIX_TRANSLATE, 20, 40)
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "blue")
        pattern.add_command(MATRIX_ROTATE, -90)
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "aqua")
        pattern = pattern.get_normalized_pattern()
        print("transrot:", pattern.stitches)
        self.assertIsNotNone(pattern.stitches)
        self.assertEqual(pattern.count_stitch_commands(MATRIX_TRANSLATE), 0)
        self.assertEqual(pattern.count_stitch_commands(MATRIX_ROTATE), 0)
        # self.assertAlmostEqual(pattern.stitches[12][0], pattern.stitches[6][0])
        # self.assertAlmostEqual(pattern.stitches[12][1], pattern.stitches[6][1])
        write_svg(pattern, "file3.svg")

        pattern = EmbPattern()
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "red")
        pattern.add_command(MATRIX_TRANSLATE, 20, 40)
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "blue")
        pattern.add_command(MATRIX_SCALE, 2, 2)
        pattern.add_block([(10, 10), (10, 110), (110, 110), (110, 10), (10, 10)], "aqua")
        pattern = pattern.get_normalized_pattern()
        print("transcale:", pattern.stitches)
        self.assertIsNotNone(pattern.stitches)
        self.assertEqual(pattern.count_stitch_commands(MATRIX_TRANSLATE), 0)
        self.assertEqual(pattern.count_stitch_commands(MATRIX_SCALE), 0)
        # self.assertAlmostEqual(pattern.stitches[12][0], pattern.stitches[6][0])
        # self.assertAlmostEqual(pattern.stitches[12][1], pattern.stitches[6][1])
        write_svg(pattern, "file4.svg")
