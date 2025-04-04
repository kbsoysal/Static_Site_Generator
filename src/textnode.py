from enum import Enum
import re

class TextType(Enum):
	TEXT = "TextType.TEXT"
	BOLD = "TextType.BOLD"
	ITALIC = "TextType.ITALIC"
	CODE = "TextType.CODE"
	LINK = "TextType.LINK"
	IMAGE = "TextType.IMAGE"

class TextNode:
	def __init__(self, text: str, text_type: TextType, url: str = None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, other):
		if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
			return True
	def __repr__(self):
		if self.url is None:
			return f"TextNode({self.text}, {self.text_type.value})"
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
def split_nodes_delimiter(old_nodes, delimiter, text_type):
	new_nodes = []
	for old_node in old_nodes:
		splitText = old_node.text.split(delimiter)
		for i,text in enumerate(splitText):
			if text != "":
				if i%2==0:
					new_nodes.append(TextNode(text, old_node.text_type))
				else:
					new_nodes.append(TextNode(text, text_type))
	return new_nodes

def extract_markdown_images(text):
	images = re.findall(r'!\[(.*?)\]\((.*?)\)', text)
	return images
def extract_markdown_links(text):
	links = re.findall(r'\[(.*?)\]\((.*?)\)', text)
	return links

def split_nodes_image(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		images = extract_markdown_images(old_node.text)
		for image in images:
			image_alt = image[0]
			image_link = image[1]
			image_html = f"![{image_alt}]({image_link})"
			sections = old_node.text.split(image_html)
			while len(sections) > 1:
				section = sections[0]
				if section != "":
					new_nodes.append(TextNode(section, old_node.text_type))
					old_node.text = old_node.text[len(section):]
				sections = sections[1:]
				new_nodes.append(TextNode(image_alt,TextType.IMAGE, image_link))
				old_node.text = old_node.text[len(image_html):]
		if len(images) == 0:
			new_nodes.append(old_node)
		else:
			if sections[0]!='':
				new_nodes.append(TextNode(sections[0], old_node.text_type))
	return new_nodes

def split_nodes_link(old_nodes):
	new_nodes = []
	for old_node in old_nodes:
		links = extract_markdown_links(old_node.text)
		for link in links:
			link_text = link[0]
			link_url = link[1]
			link_html = f"[{link_text}]({link_url})"
			sections = old_node.text.split(link_html, 1)
			while len(sections) > 1:
				section = sections[0]
				if section != "":
					new_nodes.append(TextNode(section, old_node.text_type))
					old_node.text = old_node.text[len(section):]
				sections = sections[1:]
				new_nodes.append(TextNode(link_text,TextType.LINK, link_url))
				old_node.text = old_node.text[len(link_html):]
		if len(links) == 0:
			new_nodes.append(old_node)
		else:
			if sections[0]!='':
				new_nodes.append(TextNode(sections[0], old_node.text_type))
	return new_nodes

def text_to_textnodes(text):
	node = TextNode(text, TextType.TEXT)
	text_nodes = []
	text_nodes = split_nodes_delimiter([node], '**', TextType.BOLD)
	text_nodes = split_nodes_delimiter(text_nodes, '_', TextType.ITALIC)
	text_nodes = split_nodes_delimiter(text_nodes, '`', TextType.CODE)
	text_nodes = split_nodes_image(text_nodes)
	text_nodes = split_nodes_link(text_nodes)
	
	if len(text_nodes) == 0:
		text_nodes.append(node)
	return text_nodes