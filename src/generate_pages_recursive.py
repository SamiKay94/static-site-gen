import os

from generate_page import generate_page


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for content in os.listdir(dir_path_content):
        print("Content", content)
        the_path = os.path.join(dir_path_content, content)
        dest_path = os.path.join(dest_dir_path, content)
        print("The Path", the_path)
        print("Dest Path", dest_path)
        if os.path.isdir(the_path):
            generate_pages_recursive(the_path, template_path, dest_path)

        if os.path.isfile(the_path) and the_path.endswith(".md"):
            generate_page(the_path, template_path, dest_path.replace(".md", ".html"))
