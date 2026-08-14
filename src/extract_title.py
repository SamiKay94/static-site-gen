def extract_title(markdown):
    split_text = markdown.split("\n")
    found_line = None
    for line in split_text:
        if line.startswith("# "):
            found_line = line
            break

    if found_line is None:
        raise Exception("no title found")

    return found_line.replace("# ", "")
