import unittest

from textnode import TextNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node_A = TextNode("This is a text node", "bold")
        node_B = TextNode("This is a text node", "bold")
        self.assertEqual(node_A, node_B)

        node_C = TextNode(
            "This is a DIFFERENT text node", "italic", "https://google.com"
        )
        node_D = TextNode(
            "This is a DIFFERENT text node", "italic", "https://google.com"
        )
        self.assertEqual(node_C, node_D)

    def test_neq(self):
        node_A = TextNode("This is a text node", "bold")
        node_B = TextNode("This is a DIFFERENT text node", "bold")
        self.assertNotEqual(node_A, node_B)  # Nodes with different text

        node_C = TextNode("This is a text node", "italic")
        self.assertNotEqual(node_A, node_C)  # Nodes with different formatting

        node_D = TextNode("This is a text node", "bold", "https://google.com")
        self.assertNotEqual(node_A, node_D)  # Node with no URL vs Node with URL

        node_E = TextNode("This is a text node", "bold", "https://apple.com")
        self.assertNotEqual(node_D, node_E)  # Nodes with different URLs

    def test_repr(self):
        node_A = TextNode("This is a text node", "bold")
        self.assertEqual(repr(node_A), "TextNode(This is a text node, bold, None)")

        node_B = TextNode(
            "This is a DIFFERENT text node", "italic", "https://google.com"
        )
        self.assertEqual(
            repr(node_B),
            "TextNode(This is a DIFFERENT text node, italic, https://google.com)",
        )


if __name__ == "__main__":
    unittest.main()
