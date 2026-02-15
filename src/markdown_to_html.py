from blocks import BlockType, block_to_block_type
from conversions import markdown_to_blocks, text_node_to_html_node, text_to_textnodes
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, TextType


def markdown_to_html_node(markdown: str) -> HTMLNode:
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children = text_to_children(block.replace("\n", " "))
                html_node = ParentNode("p", children)
                html_nodes.append(html_node)
            case BlockType.HEADING:
                prefix, rest = block.split(" ", 1)
                level = len(prefix)
                text = rest.strip()
                children = text_to_children(text)
                html_nodes.append(ParentNode(f"h{level}", children))
            case BlockType.CODE:
                lines = block.strip("\n").split("\n")
                code_text = "\n".join(lines[1:-1])
                code_text += "\n"
                code_html = text_node_to_html_node(TextNode(code_text, TextType.CODE))
                html_nodes.append(ParentNode("pre", [code_html]))
            case BlockType.QUOTE:
                lines = block.strip("\n").split("\n")
                quote_text = []
                for line in lines:
                    quote_text.append(line.strip(">").strip())

                text = " ".join(quote_text)
                children = text_to_children(text)
                html_node = ParentNode("blockquote", children)
                html_nodes.append(html_node)
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                li_nodes = []
                for line in lines:
                    item_text = line[2:]
                    li_nodes.append(ParentNode("li", text_to_children(item_text)))
                html_nodes.append(ParentNode("ul", li_nodes))
            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                li_nodes = []
                for line in lines:
                    _, item_text = line.split(". ", 1)
                    li_nodes.append(ParentNode("li", text_to_children(item_text)))
                html_nodes.append(ParentNode("ol", li_nodes))

    return ParentNode("div", html_nodes)


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text.strip("\n"))
    children = list(map(text_node_to_html_node, text_nodes))
    return children  # pyright: ignore[reportReturnType]
