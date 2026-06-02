import os
import re

POSTS_DIR = "/Users/mustafaaltayeb/myblog/_posts/Writeups"

# Logic based on filenames and directories
def get_categories(filepath):
    filename = os.path.basename(filepath)
    lower_filename = filename.lower()
    
    # Check directory path for platform
    if "HTB/" in filepath:
        if "conversor" in lower_filename or "expressway" in lower_filename:
            return '[Writeups, CTF, Misc]'
        return '[Writeups, HackTheBox, Linux]'
        
    if "Infinity/" in filepath:
        return '[Writeups, Infinity, "SQL Injection"]'
        
    if "PortSwigger/" in filepath:
        if "fileupload" in lower_filename:
            return '[Writeups, PortSwigger, "File Upload"]'
        if "nosql" in lower_filename:
            return '[Writeups, PortSwigger, "NoSQL Injection"]'
        if "commandinjection" in lower_filename:
            return '[Writeups, PortSwigger, "OS Command Injection"]'
        if "all-labs" in lower_filename or "pathraversal" in lower_filename:
            return '[Writeups, PortSwigger, "Path Traversal"]'
        if "crosssitescript" in lower_filename:
            return '[Writeups, PortSwigger, "Cross-Site Scripting"]'
        return '[Writeups, PortSwigger, Misc]'
        
    if "RootMe/" in filepath:
        if "osi.md" in lower_filename or "commandinjection" in lower_filename:
            return '[Writeups, RootMe, "Command Injection"]'
        if "nosqlinjection" in lower_filename:
            return '[Writeups, RootMe, "NoSQL Injection"]'
        if "sqli.md" in lower_filename:
            return '[Writeups, RootMe, "SQL Injection"]'
        if "javascript" in lower_filename or "jschallenges" in lower_filename or "obfescatation" in lower_filename or "obfuscation" in lower_filename:
            return '[Writeups, RootMe, JavaScript]'
        if "insecure_code_management" in lower_filename:
            return '[Writeups, RootMe, "Code Analysis"]'
        return '[Writeups, RootMe, "Web Security"]'
        
    if "TryHackMe/" in filepath:
        return '[Writeups, TryHackMe, Linux]'
        
    if "OSCP/" in filepath:
        return '[Writeups, OSCP, Review]'
        
    return '[Writeups, CTF, Misc]'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # match frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return

    frontmatter = match.group(1)
    body = match.group(2)
    
    categories_str = get_categories(filepath)
    
    # We want to replace `category: Writeups` with `categories: [...]`
    # or if `categories: ` already exists, replace it.
    lines = frontmatter.split('\n')
    new_lines = []
    
    for line in lines:
        if line.startswith('category: '):
            new_lines.append(f"categories: {categories_str}")
        elif line.startswith('categories: '):
            pass # skip existing to avoid duplicates if re-running
        else:
            new_lines.append(line)
            
    # if we didn't add it (e.g. didn't find `category:`), add it
    if not any(l.startswith('categories:') for l in new_lines):
        new_lines.append(f"categories: {categories_str}")

    new_content = "---\n" + "\n".join(new_lines) + "\n---\n" + body

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    for root, dirs, files in os.walk(POSTS_DIR):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                process_file(filepath)
                print(f"Updated: {file} -> {get_categories(filepath)}")

if __name__ == "__main__":
    main()
