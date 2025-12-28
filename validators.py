import os

def is_file_path(path):
    if os.path.isdir(path):
        raise IsADirectoryError(f"expected a file path, got directory: {path}")
    

def dir_exists(path):
    if os.path.isdir(path) != True:
        return False
    else: return True