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