import os
import shutil

from generate_html import generate_page, generate_pages_recursive


def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    copy_directory("static", "public")
    generate_pages_recursive("content", "template.html", "public")


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
