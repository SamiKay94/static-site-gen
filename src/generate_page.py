import os

from block_markdown import markdown_to_html_node
from extract_title import extract_title


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    html_str: str
    page_title: str
    with open(from_path, "r") as file:
        content = file.read()

        if content is None:
            raise Exception("no content possible")

        html_str = markdown_to_html_node(content).to_html()
        page_title = extract_title(content)
    file.close()

    template_content: str
    full: str

    with open(template_path, "r") as template:
        template_content = template.read()

        full = template_content.replace("{{ Title }}", page_title).replace("{{ Content }}", html_str)
    template.close()

    folders = os.path.dirname(dest_path)

    if not os.path.isdir(folders):
        os.makedirs(folders, exist_ok=True)

    with open(os.path.join(dest_path), "w") as html:
        html.write(full)
    html.close()
