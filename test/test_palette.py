from __future__ import print_function

import unittest

from pyembroidery import *
from pyembroidery.EmbThreadPec import *
from pyembroidery.EmbThread import build_unique_palette, build_nonrepeat_palette, build_palette


class TestPalettes(unittest.TestCase):

    def test_unique_palette(self):
        """Similar elements should not plot to the same palette index"""
        pattern = EmbPattern()
        pattern += "#FF0001"
        pattern += "Blue"
        pattern += "Blue"
        pattern += "Red"
        threadset = get_thread_set()
        palette = build_unique_palette(threadset,pattern.threadlist)
        self.assertNotEqual(palette[0],palette[3])  # Red and altered Red
        self.assertEqual(palette[1], palette[2])  # Blue and Blue

    def test_unique_palette_large(self):
        """Excessive palette entries that all map, should be mapped"""
        pattern = EmbPattern()
        for x in range(0, 100):
            pattern += "black"
        threadset = get_thread_set()
        palette = build_unique_palette(threadset, pattern.threadlist)
        self.assertEqual(palette[0], palette[1])

    def test_unique_palette_unmap(self):
        """Excessive palette entries can't all map, should map what it can and repeat"""
        pattern = EmbPattern()
        for i in range(0, 100):
            thread = EmbThread()
            thread.set_color(i, i, i)
            pattern += thread
        threadset = get_thread_set()
        palette = build_unique_palette(threadset, pattern.threadlist)
        palette.sort()

    def test_unique_palette_max(self):
        """If the entries equal the list they should all map."""
        pattern = EmbPattern()
        threadset = get_thread_set()
        for i in range(0, len(threadset)-2):
            thread = EmbThread()
            thread.set_color(i, i, i)
            pattern += thread
        palette = build_unique_palette(threadset, pattern.threadlist)
        palette.sort()
        for i in range(1,len(palette)):
            self.assertNotEqual(palette[i-1], palette[i])

    def test_nonrepeat_palette_moving(self):
        """The almost same color should not get plotted to the same palette index"""
        pattern = EmbPattern()
        pattern += "Red"
        pattern += "Blue"
        pattern += "#0100FF"
        pattern += "Red"
        threadset = get_thread_set()
        palette = build_nonrepeat_palette(threadset,pattern.threadlist)
        self.assertEqual(palette[0],palette[3]) # Red and Red
        self.assertNotEqual(palette[1], palette[2])  # Blue and altered Blue

    def test_nonrepeat_palette_stay_moved(self):
        """An almost same moved, only temporary"""
        pattern = EmbPattern()
        pattern += "Red"
        pattern += "Blue"
        pattern += "#0100FF"
        pattern += "Red"
        pattern += "#0100FF"
        threadset = get_thread_set()
        palette = build_nonrepeat_palette(threadset,pattern.threadlist)
        self.assertEqual(palette[0],palette[3]) # Red and Red
        self.assertNotEqual(palette[1], palette[2])  # Blue and altered Blue
        self.assertNotEqual(palette[2], palette[4])  # same color, but color was moved

    def test_nonrepeat_palette_same(self):
        """The same exact same color if repeated should remain"""
        pattern = EmbPattern()
        pattern += "Red"
        pattern += "Blue"
        pattern += "#0000FF"  # actual blue
        pattern += "Red"
        threadset = get_thread_set()
        palette = build_nonrepeat_palette(threadset,pattern.threadlist)
        self.assertEqual(palette[0],palette[3]) # Red and Red
        self.assertEqual(palette[1], palette[2])  # Blue and Blue

    def test_palette(self):
        """Similar colors map to the same index"""
        pattern = EmbPattern()
        pattern += "#FF0001"
        pattern += "Blue"
        pattern += "Blue"
        pattern += "Red"
        threadset = get_thread_set()
        palette = build_palette(threadset,pattern.threadlist)
        self.assertEqual(palette[0],palette[3])  # Red and altered Red
        self.assertEqual(palette[1], palette[2])  # Blue and Blue
