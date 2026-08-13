class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return

        prop_str = ""

        for prop in self.props:
            prop_str += f' {prop}="{self.props[prop]}"'

        return prop_str.strip()

    def __repr__(self) -> str:
        result = ""
        if self.tag: result += f"Tag: {self.tag}\n"
        if self.value: result += f"Tag: {self.tag}\n"
        if self.children:
            result += "Children:"
            for child in self.children:
                result += f"\n-> {child}"
        if self.props:
            result += "\n"
            for prop in self.props:
                result += f"{prop}: {self.props[prop]}"
        return result
