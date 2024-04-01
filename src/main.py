from shutil import copytree, rmtree
from os import mkdir
from os.path import exists

from generate_page import generate_pages_recursive


def main():
    if exists("./public"):
        rmtree("./public")
    if not exists("./static"):
        raise Exception("static folder not found")
    copytree("./static", "./public")
    generate_pages_recursive("./content", "template.html", "./public")


if __name__ == "__main__":
    main()
