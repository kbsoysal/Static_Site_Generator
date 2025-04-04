
from textnode import TextNode, TextType
from functions import *
import unittest

class Testfunction(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_markdown_to_blocks(self):
        
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item

"""
        
        blocks = markdown_to_blocks(md)
        #print(md)
        #print(blocks)
        self.assertEqual(
            blocks,
            ["# This is a heading",
             "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
             "- This is the first list item in a list block\n- This is a list item\n- This is another list item"])


        '''[
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )'''


if __name__ == "__main__":
    
    unittest.main()