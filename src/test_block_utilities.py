import unittest

from block_md_utilities import (
    markdown_to_blocks,
    block_to_block_type,
)

class TestBlockMarkdown(unittest.TestCase):
    def test_md_to_blocks(self):
        markdown = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item'''
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ],
            blocks,
        )
    
    def test_block_to_block_type_heading(self):
        block_type = block_to_block_type("Heading")
        self.assertEqual(block_type, "paragraph")

        block_type = block_to_block_type("#Heading")
        self.assertEqual(block_type, "paragraph")

        block_type = block_to_block_type("# Heading")
        self.assertEqual(block_type, "heading")

        block_type = block_to_block_type("## Heading")
        self.assertEqual(block_type, "heading")

        block_type = block_to_block_type("### Heading")
        self.assertEqual(block_type, "heading")

        block_type = block_to_block_type("#### Heading")
        self.assertEqual(block_type, "heading")

        block_type = block_to_block_type("##### Heading")
        self.assertEqual(block_type, "heading")

        block_type = block_to_block_type("###### Heading")
        self.assertEqual(block_type, "heading")

        block_type = block_to_block_type("####### Heading")
        self.assertEqual(block_type, "paragraph")
        
    def test_block_to_block_type_code(self):
        block_type = block_to_block_type("```Code```")
        self.assertEqual(block_type, "code")
        
        block_type = block_to_block_type("``Code``")
        self.assertEqual(block_type, "paragraph")

        block_type = block_to_block_type("``````Code``````")
        self.assertEqual(block_type, "code")

    def test_block_to_block_type_quote(self):
        block_type = block_to_block_type(">quote")
        self.assertEqual(block_type, "quote")
        
        block_type = block_to_block_type(">Line 1\n>Line 2")
        self.assertEqual(block_type, "quote")

        block_type = block_to_block_type(">Line 1\nLine 2")
        self.assertEqual(block_type, "paragraph")

    def test_block_to_block_type_unordered_list(self):
        block_type = block_to_block_type("*item")
        self.assertEqual(block_type, "unordered_list")
        
        block_type = block_to_block_type("-item")
        self.assertEqual(block_type, "unordered_list")
        
        block_type = block_to_block_type("-item 1\n-item 2")
        self.assertEqual(block_type, "unordered_list")
        
        block_type = block_to_block_type("-item 1\n*item 2")
        self.assertEqual(block_type, "unordered_list")
        
        block_type = block_to_block_type("-item 1\nitem 2")
        self.assertEqual(block_type, "paragraph")

        block_type = block_to_block_type("an-item")
        self.assertEqual(block_type, "paragraph")
        
    def test_block_to_block_type_ordered_list(self):
        block_type = block_to_block_type("1.item")
        self.assertEqual(block_type, "paragraph")

        block_type = block_to_block_type("test 1.item")
        self.assertEqual(block_type, "paragraph")
        
        block_type = block_to_block_type("1. item")
        self.assertEqual(block_type, "ordered_list")

        block_type = block_to_block_type("1. item\n2. item 2\n3. item 3")
        self.assertEqual(block_type, "ordered_list")

        block_type = block_to_block_type("1. item\n3. item 2\n2. item 3")
        self.assertEqual(block_type, "paragraph")



if __name__ == "__main__":
    unittest.main()