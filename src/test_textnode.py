import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        expected = "TextNode(This is a text node, link, https://boot.dev)"
        actual = repr(node)
        self.assertEqual(actual, expected)

    def test_nodes_with_different_text_types_are_not_equal(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_node_with_no_url_and_node_with_url_are_not_equal(self):
        node = TextNode("This is a text node", TextType.LINK, "https://boot.dev")
        node2 = TextNode(
            "This is a text node",
            TextType.LINK,
        )
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
