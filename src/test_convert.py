import unittest

from convert import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
)
from textnode import TextNode


class TestConvert(unittest.TestCase):
    def test_split_delim(self):
        node_A = TextNode("*Hello* **World!**", "text")

        step_one = split_nodes_delimiter([node_A], "**", "bold")
        self.assertEqual(
            step_one, [TextNode("*Hello* ", "text"), TextNode("World!", "bold")]
        )

        step_two = split_nodes_delimiter(step_one, "*", "italic")
        self.assertEqual(
            step_two,
            [
                TextNode("Hello", "italic"),
                TextNode(" ", "text"),
                TextNode("World!", "bold"),
            ],
        )

    def test_split_image(self):
        node_A = TextNode(
            "Go to [Google.com](https://google.com) today! ![Google Logo](https://google.com/logo)",
            "text",
        )
        self.assertEqual(
            split_nodes_image([node_A]),
            [
                TextNode("Go to [Google.com](https://google.com) today! ", "text"),
                TextNode("Google Logo", "image", "https://google.com/logo"),
            ],
        )

    def test_split_link(self):
        node_A = TextNode(
            "Go to [Google.com](https://google.com) today! ![Google Logo](https://google.com/logo)",
            "text",
        )
        self.assertEqual(
            split_nodes_link([node_A]),
            [
                TextNode("Go to ", "text"),
                TextNode("Google.com", "link", "https://google.com"),
                TextNode(" today! ![Google Logo](https://google.com/logo)", "text"),
            ],
        )

    def test_text_to_nodes(self):
        text = "Go to [Google.com](https://google.com) today! ![Google Logo](https://google.com/logo)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("Go to ", "text"),
                TextNode("Google.com", "link", "https://google.com"),
                TextNode(" today! ", "text"),
                TextNode("Google Logo", "image", "https://google.com/logo"),
            ],
        )

    def test_markdown_to_blocks(self):
        markdown = "This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items"
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )
