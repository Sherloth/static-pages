import os
import sys
import unittest

# Ensure local imports work when running from the repo root
sys.path.append(os.path.dirname(__file__))

from textnode import TextNode, TextType
from functions import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        node3 = TextNode("This is a different text node", TextType.LINK, "https://example.com")
        node4 = TextNode("This is a different text node", TextType.LINK, "https://example.com")
        node5 = TextNode("This is a different text node", TextType.LINK, "https://other.com")  # no None

        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node4, node5)


class TestSplitNodesDelimiter(unittest.TestCase):
    # --- Bold (**)... ---
    def test_split_bold_simple(self):
        node = TextNode("This is **bold** here", TextType.TEXT)
        out = list(split_nodes_delimiter([node], "**", TextType.BOLD))
        self.assertEqual(
            out,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_unmatched_delimiter_bold_raises(self):
        node = TextNode("This is **broken", TextType.TEXT)
        with self.assertRaises(ValueError):
            list(split_nodes_delimiter([node], "**", TextType.BOLD))

    def test_empty_segments_at_edges_ignored_bold(self):
        node = TextNode("**bold**", TextType.TEXT)
        out = list(split_nodes_delimiter([node], "**", TextType.BOLD))
        self.assertEqual(out, [TextNode("bold", TextType.BOLD)])

    # --- Italic (_) ... ---
    def test_split_italic_simple(self):
        node = TextNode("This is _ital_ here", TextType.TEXT)
        out = list(split_nodes_delimiter([node], "_", TextType.ITALIC))
        self.assertEqual(
            out,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("ital", TextType.ITALIC),
                TextNode(" here", TextType.TEXT),
            ],
        )

    def test_multiple_occurrences_italic(self):
        node = TextNode("a _x_ b _y_ c", TextType.TEXT)
        out = list(split_nodes_delimiter([node], "_", TextType.ITALIC))
        self.assertEqual(
            out,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("x", TextType.ITALIC),
                TextNode(" b ", TextType.TEXT),
                TextNode("y", TextType.ITALIC),
                TextNode(" c", TextType.TEXT),
            ],
        )

    # --- Mixed / chaining (bold then italic) ---
    def test_chain_bold_then_italic(self):
        text = "Start **bold** and _ital_ end"
        nodes = [TextNode(text, TextType.TEXT)]

        nodes = list(split_nodes_delimiter(nodes, "**", TextType.BOLD))
        nodes = list(split_nodes_delimiter(nodes, "_", TextType.ITALIC))

        self.assertEqual(
            nodes,
            [
                TextNode("Start ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("ital", TextType.ITALIC),
                TextNode(" end", TextType.TEXT),
            ],
        )

    # --- No-op / preservation ---
    def test_no_delimiter_noop(self):
        node = TextNode("No special here", TextType.TEXT)
        out = list(split_nodes_delimiter([node], "**", TextType.BOLD))
        self.assertEqual(out, [node])

    def test_preserve_non_text_nodes(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        link_node = TextNode("click me", TextType.LINK, "https://example.com")
        image_node = TextNode("logo", TextType.IMAGE, "https://example.com/logo.png")

        out = list(split_nodes_delimiter([bold_node, link_node, image_node], "**", TextType.BOLD))
        self.assertEqual(out, [bold_node, link_node, image_node])

    def test_interleaved_text_untouched(self):
        a = TextNode("A **b** C", TextType.TEXT)
        mid = TextNode("MIDDLE", TextType.LINK, "https://example.com")
        z = TextNode("Z _i_!", TextType.TEXT)

        nodes = [a, mid, z]
        nodes = list(split_nodes_delimiter(nodes, "**", TextType.BOLD))
        nodes = list(split_nodes_delimiter(nodes, "_", TextType.ITALIC))

        self.assertEqual(
            nodes,
            [
                TextNode("A ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" C", TextType.TEXT),
                mid,
                TextNode("Z ", TextType.TEXT),
                TextNode("i", TextType.ITALIC),
                TextNode("!", TextType.TEXT),
            ],
        )
    
    def test_regex_markdown(self):
        a = "I'm a little ![teapot](https://example.com/teapot.png)"
        b = "This has [lane](https://example.com/lane) and [hunter](https://example.org/hunter)"
        self.assertEqual(
            extract_markdown_images(a),
            [("teapot", "https://example.com/teapot.png")]
        )
        self.assertEqual(
            extract_markdown_links(b),
            [("lane", "https://example.com/lane"), ("hunter", "https://example.org/hunter")]
        )
if __name__ == "__main__":
    unittest.main()
