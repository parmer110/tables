import os

def check_for_null_bytes(folder_path):
    for root, dirs, files in os.walk(folder_path):
        if '.git' in dirs:
            dirs.remove('.git')
        if 'migrations' in dirs:
            dirs.remove('migrations')
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        for file in files:
            if file.endswith(('.py', '.js', '.css', '.html')):
                file_path = os.path.join(root, file)
                if not os.path.islink(file_path):  # Ignoring symbolic links
                    with open(file_path, 'rb') as f:
                        contents = f.read()
                        if b'\x00' in contents:
                            print(f"Null bytes found in: {file_path}")

if __name__ == "__main__":
    project_directory = os.path.dirname(os.path.abspath(__file__))  # Get the project directory
    check_for_null_bytes(project_directory)
