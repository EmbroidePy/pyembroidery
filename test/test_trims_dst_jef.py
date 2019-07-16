from __future__ import print_function

import unittest

from pyembroidery import *
from pattern_for_tests import *


class TestTrims(unittest.TestCase):

    def test_dst_trims(self):
        file0 = "trim.dst"
        pattern = get_fractal_pattern()
        write_dst(pattern, file0)
        loaded_pattern = read_dst(file0)
        self.assertIsNotNone(loaded_pattern)
        self.assertNotEqual(loaded_pattern.count_stitch_commands(TRIM), 0)
        self.addCleanup(os.remove, file0)

    def test_dst_trims_fail(self):
        file0 = "trim.dst"
        pattern = get_fractal_pattern()
        write_dst(pattern, file0)
        loaded_pattern = read_dst(file0, {"trim_at": 50})  # Lines beyond 50 jumps get a trim.
        self.assertIsNotNone(loaded_pattern)
        self.assertEqual(loaded_pattern.count_stitch_commands(TRIM), 0)
        self.addCleanup(os.remove, file0)

    def test_dst_trims_success(self):
        file0 = "trim.dst"
        pattern = get_fractal_pattern()
        write_dst(pattern, file0, {"trim_at": 50})  # We make trim jumps big enough.
        loaded_pattern = read_dst(file0, {"trim_at": 50, "clipping": False})  # Lines beyond 50 jumps get a trim.
        self.assertIsNotNone(loaded_pattern)
        self.assertNotEqual(loaded_pattern.count_stitch_commands(TRIM), 0)
        self.addCleanup(os.remove, file0)

    def test_jef_trims(self):
        file0 = "trim.jef"
        pattern = get_fractal_pattern()
        write_jef(pattern, file0)
        loaded_pattern = read_jef(file0)
        self.assertIsNotNone(loaded_pattern)
        self.assertNotEqual(loaded_pattern.count_stitch_commands(TRIM), 0)
        self.addCleanup(os.remove, file0)

    def test_jef_trims_off(self):
        file0 = "trim.jef"
        pattern = get_fractal_pattern()
        write_jef(pattern, file0)
        loaded_pattern = read_jef(file0, {"trim_distance": None})
        self.assertEqual(loaded_pattern.count_stitch_commands(JUMP), 15)
        self.assertIsNotNone(loaded_pattern)
        self.assertEqual(loaded_pattern.count_stitch_commands(TRIM), 0)
        self.addCleanup(os.remove, file0)

    def test_jef_trims_commands(self):
        file0 = "trim.jef"
        pattern = get_fractal_pattern()
        write_jef(pattern, file0, {"trims": True})
        loaded_pattern = read_jef(file0, {"trim_distance": None})
        self.assertEqual(loaded_pattern.count_stitch_commands(JUMP), 15)
        self.assertEqual(loaded_pattern.count_stitch_commands(TRIM), 0)
        loaded_pattern = read_jef(file0, {"trim_distance": None, "clipping": False})
        self.assertEqual(loaded_pattern.count_stitch_commands(JUMP), 21)
        self.assertEqual(loaded_pattern.count_stitch_commands(TRIM), 0)
        loaded_pattern = read_jef(file0, {"trim_distance": None, "clipping": False, "trims": True, })
        self.assertEqual(loaded_pattern.count_stitch_commands(JUMP), 21)
        self.assertEqual(loaded_pattern.count_stitch_commands(TRIM), 2)
        loaded_pattern = read_jef(file0, {"trim_distance": None, "trims": True})
        self.assertEqual(loaded_pattern.count_stitch_commands(JUMP), 15)
        self.assertEqual(loaded_pattern.count_stitch_commands(TRIM), 2)
        self.addCleanup(os.remove, file0)
