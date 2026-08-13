from inline_markdown import split_nodes_image
from textnode import TextNode, TextType


def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://boot.dev")
    print(node)

    node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

    print(split_nodes_image([node]))

main()
