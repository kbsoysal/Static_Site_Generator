import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode('p','text123',None,None)
        node2 = HTMLNode('p','text123',None,None)
        self.assertEqual(node, node2)
    def test_repr(self):
        node = HTMLNode('p','text123',None,None)
        node2 = HTMLNode('a', 'click here', None, 
                                  {'href': 'https://google.com'})
        self.assertEqual(repr(node),'HTMLNode(p, text123, None, None)')
        self.assertEqual(repr(node2), 'HTMLNode(a, click here, None, href="https://google.com")')
    def test_repr_different(self):
        node = HTMLNode('p','text123',None,None)
        node2 = HTMLNode('a', 'click here', None, 
                                  {'href': 'https://google.com'})
        self.assertNotEqual(repr(node), repr(node2))
    
if __name__ == "__main__":
    unittest.main()
