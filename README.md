# Code to Markdown
This script generates a comprehensive Markdown (output.md) file for your project, including:

- Project Title: Automatically set to the name of the folder containing the script.
- Project Statistics: Number of files, folders, lines, characters, and words.
- Index: A navigable table of contents resembling the VS Code Explorer, complete with folder 📁 and file 📄 emojis.
- File Contents: Each file's content is included under its respective heading with syntax highlighting based on file extension.

## Features
- Automatic Index Generation: Creates an organized index that mirrors your project's folder structure.
- Statistics Overview: Provides a quick summary of your project's size and complexity.
- Syntax Highlighting: Supports a wide range of programming languages for code blocks.
- Anchor Links: Enables quick navigation from the index to specific sections within the document.
- Customizable Ignore Lists: Easily exclude specific files or directories from the documentation.

## Requirements
- Python 3.x: The script is written in Python and requires Python 3 to run.
- Operating System: Compatible with Windows, macOS, and Linux.
- Permissions: Ensure the script has read access to the project files and directories.


## Installation
1. Clone or Download the Repository:
    - Clone the repository using Git:
        ```bash
        git clone https://github.com/yourusername/project-doc-generator.git
        ```
    - Or download the ZIP file and extract it.
1. Navigate to the Project Directory:
    ```bash
    cd project-doc-generator
    ```
1. (Optional) Create a Virtual Environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
    ```

## Usage
1. Place the Script in Your Project Folder:
    - Copy the code_to_md.py script into the root directory of the project you want to document.
1. Customize Ignore Lists (Optional):
    - Edit the script to modify the ignore_dirs and ignore_files sets to exclude any directories or files you don't want to include.
        ```python
        ignore_dirs = {'node_modules', 'fonts', '.git', 'images'}
        ignore_files = {'package-lock.json', 'database.db'}
        ```
1. Run the Script:
    ```bash
    python documentation_generator.py
    ```
    - This will generate an output.md file in the same directory.
1. View the Generated Documentation:
    - Open output.md with any Markdown viewer or editor that supports emojis and HTML anchors, such as VS Code or GitHub's Markdown renderer.

## Customization
- Change Output File Name:

    - Modify the output_file variable in the script if you prefer a different name.
        ```python
        output_file = 'documentation.md'
        ```
- Adjust Heading Levels:
    - You can change the Markdown heading levels to suit your preferences.
- Modify Emojis:
    - Replace the folder 📁 and file 📄 emojis with other symbols or remove them entirely in the generate_index function.

## Troubleshooting
- Encoding Issues:
    - If you encounter encoding errors, ensure all your files are encoded in UTF-8.
    - Modify the encoding parameter in the script's file operations if necessary.
- Permission Errors:
    - Ensure you have the necessary read permissions for all files and directories in your project.
- Markdown Renderer Compatibility:
    - The script uses HTML anchors (<a id="..."></a>) for navigation. Ensure your Markdown renderer supports this feature.

---

Happy documenting!