import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_with_header(self):
        md = "# Hello"
        extracted = extract_title(md)

        self.assertEqual("Hello", extracted)

    def test_with_multiline(self):
        md = """
hello
sjdlkajfklhdsjav sahfiue hzwaoivhkj dsbaeuhf dvsa
akjhueior


sdahjklvejawfs
# This is a title
"""

        extracted = extract_title(md)

        self.assertEqual(extracted, "This is a title")

    def test_without(self):
        md = "random text aber ohne header"

        with self.assertRaises(Exception):
            extract_title(md)
