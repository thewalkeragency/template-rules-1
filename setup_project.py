import os
import shutil

def replace_in_file(file_path, old_str, new_str):
    """Replace a string in a file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        content = content.replace(old_str, new_str)
        with open(file_path, 'w') as file:
            file.write(content)
    except (IOError, UnicodeDecodeError) as e:
        print(f"Could not process file {file_path}: {e}")

def main():
    """Main function to set up the project."""
    print("--- Project Setup ---")

    project_name = input("Enter the human-readable project name (e.g., 'My Awesome Project'): ")
    project_slug = input("Enter the project slug (e.g., 'my-awesome-project'): ")
    author_name = input("Enter the author name: ")
    author_email = input("Enter the author email: ")

    placeholders = {
        "{{Project Name}}": project_name,
        "{{project_slug}}": project_slug,
        "{{author_name}}": author_name,
        "{{author_email}}": author_email,
    }

    print("\nReplacing placeholders...")
    for root, _, files in os.walk("."):
        if ".git" in root:
            continue
        for file in files:
            if file == "setup_project.py":
                continue
            file_path = os.path.join(root, file)
            for old, new in placeholders.items():
                replace_in_file(file_path, old, new)

    print("Placeholder replacement complete.")

    # Optional: Rename the source directory if it exists
    old_src_dir = os.path.join("src", "{{project_slug}}")
    if os.path.exists(old_src_dir):
        new_src_dir = os.path.join("src", project_slug)
        shutil.move(old_src_dir, new_src_dir)
        print(f"Renamed '{old_src_dir}' to '{new_src_dir}'.")

    print("\n--- Setup Complete ---")
    print("You can now delete this setup script.")
    print(f"To get started, run: 'pip install -e .' from your virtual environment.")

if __name__ == "__main__":
    main()
