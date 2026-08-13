import unittest

from src.htmlnode import HTMLNode
from src.leafnode import LeafNode
from src.parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    # --- Vorgegebene Tests ---

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    # --- Weitere passende Tests für DEINEN Code ---

    def test_to_html_many_children(self):
        """Testet mehrere verschiedene LeafNode-Kinder in einem ParentNode."""
        children: list[HTMLNode] = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode("p", children)
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_with_props(self):
        """Testet ParentNode mit HTML-Attributen/Props."""
        children: list[HTMLNode] = [LeafNode("p", "Content")]
        node = ParentNode(
            "div",
            children,
            {"class": "container", "id": "main"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container" id="main"><p>Content</p></div>',
        )

    def test_to_html_deeply_nested(self):
        """Testet mehrere Ebenen tief verschachtelte ParentNodes."""
        p_children: list[HTMLNode] = [LeafNode("b", "Deep text")]
        sec_children: list[HTMLNode] = [ParentNode("p", p_children)]
        div_children: list[HTMLNode] = [ParentNode("section", sec_children)]

        node = ParentNode("div", div_children)
        self.assertEqual(
            node.to_html(),
            "<div><section><p><b>Deep text</b></p></section></div>",
        )

    def test_to_html_empty_tag_raises_value_error(self):
        """Passend zu deiner Zeile: if self.tag == '': raise ValueError(...)"""
        children: list[HTMLNode] = [LeafNode("span", "child")]
        node = ParentNode("", children)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_empty_children_raises_value_error(self):
        """Passend zu deiner Zeile: if self.children == []: raise ValueError(...)"""
        children: list[HTMLNode] = []
        node = ParentNode("div", children)
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
