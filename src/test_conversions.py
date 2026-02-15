import unittest

from conversions import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestTextNodeToHtml(unittest.TestCase):
    def test_text_node_to_html_node_text(self):
        text = "this is some text"
        text_node = TextNode(text, TextType.TEXT)

        self.assertEqual(text_node_to_html_node(text_node).to_html(), text)

    def test_text_node_to_html_node_bold(self):
        text = "this is some bold text"
        text_node = TextNode(text, TextType.BOLD)

        self.assertEqual(text_node_to_html_node(text_node).to_html(), f"<b>{text}</b>")

    def test_text_node_to_html_node_italic(self):
        text = "this is some italicized text"
        text_node = TextNode(text, TextType.ITALIC)

        self.assertEqual(text_node_to_html_node(text_node).to_html(), f"<i>{text}</i>")

    def test_text_node_to_html_node_code(self):
        text = "this is some code"
        text_node = TextNode(text, TextType.CODE)

        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), f"<code>{text}</code>"
        )

    def test_text_node_to_html_node_link(self):
        text = "link text"
        url = "https://www.google.com"
        text_node = TextNode(text, TextType.LINK, url)

        self.assertEqual(
            text_node_to_html_node(text_node).to_html(), f'<a href="{url}">{text}</a>'
        )

    def test_text_node_to_html_node_image(self):
        text = "alt text"
        url = "https://www.image.com"
        text_node = TextNode(text, TextType.IMAGE, url)

        self.assertEqual(
            text_node_to_html_node(text_node).to_html(),
            f'<img src="{url}" alt="{text}"></img>',
        )


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_inline_bold(self):
        node = TextNode("this is some **bold** text", TextType.TEXT)
        delimiter = "**"
        text_type = TextType.BOLD

        self.assertEqual(
            split_nodes_delimiter([node], delimiter, text_type),
            [
                TextNode("this is some ", TextType.TEXT),
                TextNode("bold", text_type),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_inline_italic(self):
        node = TextNode("this is some _italic_ text", TextType.TEXT)
        delimiter = "_"
        text_type = TextType.ITALIC

        self.assertEqual(
            split_nodes_delimiter([node], delimiter, text_type),
            [
                TextNode("this is some ", TextType.TEXT),
                TextNode("italic", text_type),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_inline_code(self):
        node = TextNode("this is an `inline code` block", TextType.TEXT)
        delimiter = "`"
        text_type = TextType.CODE

        self.assertEqual(
            split_nodes_delimiter([node], delimiter, text_type),
            [
                TextNode("this is an ", TextType.TEXT),
                TextNode("inline code", text_type),
                TextNode(" block", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_starts_with_delimiter(self):
        node = TextNode("**aha**, bold text", TextType.TEXT)
        delimiter = "**"
        text_type = TextType.BOLD

        self.assertEqual(
            split_nodes_delimiter([node], delimiter, text_type),
            [
                TextNode("aha", text_type),
                TextNode(", bold text", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_ends_with_delimiter(self):
        node = TextNode("text thats _italic_", TextType.TEXT)
        delimiter = "_"
        text_type = TextType.ITALIC

        self.assertEqual(
            split_nodes_delimiter([node], delimiter, text_type),
            [
                TextNode("text thats ", TextType.TEXT),
                TextNode("italic", text_type),
            ],
        )

    def test_split_nodes_delimiter_with_many_delimeters(self):
        node = TextNode("this is **bold** and **bold** this is", TextType.TEXT)
        delimiter = "**"
        text_type = TextType.BOLD

        self.assertEqual(
            split_nodes_delimiter([node], delimiter, text_type),
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" this is", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_with_no_delimiter(self):
        node = TextNode("this is some text", TextType.TEXT)

        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.TEXT),
            [TextNode("this is some text", TextType.TEXT)],
        )

    def split_nodes_delimiter_with_mismatched_delimiter(self):
        node = TextNode("this is _some text", TextType.ITALIC)

        with self.assertRaises(ValueError) as context:
            _ = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            str(context.exception), "invalid markdown: missing closing delimiter, _"
        )

    def test_split_nodes_delimiter_with_non_TextType_TEXT_TextType(self):
        node = TextNode("this is some bold text", TextType.BOLD)

        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [TextNode("this is some bold text", TextType.BOLD)],
        )


class TestLinkAndImageExtraction(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://www.image.com)"
        )
        self.assertEqual([("image", "https://www.image.com")], matches)

    def test_extract_markdown_images_with_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://www.image.com), and another ![image](https://www.image2.com)"
        )
        self.assertEqual(
            [("image", "https://www.image.com"), ("image", "https://www.image2.com")],
            matches,
        )

    def test_extract_markdown_link(self):
        matches = extract_markdown_links("This a [link](https://www.link.com)")
        self.assertEqual([("link", "https://www.link.com")], matches)

    def test_extract_markdown_link_with_multiple_links(self):
        matches = extract_markdown_links(
            "This is one [link](https://www.link.com) and a second [link](https://www.link2.com)"
        )
        self.assertEqual(
            [("link", "https://www.link.com"), ("link", "https://www.link2.com")],
            matches,
        )

    def test_markdown_images_doesnt_extract_links(self):
        matches = extract_markdown_images(
            "This is an ![image](https://www.image.com), and a [link](https://www.link.com)"
        )
        self.assertEqual([("image", "https://www.image.com")], matches)

    def test_markdown_links_doesnt_extract_images(self):
        matches = extract_markdown_links(
            "This is an ![image](https://www.image.com), and a [link](https://www.link.com)"
        )
        self.assertEqual([("link", "https://www.link.com")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image_with_one_image_in_one_node(self):
        alt = "test image"
        url = "https://www.testimage.com"

        node = TextNode(f"this is an ![{alt}]({url})", TextType.TEXT)

        self.assertEqual(
            [
                TextNode("this is an ", TextType.TEXT),
                TextNode(alt, TextType.IMAGE, url),
            ],
            split_nodes_image([node]),
        )

    def test_split_nodes_image_with_one_image_in_multiple_nodes(self):
        alt = "test image"
        url = "https://www.testimage.com"
        old_nodes = [
            TextNode("not an image", TextType.TEXT),
            TextNode("not an image", TextType.TEXT),
            TextNode(f"this is an ![{alt}]({url})", TextType.TEXT),
            TextNode("not an image", TextType.TEXT),
        ]

        self.assertEqual(
            [
                TextNode("not an image", TextType.TEXT),
                TextNode("not an image", TextType.TEXT),
                TextNode("this is an ", TextType.TEXT),
                TextNode(alt, TextType.IMAGE, url),
                TextNode("not an image", TextType.TEXT),
            ],
            split_nodes_image(old_nodes),
        )

    def test_split_nodes_image_with_multiple_images_in_one_node(self):
        alt = "test image"
        url = "https://www.testimage.com"
        node = TextNode(
            f"this is a ![{alt}]({url}) and this is a ![{alt}]({url})", TextType.TEXT
        )

        self.assertEqual(
            [
                TextNode("this is a ", TextType.TEXT),
                TextNode(alt, TextType.IMAGE, url),
                TextNode(" and this is a ", TextType.TEXT),
                TextNode(alt, TextType.IMAGE, url),
            ],
            split_nodes_image([node]),
        )

    def test_split_nodes_image_with_multiple_images_in_multiple_nodes(self):
        alt1 = "test image"
        url1 = "https://www.testimage.com"
        alt2 = "kitty cat"
        url2 = "https://www.kittycat.com"
        alt3 = "doggy"
        url3 = "https://www.doggy.com"

        old_nodes = [
            TextNode(
                f"this is a ![{alt1}]({url1}), and this is a ![{alt2}]({url2})",
                TextType.TEXT,
            ),
            TextNode(
                f"this is a ![{alt2}]({url2}), and this is a ![{alt3}]({url3})",
                TextType.TEXT,
            ),
        ]
        self.assertEqual(
            [
                TextNode("this is a ", TextType.TEXT),
                TextNode(alt1, TextType.IMAGE, url1),
                TextNode(", and this is a ", TextType.TEXT),
                TextNode(alt2, TextType.IMAGE, url2),
                TextNode("this is a ", TextType.TEXT),
                TextNode(alt2, TextType.IMAGE, url2),
                TextNode(", and this is a ", TextType.TEXT),
                TextNode(alt3, TextType.IMAGE, url3),
            ],
            split_nodes_image(old_nodes),
        )

    def test_split_nodes_image_when_node_is_not_text_type_text(self):
        node = TextNode("this is bold text", TextType.BOLD)

        self.assertEqual([node], split_nodes_image([node]))

    def test_split_nodes_image_when_old_nodes_has_no_images(self):
        old_nodes = [
            TextNode("this is some text", TextType.TEXT),
            TextNode("and this is some text", TextType.TEXT),
            TextNode("and even this is some text", TextType.TEXT),
        ]
        self.assertEqual(
            [
                TextNode("this is some text", TextType.TEXT),
                TextNode("and this is some text", TextType.TEXT),
                TextNode("and even this is some text", TextType.TEXT),
            ],
            split_nodes_image(old_nodes),
        )

    def test_split_nodes_image_with_mixed_text_types(self):
        alt = "test image"
        url = "https://www.testimage.com"
        old_nodes = [
            TextNode("this is some bold text", TextType.BOLD),
            TextNode(f"this is a ![{alt}]({url})", TextType.TEXT),
            TextNode("this is some italic text", TextType.ITALIC),
        ]

        self.assertEqual(
            [
                TextNode("this is some bold text", TextType.BOLD),
                TextNode("this is a ", TextType.TEXT),
                TextNode(alt, TextType.IMAGE, url),
                TextNode("this is some italic text", TextType.ITALIC),
            ],
            split_nodes_image(old_nodes),
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link_with_one_link_in_one_node(self):
        src = "test link"
        url = "https://www.testlink.com"

        node = TextNode(f"this is an [{src}]({url})", TextType.TEXT)

        self.assertEqual(
            [
                TextNode("this is an ", TextType.TEXT),
                TextNode(src, TextType.LINK, url),
            ],
            split_nodes_link([node]),
        )

    def test_split_nodes_link_with_one_link_in_multiple_nodes(self):
        src = "test link"
        url = "https://www.testlink.com"
        old_nodes = [
            TextNode("not an link", TextType.TEXT),
            TextNode("not an link", TextType.TEXT),
            TextNode(f"this is an [{src}]({url})", TextType.TEXT),
            TextNode("not an link", TextType.TEXT),
        ]

        self.assertEqual(
            [
                TextNode("not an link", TextType.TEXT),
                TextNode("not an link", TextType.TEXT),
                TextNode("this is an ", TextType.TEXT),
                TextNode(src, TextType.LINK, url),
                TextNode("not an link", TextType.TEXT),
            ],
            split_nodes_link(old_nodes),
        )

    def test_split_nodes_link_with_multiple_links_in_one_node(self):
        src = "test link"
        url = "https://www.testlink.com"
        node = TextNode(
            f"this is a [{src}]({url}) and this is a [{src}]({url})", TextType.TEXT
        )

        self.assertEqual(
            [
                TextNode("this is a ", TextType.TEXT),
                TextNode(src, TextType.LINK, url),
                TextNode(" and this is a ", TextType.TEXT),
                TextNode(src, TextType.LINK, url),
            ],
            split_nodes_link([node]),
        )

    def test_split_nodes_link_with_multiple_links_in_multiple_nodes(self):
        src1 = "test link"
        url1 = "https://www.testlink.com"
        src2 = "kitty cat"
        url2 = "https://www.kittycat.com"
        src3 = "doggy"
        url3 = "https://www.doggy.com"

        old_nodes = [
            TextNode(
                f"this is a [{src1}]({url1}), and this is a [{src2}]({url2})",
                TextType.TEXT,
            ),
            TextNode(
                f"this is a [{src2}]({url2}), and this is a [{src3}]({url3})",
                TextType.TEXT,
            ),
        ]
        self.assertEqual(
            [
                TextNode("this is a ", TextType.TEXT),
                TextNode(src1, TextType.LINK, url1),
                TextNode(", and this is a ", TextType.TEXT),
                TextNode(src2, TextType.LINK, url2),
                TextNode("this is a ", TextType.TEXT),
                TextNode(src2, TextType.LINK, url2),
                TextNode(", and this is a ", TextType.TEXT),
                TextNode(src3, TextType.LINK, url3),
            ],
            split_nodes_link(old_nodes),
        )

    def test_split_nodes_link_when_node_is_not_text_type_text(self):
        node = TextNode("this is bold text", TextType.BOLD)

        self.assertEqual([node], split_nodes_link([node]))

    def test_split_nodes_link_when_old_nodes_has_no_links(self):
        old_nodes = [
            TextNode("this is some text", TextType.TEXT),
            TextNode("and this is some text", TextType.TEXT),
            TextNode("and even this is some text", TextType.TEXT),
        ]
        self.assertEqual(
            [
                TextNode("this is some text", TextType.TEXT),
                TextNode("and this is some text", TextType.TEXT),
                TextNode("and even this is some text", TextType.TEXT),
            ],
            split_nodes_link(old_nodes),
        )

    def test_split_nodes_link_with_mixed_text_types(self):
        src = "test link"
        url = "https://www.testlink.com"
        old_nodes = [
            TextNode("this is some bold text", TextType.BOLD),
            TextNode(f"this is a [{src}]({url})", TextType.TEXT),
            TextNode("this is some italic text", TextType.ITALIC),
        ]

        self.assertEqual(
            [
                TextNode("this is some bold text", TextType.BOLD),
                TextNode("this is a ", TextType.TEXT),
                TextNode(src, TextType.LINK, url),
                TextNode("this is some italic text", TextType.ITALIC),
            ],
            split_nodes_link(old_nodes),
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes_with_multiple_text_types(self):
        text = "this is **some** example _text_ with an ![image](https://www.image.com), `some code` and even a [link](https://www.link.com)"

        self.assertEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("some", TextType.BOLD),
                TextNode(" example ", TextType.TEXT),
                TextNode("text", TextType.ITALIC),
                TextNode(" with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://www.image.com"),
                TextNode(", ", TextType.TEXT),
                TextNode("some code", TextType.CODE),
                TextNode(" and even a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.link.com"),
            ],
            text_to_textnodes(text),
        )

    def test_text_to_text_nodes_with_no_links_or_images(self):
        text = "this is **some** example _text_ with `some code`"

        self.assertEqual(
            [
                TextNode("this is ", TextType.TEXT),
                TextNode("some", TextType.BOLD),
                TextNode(" example ", TextType.TEXT),
                TextNode("text", TextType.ITALIC),
                TextNode(" with ", TextType.TEXT),
                TextNode("some code", TextType.CODE),
            ],
            text_to_textnodes(text),
        )

    def test_text_to_text_nodes_with_no_delimiters_links_or_images(self):
        text = "this is some example text"

        self.assertEqual(
            [TextNode("this is some example text", TextType.TEXT)],
            text_to_textnodes(text),
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_ignores_empty_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items




"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_strips_blocks_of_extra_whitespace(self):
        md = """
 This is **bolded** paragraph

 This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

 - This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
