import unittest

from extract import extract_markdown_images, extract_markdown_links


class TestExtract(unittest.TestCase):
    def test_images(self):
        text_A = "Go to [Google.com](https://google.com) today! ![Google Logo](https://google.com/logo)"
        self.assertEqual(
            extract_markdown_images(text_A),
            [("Google Logo", "https://google.com/logo")],
        )

    def test_images(self):
        text_A = "Go to [Google.com](https://google.com) today! ![Google Logo](https://google.com/logo)"
        self.assertEqual(
            extract_markdown_links(text_A),
            [("Google.com", "https://google.com")],
        )
