from __future__ import print_function

import unittest

from pattern_for_tests import *
from pyembroidery import GenericWriter


class TestConverts(unittest.TestCase):
    def position_equals(self, stitches, j, k):
        self.assertEqual(stitches[j][:1], stitches[k][:1])

    def test_generic_write_stitch(self):
        file1 = "convert.dst"
        file2 = "convert.txt"
        pattern = get_fractal_pattern()
        pattern.write(file1)

        pattern = EmbPattern(file1)

        EmbPattern.write_embroidery(
            GenericWriter,
            pattern,
            file2,
            {
                "segment_start": "\t\t",
                "segment_end": "\n",
                "segment": "{cmd_str} {x},{y}",
                "stitch": "Stitch: {x},{y}",
                "jump": "Jump {x},{y}",
                "trim": "Trim: {x},{y}",
                "color_change": "Color-Change: {x},{y}",
                "block_start": "\t{{\n",
                "block_end": "\t}}\n",
                "color_start": "[\n",
                "color_end": "]\n",
            },
        )

        print("write generic: ", file1)
        # self.addCleanup(os.remove, file1)
