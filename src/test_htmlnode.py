import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node_A = HTMLNode(None, None, None, {"class": "testClass", "id": "testID"})
        self.assertEqual(node_A.props_to_html(), ' class="testClass" id="testID"')

        node_B = HTMLNode()  # All args None
        self.assertEqual(node_B.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node_A = LeafNode("Hello world!", "p", {"class": "testClass", "id": "testID"})
        self.assertEqual(
            node_A.to_html(), '<p class="testClass" id="testID">Hello world!</p>'
        )

        node_B = LeafNode("Hello world!")
        self.assertEqual(node_B.to_html(), "Hello world!")

        node_C = LeafNode(
            "Hello world!", None, {"class": "testClass", "id": "testID"}
        )  # Can't apply props if no tag! This should never occur regardless
        self.assertEqual(node_C.to_html(), "Hello world!")

        node_D = LeafNode("Hello world!", "a")
        self.assertEqual(node_D.to_html(), "<a>Hello world!</a>")


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        child_A = LeafNode("Hello world!")

        node_A = ParentNode("p", [child_A], {"class": "testClass"})
        self.assertEqual(node_A.to_html(), '<p class="testClass">Hello world!</p>')

        node_B = ParentNode("div", [node_A])
        self.assertEqual(
            node_B.to_html(), '<div><p class="testClass">Hello world!</p></div>'
        )

        node_C = ParentNode("", [])
        self.assertRaises(ValueError, node_C.to_html)  # No tag
        node_C.tag = "div"
        self.assertRaises(ValueError, node_C.to_html)  # Still doesn't have children
        node_C.children = [node_B]
        self.assertEqual(  # Should work with both required params fixed
            node_C.to_html(),
            '<div><div><p class="testClass">Hello world!</p></div></div>',
        )
