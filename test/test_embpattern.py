from __future__ import print_function

# External dependencies:
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
        pattern = pattern.get_normalized_pattern()
        assert (pattern is not None)
        stitches = pattern.stitches
        assert (stitches[-1][0] != 0)
        assert (stitches[-1][1] != 0)
