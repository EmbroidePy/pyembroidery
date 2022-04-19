from __future__ import print_function

import unittest
from test.pattern_for_tests import *


class TestDataCatalog(unittest.TestCase):

    def test_catalog_files(self):
        for f in EmbPattern.supported_formats():
            self.assertIn("extensions", f)
            self.assertIn("extension", f)
            self.assertIn("description", f)
            self.assertIn("category", f)
