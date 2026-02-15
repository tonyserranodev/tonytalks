import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, Props


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_returns_empty_string_when_props_is_none(self):
        node = HTMLNode()
        expected = ""
        actual = node.props_to_html()

        self.assertEqual(expected, actual)

    def test_props_to_html_is_formatted_correctly(self):
        test_props: Props = {"href": "https://www.google.com", "target": "_blank"}
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
        test_props: dict[str, str | None] = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
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
        test_props: Props = {"href": "https://www.google.com", "target": "_blank"}
        node = LeafNode(tag="a", value="this is a link", props=test_props)
        expected = "LeafNode(tag: a\nvalue: this is a link\nprops: {'href': 'https://www.google.com', 'target': '_blank'})"
        actual = node.__repr__()

        self.assertEqual(expected, actual)

    def test_tag_has_no_value(self):
        node = LeafNode(value="this is some raw text", tag="")
        expected = "<>this is some raw text</>"
        actual = node.to_html()

        self.assertEqual(expected, actual)


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_with_many_parent_nodes(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node1 = ParentNode("p", [grandchild_node])
        child_node2 = ParentNode("span", [child_node1])
        parent_node = ParentNode("div", [child_node2])

        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p><b>grandchild</b></p></span></div>",
        )

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("b", "child")
        parent_node = ParentNode(None, [child_node])  # pyright: ignore[reportArgumentType]

        with self.assertRaises(ValueError) as context:
            _ = parent_node.to_html()

        self.assertEqual(str(context.exception), "All parent nodes must have a tag")

    def test_to_html_with_props(self):
        grandchild_node = LeafNode("i", "grandchild")
        child_node1 = ParentNode(
            "a",
            [grandchild_node],
            {"href": "https://www.google.com", "target": "_blank"},
        )
        child_node2 = ParentNode("span", [child_node1])
        parent_node = ParentNode("div", [child_node2])

        self.assertEqual(
            parent_node.to_html(),
            '<div><span><a href="https://www.google.com" target="_blank"><i>grandchild</i></a></span></div>',
        )


if __name__ == "__main__":
    unittest.main()  # pyright: ignore[reportUnusedCallResult]
