import textnode
import htmlnode

def text_node_to_html_node(text_node):
    if text_node.text_type == textnode.TextType.TEXT:
        return htmlnode.LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == textnode.TextType.BOLD:
        return htmlnode.LeafNode(tag='b' , value=text_node.text)
    elif text_node.text_type == textnode.TextType.ITALIC:
        return htmlnode.LeafNode(tag='i', value=text_node.text)
    elif text_node.text_type == textnode.TextType.CODE:
        return htmlnode.LeafNode(tag='code', value=text_node.text)
    elif text_node.text_type == textnode.TextType.LINK:
        return htmlnode.LeafNode(tag='a', value=text_node.text, 
                                 props={'href': text_node.url})
    elif text_node.text_type == textnode.TextType.IMAGE:
        return htmlnode.LeafNode(tag='img', value='', props={'src': text_node.url,
                                                              'alt': text_node.text})
    else:
        raise Exception("Unknown text node type")
    
def markdown_to_blocks(markdown):
    delimiter = '\n\n'
    blocks = markdown.split(delimiter)
    for i, block in enumerate(blocks):
         lines = block.split('\n')
         lines = [line.strip() for line in lines]
         block=''
         for line in lines:
             block += line +'\n'
         blocks[i]=block
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block]
    return blocks
