import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?:^|[^!])\[(.*?)\]\((.*?)\)", text)


def extract_title(markdown: str):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[1:].lstrip()
