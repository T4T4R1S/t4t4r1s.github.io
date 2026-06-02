import os
import re
import shutil

BASE_DIR = "/Users/mustafaaltayeb/myblog"
POSTS_DIR = os.path.join(BASE_DIR, "_posts")

MAPPINGS = {
    "HTB": "HTB",
    "TryHackMe": "TryHackMe",
    "RootMe": "RootMe",
    "PortSwiggerLabs": "PortSwigger",
    "Infinity": "Infinity",
    "OSCP_12W": "OSCP"
}


def process_file(filepath, platform_name, dest_dir):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        print(f"No frontmatter found in {filepath}")
        return

    frontmatter = match.group(1)
    body = match.group(2)

    lines = frontmatter.split('\n')
    new_lines = []
    
    title = ""
    date = ""
    tags = set()
    tags.add(platform_name) # Add platform as a tag

    # Extract info and filter out old categories/tags
    in_tags = False
    in_categories = False
    for line in lines:
        if line.startswith('title:'):
            title = line
            new_lines.append(line)
        elif line.startswith('date:'):
            date = line
            new_lines.append(line)
        elif line.startswith('layout:'):
            new_lines.append(line)
        elif line.startswith('tags:'):
            in_tags = True
            in_categories = False
            # check if it's inline like tags: [a, b]
            if '[' in line:
                t_str = line.split('[')[1].split(']')[0]
                for t in t_str.split(','):
                    if t.strip():
                        tags.add(t.strip().strip("'").strip('"'))
                in_tags = False
        elif line.startswith('categories:') or line.startswith('category:'):
            in_categories = True
            in_tags = False
            if '[' in line:
                in_categories = False
        elif line.startswith('- ') and in_tags:
            t = line.replace('- ', '').strip().strip("'").strip('"')
            if t:
                tags.add(t)
        elif line.startswith('- ') and in_categories:
            pass # ignore old categories
        elif line.startswith('author:'):
            pass # we will add it manually
        else:
            in_tags = False
            in_categories = False
            new_lines.append(line)

    # Reconstruct frontmatter
    final_fm = []
    if not any(l.startswith('layout:') for l in new_lines):
        final_fm.append("layout: post")
    else:
        final_fm.append([l for l in new_lines if l.startswith('layout:')][0])
        
    if title:
        final_fm.append(title)
        
    if date:
        final_fm.append(date)

    final_fm.append("category: Writeups")
    
    final_fm.append("tags:")
    for tag in sorted(tags):
        final_fm.append(f"  - {tag}")
        
    final_fm.append("author: mustafa_altayeb")
    
    # Add any remaining lines that we didn't handle specifically
    handled = ['layout:', 'title:', 'date:', 'category:', 'categories:', 'tags:', 'author:']
    for line in new_lines:
        if not any(line.startswith(h) for h in handled) and line.strip():
            final_fm.append(line)

    new_content = "---\n" + "\n".join(final_fm) + "\n---\n" + body

    filename = os.path.basename(filepath)
    dest_path = os.path.join(POSTS_DIR, "Writeups", dest_dir, filename)

    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    for src_dir, dest_dir in MAPPINGS.items():
        full_src_dir = os.path.join(POSTS_DIR, src_dir)
        if not os.path.exists(full_src_dir):
            continue
            
        for root, dirs, files in os.walk(full_src_dir):
            for file in files:
                if file.endswith('.md'):
                    filepath = os.path.join(root, file)
                    process_file(filepath, dest_dir, dest_dir)
                    os.remove(filepath) # Remove original file
                    
        # Remove empty directories after processing
        shutil.rmtree(full_src_dir, ignore_errors=True)
        print(f"Processed {src_dir} -> Writeups/{dest_dir}")

if __name__ == "__main__":
    main()
