#!/usr/bin/python3

import os
import sys
from ruamel.yaml import YAML

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 fix_image_url.py <path>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.indent(mapping=2, sequence=4, offset=2)

    suf = {
        "01": "a",
        "02": "a",
        "03": "a",
        "04": "a",
        "05": "a",
        "06": "a",
        "07": "a",
        "08": "a",
        "09": "a",
        "10": "a",
        "11": "a",
        "12": "a",
    }

    suf_conf = {}
    
    for filename in os.listdir(path):
        if filename.endswith(".md"):
            filepath = os.path.join(path, filename)
            with open(filepath, "r+") as f:
                content = f.read()
                front_matter = ""
                if content.startswith("---"):
                    _, front_matter, content = content.split("---\n", 2)
                
                data = yaml.load(front_matter)

                post_date = str(data.get("date", ""))
                title = data.get("title", "")
                year = post_date[:4]
                if year not in suf_conf:
                    suf_conf[year] = suf.copy()
                month = post_date[5:7]
                month_suf = suf_conf[year][month]
                suf_conf[year][month] = chr(ord(month_suf) + 1)

                print(post_date)

                data["permalink"] = filename.replace(".md", "/")
                f.seek(0)
                f.write("---\n")
                yaml.dump(data, f)
                f.write("---\n")
                f.write(content)
                f.truncate()

                new_filename = f"{month}{month_suf}-{title}.md"
                print(new_filename)
                new_filepath = os.path.join(path, post_date[:4], new_filename)
                os.makedirs(os.path.dirname(new_filepath), exist_ok=True)
                os.rename(filepath, new_filepath)
