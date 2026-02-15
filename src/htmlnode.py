from typing import override


type Props = dict[str, str | None] | None


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: Props = None,
    ) -> None:
        self.tag: str | None = tag
        self.value: str | None = value
        self.children: list[HTMLNode] | None = children
        self.props: Props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        html = ""
        if self.props is None or len(self.props) == 0:
            return ""

        for prop in self.props:
            html += f' {prop}="{self.props[prop]}"'
        return html

    @override
    def __repr__(self) -> str:
        return f"HTMLNode(tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: Props = None):
        super().__init__(tag=tag, value=value, props=props)

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    @override
    def __repr__(self):
        return f"LeafNode(tag: {self.tag}\nvalue: {self.value}\nprops: {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: Props = None,
    ) -> None:
        super().__init__(tag=tag, children=children, props=props)

    @override
    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")

        if self.children is None:
            raise ValueError("All parent nodes must have children")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
