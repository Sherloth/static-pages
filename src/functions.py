from textnode import TextNode, TextType
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
