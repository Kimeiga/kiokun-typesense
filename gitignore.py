import os


def add_large_files_to_gitignore(directory, max_size_mib=50):
    gitignore_file = os.path.join(directory, ".gitignore")

    # Collect large files
    large_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # Convert to MiB

            if file_size > max_size_mib and ".git" not in root:  # Skip .git directory
                # Get relative path
                rel_path = os.path.relpath(file_path, directory)
                large_files.append(rel_path)

    # Append to .gitignore
    with open(gitignore_file, "a") as gitignore:
        for file in large_files:
            gitignore.write(f"{file}\n")

    print(f"Added {len(large_files)} files to {gitignore_file}")


# Replace 'your_project_directory' with the path to your project directory
add_large_files_to_gitignore(".")
