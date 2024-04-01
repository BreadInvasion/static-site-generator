import re
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode
from extract import extract_markdown_images, extract_markdown_links


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    supported_types = {
        "text": None,
        "bold": "b",
        "italic": "i",
        "code": "code",
        "link": "a",
        "image": "img",
    }

    if text_node.text_type not in supported_types:
        raise ValueError(f'TextNode text_type "{text_node.text_type}" is not supported')

    output_node = LeafNode(text_node.text, supported_types[text_node.text_type], {})

    # Special cases
    if output_node.tag == "img":
        output_node.value = ""
        output_node.props["src"] = text_node.url
        output_node.props["alt"] = text_node.text
    elif output_node.tag == "a":
        output_node.props["href"] = text_node.url

    return output_node


def split_nodes_delimiter(
    old_nodes: list[TextNode | HTMLNode], delimiter: str, text_type: str
):
    output = []
    for node in old_nodes:
        if type(node) != TextNode:
            output.append(node)
            continue

        if node.text_type != "text" or not node.text:
            output.append(node)
            continue

        split_text = node.text.split(delimiter)
        in_delim = False  # Flip this as we step through the list, to indicate whether we're inside the bounds of a delimiter pair

        for i in range(len(split_text) - 1):
            if len(split_text[i]) == 0:
                in_delim = not in_delim
                continue

            output.append(
                TextNode(split_text[i], text_type if in_delim else node.text_type)
            )
            in_delim = not in_delim
        if in_delim:
            raise ValueError("All delimiters must be closed")
        if split_text[-1]:
            output.append(TextNode(split_text[-1], node.text_type))

    return output


def split_nodes_image(old_nodes: list[TextNode | HTMLNode]):
    output = []
    for node in old_nodes:
        if type(node) != TextNode or node.text_type != "text" or not node.text:
            output.append(node)
            continue

        images = extract_markdown_images(node.text)
        text = node.text
        for image in images:
            text_split = text.split(f"![{image[0]}]({image[1]})", 1)
            if text_split[0]:
                output.append(TextNode(text_split[0], node.text_type))
            output.append(TextNode(image[0], "image", image[1]))
            text = text_split[1]
        if text:
            output.append(TextNode(text, node.text_type))
    return output


def split_nodes_link(old_nodes: list[TextNode | HTMLNode]):
    output = []
    for node in old_nodes:
        if type(node) != TextNode or node.text_type != "text" or not node.text:
            output.append(node)
            continue

        links = extract_markdown_links(node.text)
        text = node.text
        for link in links:
            text_split = text.split(f"[{link[0]}]({link[1]})", 1)
            if text_split[0]:
                output.append(TextNode(text_split[0], node.text_type))
            output.append(TextNode(link[0], "link", link[1]))
            text = text_split[1]
        if text:
            output.append(TextNode(text, node.text_type))
    return output


def text_to_textnodes(text: str) -> list[TextNode]:
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([TextNode(text, "text")], "`", "code"),
                    "**",
                    "bold",
                ),
                "*",
                "italic",
            )
        )
    )


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block.strip() != ""]


def block_to_block_type(block: str):
    if re.match(r"^[#]{1,6} ", block):
        return "heading"
    if len(block) >= 6 and block[:3] == "```" and block[-3:] == "```":
        return "code"
    if all(map(lambda x: x[0] == ">", block.split("\n"))):
        return "quote"
    if all(map(lambda x: x[0:2] in ["* ", "- "], block.split("\n"))):
        return "unordered_list"

    i = 1
    for line in block.split("\n"):
        if not line.startswith(f"{i}. "):
            return "paragraph"
        i += 1
    return "ordered_list"


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        match block_to_block_type(block):
            case "heading":
                content = block.lstrip("#").lstrip(
                    " "
                )  # Don't combine, because using # again after the first space is valid
                size = block.index(" ")
                node = ParentNode(
                    f"h{size}",
                    map(text_node_to_html_node, text_to_textnodes(content)),
                    {},
                )
                children.append(node)
            case "quote":
                content = "\n".join(map(lambda x: x[1:].strip(), block.split("\n")))
                node = ParentNode(
                    "blockquote",
                    map(text_node_to_html_node, text_to_textnodes(content)),
                    {},
                )
                children.append(node)
            case "code":
                content = block[3:-3].strip()
                node = ParentNode(
                    "pre", [LeafNode(tag="code", value=content, props={})], {}
                )
                children.append(node)
            case "unordered_list":
                content = [line[1:].lstrip() for line in block.split("\n")]
                node = ParentNode(
                    "ul",
                    [
                        ParentNode(
                            "li", map(text_node_to_html_node, text_to_textnodes(line))
                        )
                        for line in content
                    ],
                    {},
                )
                children.append(node)
            case "ordered_list":
                content = [line[2:].lstrip() for line in block.split("\n")]
                node = ParentNode(
                    "ol",
                    [
                        ParentNode(
                            "li", map(text_node_to_html_node, text_to_textnodes(line))
                        )
                        for line in content
                    ],
                    {},
                )
                children.append(node)
            case "paragraph":
                node = ParentNode(
                    "p", map(text_node_to_html_node, text_to_textnodes(block)), {}
                )
                children.append(node)
    return ParentNode("div", children, {})
