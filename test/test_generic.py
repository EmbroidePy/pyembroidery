from __future__ import print_function

import unittest

from test.pattern_for_tests import *
from pyembroidery import GenericWriter


class TestConverts(unittest.TestCase):
    def test_generic_write_stitch(self):
        file1 = "convert.dst"
        file2 = "convert.txt"
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)
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

    def test_generic_write_gcode(self):
        gcode_writer_dict = {
            "scale": (-0.1, -0.1),
            "pattern_start": "(STITCH_COUNT: {stitch_total})\n"
            "(THREAD_COUNT: {color_change_count})\n"
            "(EXTENTS_LEFT: {extents_left:.3f})\n"
            "(EXTENTS_TOP: {extends_top:.3f})\n"
            "(EXTENTS_RIGHT: {extends_right:.3f})\n"
            "(EXTENTS_BOTTOM: {extends_bottom:.3f})\n"
            "(EXTENTS_WIDTH: {extends_width:.3f})\n"
            "(EXTENTS_HEIGHT: {extends_height:.3f})\n"
            "(COMMAND_STITCH: {stitch_count})\n"
            "(COMMAND_COLOR_CHANGE: {color_change_count})\n"
            "(COMMAND_TRIM: {trim_count})\n"
            "(COMMAND_STOP: {stop_count})\n"
            "(COMMAND_END: {end_count})\n",
            "metadata_entry": "({metadata_key}: {metadata_value})\n",
            "thread_entry": "(Thread{thread_index}: {thread_color} {thread_description} {thread_brand} {thread_catalog_number})\n",
            "stitch": "G00 X{x:.3f} Y{y:.3f}\nG00 Z{z:.1f}\n",
            "color_change": "M00\n",
            "stop": "M00\n",
            "end": "M30\n",
        }
        file1 = "file-gcode.gcode"
        file2 = "file-generic.gcode"
        pattern = get_fractal_pattern()
        pattern.fix_color_count()
        EmbPattern.write_embroidery(
            GenericWriter,
            pattern,
            file2,
            gcode_writer_dict,
        )
        pattern.write(file1)
        f1 = open(file1, "rb").read()
        f2 = open(file2, "rb").read()
        self.assertEqual(f1, f2)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)
