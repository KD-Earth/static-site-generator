import re

from htmlnode import LeafNode

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str):
    result = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            result.append(node)
            continue

        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        
        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(section, node.text_type))
            else:
                result.append(TextNode(section, text_type))
    
    return result

def extract_markdown_images(text: str) -> list[tuple[str,str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str) -> list[tuple[str,str]]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes: list[TextNode]):
    result = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            result.append(node)
            continue

        matches = extract_markdown_images(node.text)        
        text_to_split = node.text

        for image_alt_text, url in matches:
            sections = text_to_split.split(f"![{image_alt_text}]({url})", 1)
            if(len(sections) != 2):
                raise ValueError("Invalid markdown, image section not closed")

            [section, text_to_split] = sections
            if section != "":
                result.append(TextNode(section, text_type_text))
            result.append(TextNode(image_alt_text, text_type_image, url))
        
        if text_to_split != "":
            result.append(TextNode(text_to_split, text_type_text))
    return result

def split_nodes_link(old_nodes: list[TextNode]):
    result = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            result.append(node)
            continue

        matches = extract_markdown_links(node.text)        
        text_to_split = node.text

        for anchor_text, url in matches:
            sections = text_to_split.split(f"[{anchor_text}]({url})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            
            [section, text_to_split] = sections
            if section != "":
                result.append(TextNode(section, text_type_text))
            result.append(TextNode(anchor_text, text_type_link, url))
        
        if text_to_split != "":
            result.append(TextNode(text_to_split, text_type_text))
    return result

def text_to_textnodes(text: str):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)    
    return nodes