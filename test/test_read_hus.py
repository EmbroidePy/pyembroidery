from __future__ import print_function

import random
import unittest

from pyembroidery import *


class TestReadHus(unittest.TestCase):

    def test_fake_compression(self):
        for i in range(10):
            s = random.randint(10, 1000)  # May fail if larger.
            test_bytes = bytearray(random.getrandbits(8) for _ in range(s))
            compressed_bytes = EmbCompress.compress(test_bytes)
            uncompressed = bytearray(EmbCompress.expand(compressed_bytes, len(test_bytes)))
            self.assertEqual(test_bytes, uncompressed)
