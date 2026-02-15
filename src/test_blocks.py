import unittest
from blocks import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_returns_heading(self):
        blocks = [
            "# An example heading",
            "## An example heading",
            "### An example heading",
            "#### An example heading",
            "##### An example heading",
            "###### An example heading",
        ]
        for block in blocks:
            self.assertEqual(BlockType.HEADING, block_to_block_type(block))

    def test_block_to_block_type_returns_code(self):
        block = """```
        print("Hello, world!")
        ```"""
        self.assertEqual(
            BlockType.CODE, block_to_block_type(block), f"\nblock: {block}"
        )

    def test_block_to_block_type_returns_quote(self):
        block = """
> this is a quote
> this is a quote
> this is a quote
> this is a quote
        """
        bad_block = """
 this is a quote
> this is a quote
> this is a quote
> this is a quote
        """
        self.assertEqual(
            BlockType.QUOTE, block_to_block_type(block), f"\nblock: {block}"
        )
        self.assertNotEqual(
            BlockType.QUOTE, block_to_block_type(bad_block), f"\nblock: {bad_block}"
        )

    def test_block_to_block_type_returns_unordered_list(self):
        block = """
- this is an unordered list
- this is an unordered list
- this is an unordered list
- this is an unordered list
        """
        bad_block = """
this is an unordered list
- this is an unordered list
- this is an unordered list
- this is an unordered list
        """

        self.assertEqual(
            BlockType.UNORDERED_LIST, block_to_block_type(block), f"\nblock: {block}"
        )
        self.assertNotEqual(
            BlockType.UNORDERED_LIST,
            block_to_block_type(bad_block),
            f"\nblock: {bad_block}",
        )

    def test_block_to_block_type_returns_ordered_list(self):
        block = """
1. this is an ordered list
2. this is an ordered list
3. this is an ordered list
4. this is an ordered list
        """
        bad_block = """
. this is an ordered list
2. this is an ordered list
3. this is an ordered list
4. this is an ordered list
        """

        self.assertEqual(
            BlockType.ORDERED_LIST, block_to_block_type(block), f"\nblock: {block}"
        )
        self.assertNotEqual(
            BlockType.ORDERED_LIST,
            block_to_block_type(bad_block),
            f"\nblock: {bad_block}",
        )

    def test_block_to_block_type_returns_paragraph(self):
        block = """
normal text
straight up normal text
and even more normal text
        """
        self.assertEqual(
            BlockType.PARAGRAPH, block_to_block_type(block), f"\nblock: {block}"
        )
