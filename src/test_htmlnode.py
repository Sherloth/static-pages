import pytest
from htmlnode import HTMLNode  # assumes src/htmlnode.py and tests run with PYTHONPATH=src

def test_props_to_html_none():
    node = HTMLNode(tag="p", value="hi", props=None)
    assert node.props_to_html() == ""

def test_props_to_html_empty_dict():
    node = HTMLNode(tag="p", value="hi", props={})
    assert node.props_to_html() == ""

def test_props_to_html_single_attr():
    node = HTMLNode(tag="a", value="Click", props={"href": "https://example.com"})
    assert node.props_to_html() == ' href="https://example.com"'

def test_props_to_html_multiple_attrs_ordered():
    # dict literals preserve insertion order in Python 3.7+
    node = HTMLNode(
        tag="a",
        value="Google",
        props={"href": "https://www.google.com", "target": "_blank"},
    )
    assert node.props_to_html() == ' href="https://www.google.com" target="_blank"'

def test_to_html_raises_not_implemented():
    node = HTMLNode(tag="div", children=[])
    with pytest.raises(NotImplementedError):
        node.to_html()