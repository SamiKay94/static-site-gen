from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag == "" or self.tag is None:
            raise ValueError("no tag provided")
        if self.children == [] or self.children is None:
            raise ValueError("no children provided")

        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        prop_text = ""
        if self.props:
            for prop in self.props:
                prop_text += f' {prop}="{self.props[prop]}"'

        return f"<{self.tag}{prop_text}>{children_html}</{self.tag}>"
