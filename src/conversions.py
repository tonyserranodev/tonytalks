import re

from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 != 0:
            raise ValueError(
                f"invalid markdown: missing closing delimiter, {delimiter}"
            )

        parts = node.text.split(delimiter)
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:

    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        curr_text = node.text
        for match in matches:
            alt, url = match[0], match[1]

            sections = curr_text.split(f"![{alt}]({url})")
            before = sections[0]
            curr_text = sections[1] if len(sections) > 1 else ""

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(alt, TextType.IMAGE, url))

        if curr_text != "":
            new_nodes.append(TextNode(curr_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue

        curr_text = node.text
        for match in matches:
            src, url = match[0], match[1]

            sections = curr_text.split(f"[{src}]({url})")
            before = sections[0]
            curr_text = sections[1] if len(sections) > 1 else ""

            if before != "":
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(src, TextType.LINK, url))

        if curr_text != "":
            new_nodes.append(TextNode(curr_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    return split_nodes_link(nodes)


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [block.strip() for block in markdown.split("\n\n")]
    blocks = [block for block in blocks if block != ""]

    return blocks
