import os
import shutil
import sys

from generate_html import generate_pages_recursive


def main():
    basepath = sys.argv or "/"

    if os.path.exists("docs"):
        shutil.rmtree("docs")
    copy_directory("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


def copy_directory(source: str, destination: str) -> None:

    if not os.path.exists(destination):
        os.mkdir(destination)

    for item in os.listdir(source):
        source_item_path = os.path.join(source, item)
        destination_item_path = os.path.join(destination, item)
        if os.path.isdir(source_item_path):
            copy_directory(source_item_path, destination_item_path)
        else:
            shutil.copy(source_item_path, destination_item_path)
            print("item copied")


if __name__ == "__main__":
    main()
