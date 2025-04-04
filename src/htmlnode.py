
class HTMLNode:
    def __init__(self,tag=None, value=None, children=None, props=None):
        self.tag = tag  # "p", "a","h1"..
        self.value = value # text content
        self.children = children 
        self.props = props
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)  

    def to_html(self):
        raise NotImplementedError("Subclasses should implement this method")
    
    def props_to_html(self):
        if self.props is None:
            return ''
        keys = list(self.props.keys())
        values = list(self.props.values())
        str = ""
        for i in range(len(keys)):
            str += f'{keys[i]}="{values[i]}"'
        
        return str
    
    def __repr__(self):
         if self.props is None:
            return f'HTMLNode({self.tag}, {self.value}, {self.children}, None)'
         return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})'
    
class LeafNode(HTMLNode): #no children
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError("value of LeafNode cannot be None")
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode): #has children
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("tag of ParentNode cannot be None")
        if self.children is None:
            raise ValueError("children of ParentNode cannot be None")
        
        children_html = ''.join([child.to_html() for child in self.children])
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'