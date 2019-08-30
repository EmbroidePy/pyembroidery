from __future__ import print_function

import unittest

from pattern_for_tests import *


class TestColorFormats(unittest.TestCase):

    def test_write_read_col(self):
        file1 = "color.col"
        for m in range(0,50):
            pattern = EmbPattern()
            for i in range(4, 20):
                pattern.add_thread(EmbThread("random"))
            write(pattern, file1)
            w_pattern = read(file1)
            self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
            for q in range(0,len(pattern.threadlist)):
                self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)
        self.addCleanup(os.remove, file1)

    def test_write_read_edr(self):
        file1 = "color.edr"
        for m in range(0, 50):
            pattern = EmbPattern()
            for i in range(4, 20):
                pattern.add_thread(EmbThread("random"))
            write(pattern, file1)
            w_pattern = read(file1)
            self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
            for q in range(0, len(pattern.threadlist)):
                self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)
        self.addCleanup(os.remove, file1)

    def test_write_read_inf(self):
        file1 = "color.inf"
        for m in range(0, 50):
            pattern = EmbPattern()
            for i in range(4, 20):
                pattern.add_thread(EmbThread("random"))
            write(pattern, file1)
            w_pattern = read(file1)
            self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
            for q in range(0, len(pattern.threadlist)):
                self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)
        self.addCleanup(os.remove, file1)

    def test_write_edr_dst(self):
        pattern = get_shift_pattern()
        file1 = "color.edr"
        file2 = "color.dst"
        write(pattern, file1)
        write(pattern, file2)
        w_pattern = read(file1)
        w_pattern = read(file2, pattern=w_pattern)
        self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
        for q in range(0, len(pattern.threadlist)):
            self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_write_dst_edr(self):
        pattern = get_shift_pattern()
        file1 = "color.dst"
        file2 = "color.edr"
        write(pattern, file1)
        write(pattern, file2)
        w_pattern = read(file1)
        w_pattern = read(file2, pattern=w_pattern)
        self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
        for q in range(0, len(pattern.threadlist)):
            self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_write_dst_col(self):
        pattern = get_shift_pattern()
        file1 = "color.dst"
        file2 = "color.col"
        write(pattern, file1)
        write(pattern, file2)
        w_pattern = read(file1)
        w_pattern = read(file2, pattern=w_pattern)
        self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
        for q in range(0, len(pattern.threadlist)):
            self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)

    def test_write_dst_inf(self):
        pattern = get_shift_pattern()
        file1 = "color.dst"
        file2 = "color.inf"
        write(pattern, file1)
        write(pattern, file2)
        w_pattern = read(file1)
        w_pattern = read(file2, pattern=w_pattern)
        self.assertEqual(len(pattern.threadlist), len(w_pattern.threadlist))
        for q in range(0, len(pattern.threadlist)):
            self.assertEqual(pattern.threadlist[q].color, w_pattern.threadlist[q].color)
        self.addCleanup(os.remove, file1)
        self.addCleanup(os.remove, file2)