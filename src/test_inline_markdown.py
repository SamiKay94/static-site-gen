import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://wikipedia.org"),
            ],
            matches,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_basic(self):
            """Basic single match"""
            node = TextNode(
                "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) inside.",
                TextType.TEXT,
            )
            new_nodes = split_nodes_image([node])
            self.assertListEqual(
                [
                    TextNode("This is text with an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" inside.", TextType.TEXT),
                ],
                new_nodes,
            )

    def test_split_images_multiple(self):
        """Multiple matches interspersed with text"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_images_consecutive(self):
        """Consecutive matches without text in between"""
        node = TextNode(
            "![img1](https://example.com/1.png)![img2](https://example.com/2.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("img1", TextType.IMAGE, "https://example.com/1.png"),
                TextNode("img2", TextType.IMAGE, "https://example.com/2.png"),
            ],
            new_nodes,
        )

    def test_split_images_start_and_end(self):
        """Match at the start and end of text"""
        node = TextNode(
            "![start](https://example.com/start.png) middle text ![end](https://example.com/end.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://example.com/start.png"),
                TextNode(" middle text ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "https://example.com/end.png"),
            ],
            new_nodes,
        )

    def test_split_images_no_matches(self):
        """No matches - returns original node untouched"""
        node = TextNode("This is just plain text without images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_split_images_wrong_text_type(self):
        """Node with non-TEXT type should not be processed"""
        node = TextNode("![image](https://example.com/img.png)", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    def test_text_to_textnodes_all(self):
        """Node with all examples"""
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")

        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

    def test_text_to_textnodes_text_only(self):
        nodes = text_to_textnodes("Just a regular text without any markdown stuff")

        self.assertEqual(
            [
                TextNode("Just a regular text without any markdown stuff", TextType.TEXT)
            ],
            nodes
        )

    def test_text_to_textnodes_one_type(self):
        nodes = text_to_textnodes("Just a **regular text** without any markdown stuff")

        self.assertEqual(
            [
                TextNode("Just a ", TextType.TEXT),
                TextNode("regular text", TextType.BOLD),
                TextNode(" without any markdown stuff", TextType.TEXT)
            ],
            nodes
        )

    def test_text_to_textnodes_two_images(self):
        nodes = text_to_textnodes("Hier ist das erste Bild ![Bild 1](https://example.com/1.png) und direkt danach das zweite ![Bild 2](https://example.com/2.png) im selben Text.")

        self.assertEqual(
            [
                TextNode("Hier ist das erste Bild ", TextType.TEXT),
                TextNode("Bild 1", TextType.IMAGE, "https://example.com/1.png"),
                TextNode(" und direkt danach das zweite ", TextType.TEXT),
                TextNode("Bild 2", TextType.IMAGE, "https://example.com/2.png"),
                TextNode(" im selben Text.", TextType.TEXT)
            ],
            nodes
        )

    def test_text_to_textnodes_two_links(self):
        nodes = text_to_textnodes("Besuche [Google](https://google.com) oder alternativ [GitHub](https://github.com) für den Code.")

        self.assertEqual(
            [
                TextNode("Besuche ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(" oder alternativ ", TextType.TEXT),
                TextNode("GitHub", TextType.LINK, "https://github.com"),
                TextNode(" für den Code.", TextType.TEXT)
            ],
            nodes
        )

    def test_text_to_textnodes_consecutive(self):
        nodes = text_to_textnodes("[Link 1](https://a.com)[Link 2](https://b.com)")

        self.assertEqual(
            [
                TextNode("Link 1", TextType.LINK, "https://a.com"),
                TextNode("Link 2", TextType.LINK, "https://b.com"),
            ],
            nodes
        )

    def test_text_to_textnodes_empty(self):
        nodes = text_to_textnodes("")

        nodes_ws = text_to_textnodes("   ")

        self.assertEqual(
            [],
            nodes
        )

        self.assertEqual(
            [],
            nodes_ws
        )

    def test_text_to_textnodes_beginning_or_end(self):
        start = text_to_textnodes("**Fett** steht direkt am Anfang des Satzes.")
        end = text_to_textnodes("Der Satz endet mit _kursiv_.")
        full = text_to_textnodes("`vollstaendiger code block`")
        both = text_to_textnodes("[Link am Anfang](https://start.com) Mitte [Link am Ende](https://end.com)")

        self.assertEqual(
            [
                TextNode("Fett", TextType.BOLD),
                TextNode(" steht direkt am Anfang des Satzes.", TextType.TEXT)
            ],
            start
        )

        self.assertEqual(
            [
                TextNode("Der Satz endet mit ", TextType.TEXT),
                TextNode("kursiv", TextType.ITALIC),
                TextNode(".", TextType.TEXT)
            ],
            end
        )

        self.assertEqual(
            [
                TextNode("vollstaendiger code block", TextType.CODE),
            ],
            full
        )
        self.assertEqual(
            [
                TextNode("Link am Anfang", TextType.LINK, "https://start.com"),
                TextNode(" Mitte ", TextType.TEXT),
                TextNode("Link am Ende", TextType.LINK, "https://end.com"),
            ],
            both
        )

if __name__ == "__main__":
    unittest.main()
