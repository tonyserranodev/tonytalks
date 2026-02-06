class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html = ""
        if self.props is None or len(self.props) == 0:
            return ""

        for prop in self.props:
            html += f' {prop}="{self.props[prop]}"'
        return html

    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}\nprops: {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, props)
        self.tag = tag
        self.value = value
        self.props = props

    def to_html(self):
        if self.value is None or self.value == "":
            raise ValueError("All leaf nodes must have a value")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode(tag: {self.tag}\nvalue: {self.value}\nprops: {self.props})"
