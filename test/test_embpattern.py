# External dependencies:
import unittest
from pyembroidery import *


class TestEmbpattern(unittest.TestCase):

    def test_write(self):
        pattern = EmbPattern()
        pattern.stitch(0, 0)
        pattern.stitch(0, 100)
        pattern.stitch(100, 100)
        pattern.stitch(100, 0)
        pattern.stitch(0, 0)
        pattern = pattern.get_normalized_pattern()
        assert (pattern is not None)
