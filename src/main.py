import textnode


def main():
    tnode = textnode.TextNode("anchor text", textnode.TextType.LINK, "https://example.com")
    print(tnode)
    

if __name__ == "__main__":
    main()