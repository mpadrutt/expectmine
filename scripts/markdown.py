import os
import re
from pathlib import Path

"""
DISCLAIMER: 
    In this script, base path means root of project.
    This also counts for the tmpl files.
"""

README_PATH = Path("README.md")
TEMPLATE_PATH = Path("scripts/markdown/readme.tmpl.md")

INCLUDE_RE = re.compile(r"!\[\[(.*\.md)]]")

ALIAS_DICT = {"@docs": "docs/source/markdown", "@code": "expectmine"}


def process_markdown():
    with open(TEMPLATE_PATH, "r") as template:
        lines = template.readlines()

    for i, line in enumerate(lines):
        match = re.search(INCLUDE_RE, line)

        if not match:
            continue

        included_file_path = match.group(1)

        for alias, replacement in ALIAS_DICT.items():
            included_file_path = included_file_path.replace(alias, replacement)

        included_file_path = Path(included_file_path)

        if not included_file_path.is_file():
            lines.pop(i)
            continue

        with open(included_file_path, "r") as temp_file:
            temp_lines = temp_file.readlines()

        link_pattern = r"\[(.*?)\]\(([^)]+)\)"

        for j, temp_line in enumerate(temp_lines):
            if temp_line.startswith("#"):
                temp_lines[j] = "#" + temp_lines[j]

            temp_match = re.search(link_pattern, temp_line)

            if not temp_match:
                continue

            temp_match = temp_match.group(2)

            full_path = Path(os.path.normpath(included_file_path.parent / temp_match))

            if full_path.is_file():
                temp_lines[j] = temp_line.replace(temp_match, str(full_path))

        lines[i] = "".join(temp_lines)

    lines.append("\n")

    with open(README_PATH, "w") as md:
        md.writelines(lines)
