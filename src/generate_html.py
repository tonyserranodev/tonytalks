import os
import pathlib
from markdown_to_html import markdown_to_html_node


def extract_title(markdown: str) -> str:
    if not markdown.strip().startswith("# "):
        raise Exception("All markdown titles must start with: # ")
    return markdown.strip().strip("# ")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, "r") as f:
            markdown = f.read()
        with open(template_path, "r") as f:
            template = f.read()
    except FileNotFoundError as e:
        print(e)
        return

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown.strip("\n").split("\n")[0])
    new_html = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    try:
        with open(dest_path, "w") as f:
            f.write(new_html)
    except FileNotFoundError as e:
        print(e)
        return


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        print(f"dir_path_content: {dir_path_content}")
        if os.path.isfile(os.path.join(dir_path_content, item)):
            generate_page(
                os.path.join(dir_path_content, item),
                template_path,
                os.path.join(dest_dir_path, item.replace(".md", ".html")),
            )
        else:
            generate_pages_recursive(
                os.path.join(dir_path_content, item),
                template_path,
                os.path.join(dest_dir_path, item),
            )
