import unittest

from textnode import *


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), repr(node2))
    def test_repr_different(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(repr(node), repr(node2))
    def test_eq_different(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected_nodes = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT)]
        
        self.assertEqual(new_nodes, expected_nodes)

        node = TextNode("This is text with a **some formatted** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

        expected_nodes = [
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("some formatted", TextType.BOLD),
    TextNode(" word", TextType.TEXT)]
        
        self.assertEqual(new_nodes, expected_nodes)

        node = TextNode("`code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected_nodes = [
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT)]
        
        self.assertEqual(new_nodes, expected_nodes)

        node = TextNode("`code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected_nodes = [
    TextNode("code block", TextType.CODE)]
        
        self.assertEqual(new_nodes, expected_nodes)

        node = TextNode("`code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected_nodes = [
    TextNode("code block", TextType.CODE)]
        
        self.assertEqual(new_nodes, expected_nodes)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        #print(matches)
        self.assertEqual(matches,[("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        #print(links)
        self.assertEqual(links,[("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
        new_nodes =[]
        expected_new_nodes =[]

        new_nodes.append(split_nodes_image([node]))
        expected_new_nodes.append([
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ])
        node = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
        new_nodes.append(split_nodes_image([node]))
        expected_new_nodes.append([
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ])
        node = TextNode(
        "![second image](https://i.imgur.com/3elNhQu.png)123",
        TextType.TEXT,
    )
        new_nodes.append(split_nodes_image([node]))
        expected_new_nodes.append([
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
            TextNode("123", TextType.TEXT),
        ])
        node = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/zjjcJKZ.png)![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
    )
        new_nodes.append(split_nodes_image([node]))
        expected_new_nodes.append([
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
              
        ])



        for i in range(0, len(new_nodes)):
            new_node= new_nodes[i]
            expected_new_node= expected_new_nodes[i]
            self.assertListEqual(new_node, expected_new_node)
    
    def test_text_to_textnodes(self):
        text = 'This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)123**11**123'
        nodes = text_to_textnodes(text)
        expected = [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
    TextNode("123", TextType.TEXT),
    TextNode("11", TextType.BOLD),
    TextNode("123", TextType.TEXT),
    ]
        self.assertEqual(nodes, expected)

if __name__ == "__main__":
    unittest.main()
