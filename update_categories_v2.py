import os
import re

POSTS_DIR = "/Users/mustafaaltayeb/myblog/_posts/Writeups"

def get_categories(filepath):
    filename = os.path.basename(filepath)
    lower_filename = filename.lower()
    
    if "HTB/" in filepath:
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
            return '[Writeups, PortSwigger, XSS]'
        return '[Writeups, PortSwigger, Misc]'
        
    if "RootMe/" in filepath:
        # Web Client:
        if "osi.md" in lower_filename or "commandinjection" in lower_filename:
            return '[Writeups, RootMe, "Web Client"]'
        if "javascript" in lower_filename or "jschallenges" in lower_filename or "obfescatation" in lower_filename or "obfuscation" in lower_filename:
            return '[Writeups, RootMe, "Web Client"]'
        # Web Server:
        return '[Writeups, RootMe, "Web Server"]'
        
    if "TryHackMe/" in filepath:
        windows_machines = ["hackpark", "alfred", "steelmountain", "relevant", "blue"]
        if any(win in lower_filename for win in windows_machines):
            return '[Writeups, TryHackMe, Windows]'
        return '[Writeups, TryHackMe, Linux]'
        
    if "OSCP/" in filepath:
        return '[Writeups, OSCP, "Week 1"]'
        
    return '[Writeups, CTF, Misc]'

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        return

    frontmatter = match.group(1)
    body = match.group(2)
    
    categories_str = get_categories(filepath)
    
    lines = frontmatter.split('\n')
    new_lines = []
    
    for line in lines:
        if line.startswith('categories: '):
            new_lines.append(f"categories: {categories_str}")
        elif line.startswith('category: '):
            new_lines.append(f"categories: {categories_str}")
        else:
            new_lines.append(line)

    if not any(l.startswith('categories:') for l in new_lines):
        new_lines.append(f"categories: {categories_str}")

    # Remove duplicates from new_lines if both category and categories existed
    final_lines = []
    seen_cat = False
    for l in new_lines:
        if l.startswith('categories: '):
            if not seen_cat:
                final_lines.append(l)
                seen_cat = True
        else:
            final_lines.append(l)

    new_content = "---\n" + "\n".join(final_lines) + "\n---\n" + body

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
