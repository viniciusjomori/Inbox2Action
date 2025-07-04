import os
import shutil
import base64

class File:
    def __init__(self, name, content, path="", binary=False):
        self.name = name
        self.content = content
        self.path = path
        self.binary = binary

def exists(path):
    return os.path.exists(path)

def is_file(path):
    return os.path.isfile(path)

def is_dir(path):
    return os.path.isdir(path)

def create_dir(path):
    if not exists(path):
        os.makedirs(path)

def get_filename(path):
    return os.path.basename(path)

def ls_all(path):
    return os.listdir(path)

def ls_files(path):
    files = ls_all(path)
    files = [file for file in files if is_file(f'{path}/{file}')]
    return files

def ls_dirs(path):
    dirs = ls_all(path)
    dirs = [dir for dir in dirs if is_dir(f'{path}/{dir}')]
    return dirs

def create_file(file, path=""):
    binary = is_binary(file.content)

    method = 'wb' if binary else 'w'
    encoding = None if binary else 'utf-8'

    if path:
        create_dir(path)

    path = os.path.join(path, file.name)

    with open(path, method, encoding=encoding) as new_file:
        new_file.write(file.content)    

def delete_file(path):
    os.remove(path)

def delete_dir(path):
    shutil.rmtree(path)

def move_file(og_path, new_path):
    shutil.move(og_path, new_path)

def clear_dir(path):
    delete_dir(path)
    create_dir(path)

def is_binary(content):
    if isinstance(content, str):
        return False

    return True

def get_extension(path):
    _, extension = os.path.splitext(path)
    return extension.lstrip('.')

def to_base64(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode('utf-8')