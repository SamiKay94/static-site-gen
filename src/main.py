import os
import shutil

from copystatic import copy_files_recursive
from generate_page import generate_page
from generate_pages_recursive import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"


def main() -> None:
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    print("Generating page...")
    generate_pages_recursive("content", "template.html", "public")


main()
