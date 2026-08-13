import unittest
from htmlnode import HTMLNode  # Anpassen an deinen Dateinamen


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_formatting(self):
        """Testet, ob props_to_html einen korrekt formatierten String zurückgibt."""
        node = HTMLNode(
            tag="a",
            props={"href": "https://www.google.com", "target": "_blank"}
        )
        expected = 'href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_none_or_empty(self):
        """Testet, ob props_to_html None zurückgibt, wenn keine Props angegeben sind."""
        node_none = HTMLNode(tag="p")
        node_empty = HTMLNode(tag="p", props={})

        self.assertIsNone(node_none.props_to_html())
        self.assertIsNone(node_empty.props_to_html())

    def test_to_html_raises_not_implemented(self):
        """Testet, ob to_html eine NotImplementedError wirft."""
        node = HTMLNode(tag="p", value="Hallo Welt")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_html_node_initialization_defaults(self):
        """Testet die Standardwerte bei der Initialisierung ohne Argumente."""
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)


if __name__ == "__main__":
    unittest.main()
