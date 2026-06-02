import os
import re

for root, _, files in os.walk('_posts/Writeups/TryHackMe'):
    for f in files:
        if f.endswith('.md'):
            with open(os.path.join(root, f), 'r') as file:
                content = file.read()
                tags = re.search(r'tags:\n(.*?)(?:\n\w+|$)', content, re.DOTALL)
                if tags:
                    print(f"{f}:")
                    print(tags.group(1).strip())
