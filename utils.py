import os

def get_absolute_file_paths(directory_path):
    file_paths = []

    if os.name == "nt":
        directory_path = directory_path.replace("/", "\\")

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)

    return file_paths
