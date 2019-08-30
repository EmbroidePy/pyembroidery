from __future__ import print_function

import unittest

from pattern_for_tests import *


class TestJson(unittest.TestCase):

    def test_metadata_write_read_json(self):
        file1 = "metadata.json"
        pattern = EmbPattern()
        for i in range(4, 20):
            pattern.add_thread(EmbThread("random"))
        pattern.extras['name'] = "My Embroidery."
        pattern.extras['bytes'] = b'\00these are bytes'
        pattern.extras['bytes2'] = bytearray(b'this is bytearray')
        pattern.extras['value'] = 208
        write(pattern, file1)
        w_pattern = read(file1)
        self.assertEqual(w_pattern.extras['name'], "My Embroidery.")
        self.assertEqual(w_pattern.extras['value'], 208)
        self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
        for q in range(0, len(pattern.threadlist)):
            self.assertEqual(pattern.threadlist[q], w_pattern.threadlist[q])

        self.addCleanup(os.remove, file1)


    def test_colors_write_read_json(self):
        file1 = "color.json"
        for m in range(0, 50):
            pattern = EmbPattern()
            for i in range(4, 20):
                pattern.add_thread(EmbThread("random"))
            write(pattern, file1)
            w_pattern = read(file1)
            self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
            for q in range(0, len(pattern.threadlist)):
                self.assertEqual(pattern.threadlist[q], w_pattern.threadlist[q])
        self.addCleanup(os.remove, file1)

    def test_write_read_json(self):
        file1 = "test.json"
        pattern = get_shift_pattern()
        write(pattern, file1)
        w_pattern = read(file1)
        self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
        for q in range(0, len(pattern.threadlist)):
            self.assertEqual(pattern.threadlist[q], w_pattern.threadlist[q])
        for q in range(0, len(pattern.stitches)):
            self.assertEqual(pattern.stitches[q], w_pattern.stitches[q])
        self.addCleanup(os.remove, file1)
