from __future__ import print_function

import unittest
from pyembroidery import *


class TestEmbpattern(unittest.TestCase):

    def test_write(self):
        pattern = EmbPattern()
        pattern.stitch_abs(0, 0)
        pattern.stitch_abs(0, 100)
        pattern.add_command(MATRIX_ROTATE, 30)
        pattern.stitch_abs(100, 100)
        pattern.stitch_abs(100, 0)
        pattern.stitch_abs(0, 0)
        stitches = pattern.stitches
        assert (stitches[-1][0] == 0)
        assert (stitches[-1][1] == 0)

        write_dst(pattern, "file.dst")
        dst_pattern = read_dst("file.dst")
        self.assertIsNotNone(dst_pattern)
        self.assertEqual(dst_pattern.count_stitch_commands(STITCH), 5)
        self.assertNotEqual(dst_pattern.stitches[-1][0], 0)
        self.assertNotEqual(dst_pattern.stitches[-1][1], 0)
        print("dst: ", dst_pattern.stitches)

        write_exp(pattern, "file.exp")
        exp_pattern = read_exp("file.exp")
        self.assertIsNotNone(exp_pattern)
        self.assertEqual(exp_pattern.count_stitch_commands(STITCH), 5)
        self.assertNotEqual(exp_pattern.stitches[-1][0], 0)
        self.assertNotEqual(exp_pattern.stitches[-1][1], 0)
        print("exp: ", exp_pattern.stitches)

        write_vp3(pattern, "file.vp3")
        vp3_pattern = read_vp3("file.vp3")
        self.assertIsNotNone(vp3_pattern)
        self.assertEqual(vp3_pattern.count_stitch_commands(STITCH), 5)
        self.assertNotEqual(vp3_pattern.stitches[-1][0], 0)
        self.assertNotEqual(vp3_pattern.stitches[-1][1], 0)
        print("vp3: ", vp3_pattern.stitches)

        write_jef(pattern, "file.jef")
        jef_pattern = read_jef("file.jef")
        self.assertIsNotNone(jef_pattern)
        self.assertEqual(jef_pattern.count_stitch_commands(STITCH), 5)
        self.assertNotEqual(jef_pattern.stitches[-1][0], 0)
        self.assertNotEqual(jef_pattern.stitches[-1][1], 0)
        print("jef: ", jef_pattern.stitches)

        write_pec(pattern, "file.pec")
        pec_pattern = read_pec("file.pec")
        self.assertIsNotNone(pec_pattern)
        self.assertEqual(pec_pattern.count_stitch_commands(STITCH), 6)
        self.assertNotEqual(pec_pattern.stitches[-1][0], 0)
        self.assertNotEqual(pec_pattern.stitches[-1][1], 0)
        print("pec: ", pec_pattern.stitches)

        write_pes(pattern, "file.pes")
        pes_pattern = read_pes("file.pes")
        self.assertIsNotNone(pes_pattern)
        self.assertEqual(pes_pattern.count_stitch_commands(STITCH), 6)
        self.assertNotEqual(pes_pattern.stitches[-1][0], 0)
        self.assertNotEqual(pes_pattern.stitches[-1][1], 0)
        print("pes: ", pes_pattern.stitches)

        write_u01(pattern, "file.u01")
        u01_pattern = read_u01("file.u01")
        self.assertIsNotNone(u01_pattern)
        self.assertEqual(u01_pattern.count_stitch_commands(STITCH), 5)
        self.assertNotEqual(u01_pattern.stitches[-1][0], 0)
        self.assertNotEqual(u01_pattern.stitches[-1][1], 0)
        print("u01: ", u01_pattern.stitches)

        write_csv(pattern, "file.csv")
        csv_pattern = read_csv("file.csv")
        self.assertIsNotNone(csv_pattern)
        self.assertEqual(csv_pattern.count_stitch_commands(STITCH), 5)
        self.assertNotEqual(csv_pattern.stitches[-1][0], 0)
        self.assertNotEqual(csv_pattern.stitches[-1][1], 0)
        print("csv: ", csv_pattern.stitches)

    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][0], stitches[k][0])
        self.assertEqual(stitches[j][1], stitches[k][1])

    def test_matrix(self):
        pattern = EmbPattern()
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "red")
        pattern.add_command(MATRIX_ROTATE, 45)
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "blue")
        pattern.add_command(MATRIX_ROTATE, 45)
        pattern.add_block([(0, 0), (0, 100), (100, 100), (100, 0), (0, 0)], "aqua")
        pattern = pattern.get_normalized_pattern()
        self.position_equals(pattern.stitches, 5, 6)
        self.position_equals(pattern.stitches, 10, 11)
        print(pattern.stitches)
        write_svg(pattern, "file.svg")

        self.assertIsNotNone(pattern.stitches)
