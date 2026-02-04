import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_returns_empty_string_when_props_is_none(self):
        node = HTMLNode()
        expected = ""
        actual = node.props_to_html()

        self.assertEqual(expected, actual)

    def test_props_to_html_is_formatted_correctly(self):
        test_props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(tag="a", value="This is a link", props=test_props)
        expected = ' href="https://www.google.com" target="_blank"'
        actual = node.props_to_html()

        self.assertEqual(expected, actual)

    def test_props_to_html_returns_empty_string_when_props_is_empty_dict(self):
        node = HTMLNode(tag="a", value="This is a link", props={})
        expected = ""
        actual = node.props_to_html()

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
