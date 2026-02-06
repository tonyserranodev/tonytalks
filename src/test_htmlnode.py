import unittest

from htmlnode import HTMLNode, LeafNode


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

    def test_repr(self):
        test_props = {"href": "https://www.google.com", "target": "_blank"}
        node = HTMLNode(tag="a", value="This is a link", props=test_props)
        expected = "HTMLNode(tag: a\nvalue: This is a link\nchildren: None\nprops: {'href': 'https://www.google.com', 'target': '_blank'})"
        actual = node.__repr__()

        self.assertEqual(expected, actual)

    class TestLeafNode(unittest.TestCase):
        def test_repr_no_props(self):
            node = LeafNode(tag="p", value="this is some text")
            expected = "LeafNode(tag: p\nvalue: this is some text\nprops: None)"
            actual = node.__repr__()

            self.assertEqual(expected, actual)

        def test_repr_with_props(self):
            test_props = {"href": "https://www.google.com", "target": "_blank"}
            node = LeafNode(tag="a", value="this is a link", props=test_props)
            expected = "LeafNode(tag: a\nvalue: this is a link\nprops: {'href': 'https://www.google.com', 'target': '_blank'})"
            actual = node.__repr__()

            self.assertEqual(expected, actual)

        def test_tag_is_none(self):
            node = LeafNode(value="this is some raw text", tag=None)
            expected = "this is some raw text"
            actual = node.to_html()

            self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
