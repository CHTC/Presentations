import glob

# Glob all files with .yml, rename tthem to .md and add three colons inbetween them

import os
import yaml
import re
import sys

def convert_yml_to_md():
    yml_files = glob.glob('*.yml')
    if not yml_files:
        print("No .yml files found in the current directory.")
        return

    for yml_file in yml_files:
        data = None
        with open(yml_file, 'r', encoding='utf-8') as file:
            data = file.read()
        data = "---\n" + data.strip() + "\n---\n"

        md_filename = re.sub(r'\.yml$', '.md', yml_file)
        with open(md_filename, 'w', encoding='utf-8') as md_file:
            md_file.write(data)

        print(f"Converted {yml_file} to {md_filename}")

    # now delete all yml files
    for yml_file in yml_files:
        os.remove(yml_file)
        print(f"Deleted {yml_file}")

if __name__ == "__main__":
    convert_yml_to_md()
    print("Conversion completed.")