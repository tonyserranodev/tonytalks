import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = ("paragraph",)
    HEADING = ("heading",)
    CODE = ("code",)
    QUOTE = ("quote",)
    UNORDERED_LIST = ("unordered_list",)
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    for line in block.strip("\n").split("\n"):
        if not line.startswith(">"):
            break
        return BlockType.QUOTE

    for line in block.strip("\n").split("\n"):
        if not line.startswith("- "):
            break
        return BlockType.UNORDERED_LIST

    for line in block.strip("\n").split("\n"):
        if not re.match(r"^[1-9]\d*\. ", line):
            break
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
