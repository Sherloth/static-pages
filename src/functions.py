from textnode import TextNode, TextType, LeafNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            yield node
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' in text: {node.text}")
        
        for i, part in enumerate(parts):
            if not part:
                continue
            yield TextNode(part, text_type if i % 2 else TextType.TEXT)
    
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\]]+)\]\(([^)]+)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(text)

        if not matches:
            new_nodes.append(node)
            continue

        parts = re.split(r"!\[[^\]]+\]\([^)]+\)", text)

        for i, part in enumerate(parts):
            if part:
                new_nodes.append(TextNode(part, TextType.TEXT))
            if i < len(matches):
                alt, url = matches[i]
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)

        if not matches:
            new_nodes.append(node)
            continue

        parts = re.split(r"(?<!!)\[[^\]]+\]\([^)]+\)", text)

        for i, part in enumerate(parts):
            if part:
                new_nodes.append(TextNode(part, TextType.TEXT))
            if i < len(matches):
                anchor, url = matches[i]
                new_nodes.append(TextNode(anchor, TextType.LINK, url))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = list(split_nodes_delimiter(nodes, "`", TextType.CODE))
    nodes = list(split_nodes_delimiter(nodes, "**", TextType.BOLD))
    nodes = list(split_nodes_delimiter(nodes, "_", TextType.ITALIC))
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for block in raw_blocks:
        clean = block.strip()
        if clean:
            blocks.append(clean)
    return blocks

def text_node_to_html_node(text_node):
        if text_node.text_type == TextType.TEXT:
            return LeafNode(None, text_node.text)
        if text_node.text_type == TextType.BOLD:
            return LeafNode("b", text_node.text)
        if text_node.text_type == TextType.ITALIC:
            return LeafNode("i", text_node.text)
        if text_node.text_type == TextType.CODE:
            return LeafNode("code", text_node.text)
        if text_node.text_type == TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        if text_node.text_type == TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        raise ValueError(f"invalid text type: {text_node.text_type}")