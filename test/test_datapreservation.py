from __future__ import print_function

import unittest
from pattern_for_tests import *


class TestDataPreservation(unittest.TestCase):

    def test_preserve_u01_needles(self):
        file1 = "file.u01"
        pattern = get_big_pattern()
        pattern.add_command(encode_thread_change(SET_CHANGE_SEQUENCE, None, 6, 0))
        write_u01(pattern, file1)
        read_pattern = read_u01(file1)
        for cmd in read_pattern.get_match_commands(NEEDLE_SET):
            print(decode_embroidery_command(cmd[2]))
        self.addCleanup(os.remove, file1)
