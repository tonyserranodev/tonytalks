import unittest

from markdown_to_html import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    maxDiff = None

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# This is a heading level 1

## This is a heading level 2

### This is a heading level 3

#### This is a heading level 4

##### This is a heading level 5

###### This is a heading level 6
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading level 1</h1><h2>This is a heading level 2</h2><h3>This is a heading level 3</h3><h4>This is a heading level 4</h4><h5>This is a heading level 5</h5><h6>This is a heading level 6</h6></div>",
        )

    def test_headings_with_inline_markdown(self):
        md = """
# This is a heading level 1 with **bold** text and _italic_ text

## This is a heading level 2 with **bold** text and _italic_ text

### This is a heading level 3 with **bold** text and _italic_ text

#### This is a heading level 4 with **bold** text and _italic_ text

##### This is a heading level 5 with **bold** text and _italic_ text

###### This is a heading level 6 with **bold** text and _italic_ text
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading level 1 with <b>bold</b> text and <i>italic</i> text</h1><h2>This is a heading level 2 with <b>bold</b> text and <i>italic</i> text</h2><h3>This is a heading level 3 with <b>bold</b> text and <i>italic</i> text</h3><h4>This is a heading level 4 with <b>bold</b> text and <i>italic</i> text</h4><h5>This is a heading level 5 with <b>bold</b> text and <i>italic</i> text</h5><h6>This is a heading level 6 with <b>bold</b> text and <i>italic</i> text</h6></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote(self):
        md = """
> quoted text
> quoted text
> quoted text
> quoted text
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>quoted text quoted text quoted text quoted text</blockquote></div>",
        )

    def test_quote_with_inline_markdown(self):
        md = """
> this is some **bold** text
> and some _italic_ text
> and some regular text
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>this is some <b>bold</b> text and some <i>italic</i> text and some regular text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- heres a bullet point
- and another point
- and a third point
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>heres a bullet point</li><li>and another point</li><li>and a third point</li></ul></div>",
        )

    def test_unordered_list_with_inline_markdown(self):
        md = """
- heres a **bold** bullet point
- and an _italic_ bullet point
- and a third point
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>heres a <b>bold</b> bullet point</li><li>and an <i>italic</i> bullet point</li><li>and a third point</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. Go to the sto
2. Do the laundry
3. Fold the laundry
4. Cry
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Go to the sto</li><li>Do the laundry</li><li>Fold the laundry</li><li>Cry</li></ol></div>",
        )

    def test_ordered_list_with_inline_markdown(self):
        md = """
1. Go **to** _the_ sto
2. Do **the** laundry
3. Fold _the_ laundry
4. Cry
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Go <b>to</b> <i>the</i> sto</li><li>Do <b>the</b> laundry</li><li>Fold <i>the</i> laundry</li><li>Cry</li></ol></div>",
        )
