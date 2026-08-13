import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        """Testet das Rendering eines einfachen <p>-Tags."""
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        """Testet das Rendering eines <a>-Tags mit Attributen."""
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        """Testet das Rendering, wenn tag=None ist (Rohtext)."""
        node = LeafNode(None, "Just raw text.")
        self.assertEqual(node.to_html(), "Just raw text.")

    def test_leaf_to_html_no_value_raises_value_error(self):
        """Testet, ob eine ValueError geworfen wird, wenn value None ist."""
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_multiple_props(self):
        """Testet das Rendering mit mehreren Props (z.B. img oder button)."""
        node = LeafNode("button", "Submit", {"type": "submit", "class": "btn"})
        self.assertEqual(node.to_html(), '<button type="submit" class="btn">Submit</button>')


if __name__ == "__main__":
    unittest.main()
