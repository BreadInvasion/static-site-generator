from pathlib import Path
from convert import markdown_to_html_node
from extract import extract_title
from os.path import exists, isfile, join
from os import listdir


def generate_page(from_path, template_path, destination_path):
    print(
        f"Generating page from {from_path} to {destination_path} using {template_path}."
    )
    markdown = None
    template = None
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)

    path = Path(destination_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(destination_path, "w") as f:
        f.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in listdir(dir_path_content):
        from_path = Path(join(dir_path_content, entry))
        to_path = Path(join(dest_dir_path, entry))
        if isfile(from_path) and len(entry) > 3 and entry[-3:] == ".md":
            to_path = Path(join(dest_dir_path, entry[:-2] + "html"))
            generate_page(from_path, template_path, to_path)
        else:
            generate_pages_recursive(from_path, template_path, to_path)
