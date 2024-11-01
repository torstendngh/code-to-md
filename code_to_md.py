import os
import sys
import re

# Define the ignore lists
IGNORE_DIRS = {'node_modules', 'fonts', '.git', 'images'}
IGNORE_FILES = {'package-lock.json', 'database.db'}

# Get the script's directory and folder name
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
folder_name = os.path.basename(script_dir)

# Get the output filename
OUTPUT_FILE = 'output.md'

# Add the script and output file to the ignore list
script_name = os.path.basename(sys.argv[0])
IGNORE_FILES.update({script_name, OUTPUT_FILE})

# Mapping of file extensions to language identifiers
LANGUAGE_EXTENSIONS = {
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

# Initialize output content and directory tree
output_content = []
directory_tree = {}

# Compile regex patterns outside functions for efficiency
anchor_pattern = re.compile(r'[\s/\\]+')
invalid_char_pattern = re.compile(r'[^a-zA-Z0-9\-_]')


def generate_anchor(path):
    """Generate a valid anchor from a file path."""
    anchor = anchor_pattern.sub('-', path)
    anchor = invalid_char_pattern.sub('', anchor)
    return anchor.lower()


def insert_into_tree(tree, path_parts):
    """Insert directories and files into the directory tree."""
    for part in path_parts:
        tree = tree.setdefault(part, {})


def generate_index(tree, parent_path=''):
    """Generate the markdown index from the directory tree."""
    index_lines = []
    for key in sorted(tree.keys()):
        current_path = os.path.join(parent_path, key).replace('\\', '/')
        if tree[key]:
            index_lines.append(f'- 📁 **{key}**')
            sub_lines = generate_index(tree[key], current_path)
            index_lines.extend(['  ' + line for line in sub_lines])
        else:
            anchor = generate_anchor(current_path)
            index_lines.append(f'- 📄 [{key}](#{anchor})')
    return index_lines


# Walk the directory and process files
for root, dirs, files in os.walk('.', topdown=True):
    # Exclude ignored directories
    dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]

    # Add the root to folders_set if it's not '.'
    relative_root = os.path.relpath(root, '.')
    if relative_root != '.':
        folders_set.add(relative_root)

    # Build path_parts for directory_tree
    path_parts = [] if relative_root == '.' else os.path.normpath(
        relative_root).split(os.sep)

    for file in files:
        if file in IGNORE_FILES:
            continue

        total_files += 1  # Increment total files

        file_path = os.path.join(root, file)
        relative_path = os.path.relpath(file_path, '.')
        file_parts = path_parts + [file]

        # Insert file into directory_tree
        insert_into_tree(directory_tree, file_parts)

        # Generate anchor for the heading
        anchor = generate_anchor(relative_path)
        # Write a heading with the file path and name, including the anchor
        output_content.append(f'# {relative_path} <a id="{anchor}"></a>\n\n')

        # Determine the language based on the file extension
        _, ext = os.path.splitext(file_path)
        language = LANGUAGE_EXTENSIONS.get(ext.lower(), '')

        # Start the code block
        output_content.append(f'```{language}\n')

        # Read and write the file contents, and collect stats
        try:
            with open(file_path, 'r', encoding='utf-8') as infile:
                contents = infile.read()
                output_content.append(contents)
                # Update stats
                total_characters += len(contents)
                total_lines += contents.count('\n')
                total_words += len(contents.split())
        except (UnicodeDecodeError, PermissionError) as e:
            print(f"Skipping file {file_path}: {e}")
            output_content.append(
                f"<!-- Skipping file {relative_path}: {e} -->\n")

        # End the code block
        output_content.append('\n```\n\n')

# Compute total folders
total_folders = len(folders_set)

# Generate the index
index_lines = generate_index(directory_tree)

# Write to the output file
with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
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
