import unittest

from generate_html import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_no_heading_raises_exception(self):
        md = "Yo Yo Yo guys"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_returns_title(self):
        md = "# A Guide to Winning"
        self.assertEqual(extract_title(md), "A Guide to Winning")

    def test_extract_title_strips_extra_whitespace(self):
        md = "  # A Guide to Winning  "
        self.assertEqual(extract_title(md), "A Guide to Winning")

    def test_extract_title_with_many_lines_of_markdown(self):
        md = """
# This is a heading to be extracted as a title
This is some extra text in the file
and some even more text
        """
        self.assertEqual(
            extract_title(md), "This is a heading to be extracted as a title"
        )
