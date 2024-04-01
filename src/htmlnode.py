from functools import reduce


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] = [],
        props: dict[str, str] = {},
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        """
        Generate a string from this object's props dictionary which matches the inline HTML representation of props.
        """

        def props_concat(a: str, b: tuple[str, str]):
            return (
                a + f' {b[0]}="{b[1]}"'
            )  # Extra space on left side is intentional! That is the space between tag and props

        return reduce(props_concat, self.props.items(), "")


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = {}):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have children")

        contents = "".join(map(lambda x: x.to_html(), self.children))

        return f"<{self.tag}{self.props_to_html()}>{contents}</{self.tag}>"


class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: str | None = None, props: dict[str, str] = {}):
        super().__init__(tag, value, None, props)  # A leaf node may not have children

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")

        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return self.value
