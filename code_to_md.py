import os
import sys
import re

# Define the ignore lists
ignore_dirs = {'node_modules', 'fonts', '.git', 'images'}
ignore_files = {'package-lock.json', 'database.db'}

# Get the script's directory and folder name
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
folder_name = os.path.basename(script_dir)

# Get the output filename
output_file = 'output.md'

# Add the script and output file to the ignore list
script_name = os.path.basename(sys.argv[0])
ignore_files.update({script_name, output_file})

# Mapping of file extensions to language identifiers
language_extensions = {
    '.py': 'python',
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.html': 'html',
    '.css': 'css',
    '.java': 'java',
    '.c': 'c',
    '.cpp': 'cpp',
    '.cs': 'csharp',
    '.rb': 'ruby',
    '.go': 'go',
    '.php': 'php',
    '.rs': 'rust',
    '.json': 'json',
    '.xml': 'xml',
    '.sh': 'bash',
    '.bat': 'batch',
    '.md': 'markdown',
    '.yml': 'yaml',
    '.yaml': 'yaml',
    # Add more extensions and languages as needed
}

# Initialize stats counters
total_lines = 0
total_characters = 0
total_words = 0
total_files = 0
folders_set = set()

# Function to create a nested dictionary representing the directory tree
def insert_into_tree(tree, path_parts, file_name):
    if not path_parts:
        return
    first = path_parts[0]
    if first not in tree:
        tree[first] = {}
    if len(path_parts) == 1:
        tree[first][file_name] = None
    else:
        insert_into_tree(tree[first], path_parts[1:], file_name)

# Function to generate the markdown index from the directory tree
def generate_index(tree, parent_path=''):
    index_lines = []
    for key in sorted(tree.keys()):
        current_path = os.path.join(parent_path, key).replace('\\', '/')
        if tree[key] is None:
            # It's a file
            anchor = generate_anchor(current_path)
            index_lines.append(f'- 📄 [{key}](#{anchor})')
        else:
            # It's a directory
            index_lines.append(f'- 📁 **{key}**')
            sub_lines = generate_index(tree[key], current_path)
            sub_lines = ['  ' + line for line in sub_lines]
            index_lines.extend(sub_lines)
    return index_lines

# Function to generate a valid anchor from a file path
def generate_anchor(path):
    # Replace spaces with hyphens and remove invalid characters
    anchor = re.sub(r'[\s/\\]+', '-', path)
    anchor = re.sub(r'[^a-zA-Z0-9\-_]', '', anchor)
    anchor = anchor.lower()
    return anchor

# Build the directory tree
directory_tree = {}
file_list = []

for root, dirs, files in os.walk('.', topdown=True):
    # Exclude ignored directories
    dirs[:] = [d for d in dirs if d not in ignore_dirs]

    # Add the root to folders_set if it's not '.'
    if root != '.':
        relative_root = os.path.relpath(root, '.')
        folders_set.add(relative_root)
    
    for file in files:
        if file in ignore_files:
            continue

        total_files += 1  # Increment total files

        file_path = os.path.join(root, file)
        relative_path = os.path.relpath(file_path, '.')
        path_parts = os.path.normpath(relative_path).split(os.sep)[:-1]
        insert_into_tree(directory_tree, path_parts, file)
        file_list.append((relative_path, file_path))

# Generate the index
index_lines = generate_index(directory_tree)

# Initialize output content
output_content = []

# Process files to collect stats and build output content
for relative_path, file_path in file_list:
    # Generate anchor for the heading
    anchor = generate_anchor(relative_path)
    # Write a heading with the file path and name, including the anchor
    output_content.append(f'# {relative_path} <a id="{anchor}"></a>\n\n')

    # Determine the language based on the file extension
    _, ext = os.path.splitext(file_path)
    language = language_extensions.get(ext.lower(), '')

    # Start the code block
    output_content.append(f'```{language}\n')

    # Read and write the file contents, and collect stats
    try:
        with open(file_path, 'r', encoding='utf-8') as infile:
            contents = infile.read()
            output_content.append(contents)
            # Update stats
            total_characters += len(contents)
            total_lines += contents.count('\n') + 1  # Add 1 if the file doesn't end with a newline
            total_words += len(contents.split())
    except (UnicodeDecodeError, PermissionError) as e:
        print(f"Skipping file {file_path}: {e}")
        output_content.append(f"<!-- Skipping file {relative_path}: {e} -->\n")

    # End the code block
    output_content.append('\n```\n\n')

# Compute total folders
total_folders = len(folders_set)

# Write to the output file
with open(output_file, 'w', encoding='utf-8') as outfile:
    # Write the folder name as the top title
    outfile.write(f'# {folder_name}\n\n')

    # Write the stats
    outfile.write('## Project Statistics\n\n')
    outfile.write(f'- **Number of files:** {total_files}\n')
    outfile.write(f'- **Number of folders:** {total_folders}\n')
    outfile.write(f'- **Total lines:** {total_lines}\n')
    outfile.write(f'- **Total characters:** {total_characters}\n')
    outfile.write(f'- **Total words:** {total_words}\n\n')

    # Write the index
    outfile.write('## Index\n\n')
    outfile.write('\n'.join(index_lines))
    outfile.write('\n\n---\n\n')

    # Write the file contents
    outfile.write(''.join(output_content))
