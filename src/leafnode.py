from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):
        self.tag = tag
        self.props = props
        self.value = value

    def to_html(self):
        if not self.value:
            raise ValueError("no value presented")
        if not self.tag:
            return self.value

        prop_text = ""
        if self.props:
            for prop in self.props:
                prop_text += f' {prop}="{self.props[prop]}"'

        return f"<{self.tag}{prop_text}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        result = ""
        if self.tag:
            result += f"Tag: {self.tag}\n"
        if self.value:
            result += f"Value: {self.value}"
        if self.props:
            result += "\nProps:\n"
            for prop, val in self.props.items():
                result += f"  {prop}: {val}\n"
        return result
