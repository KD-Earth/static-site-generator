import re

from htmlnode import HTMLNode

def markdown_to_blocks(markdown: str):
    blocks = markdown.strip().split("\n\n")
    blocks = filter(lambda x: x != "", blocks)
    blocks = map(lambda x: x[1:] if x.startswith("\n") else x, blocks)
    return list(blocks)

def block_to_block_type(markdown: str) -> str:
    # check for headings
    matches = re.findall(r"^(#{1,6} )", markdown)
    if len(matches) == 1:
        return "heading"
    
    # check for code
    matches = re.findall(r"(```)(.*)(```)", markdown)
    if len(matches) == 1:
        return "code"
    
    lines = markdown.split("\n")

    # check for quote
    if sum(line.startswith(">") for line in lines) == len(lines):
        return "quote"
    
    # check for unordered list
    if sum(re.match(r"^(\*|-)", line) is not None for line in lines) == len(lines):
        return "unordered_list"
    
    # check for ordered list
    count = 0
    for i, line in enumerate(lines):
        match = re.match(r"^\d\. ", line)
        if match is not None and int(match[0][0]) == i + 1:
            count += 1
    
    if count == len(lines):
        return "ordered_list"

    # default
    return "paragraph"

def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == "heading":
            pass
        if block_type == "code":
            pass
        if block_type == "quote":
            pass
        if block_type == "unordered_list":
            pass
        if block_type == "ordered_list":
            pass  
        if block_type == "paragraph":
            pass