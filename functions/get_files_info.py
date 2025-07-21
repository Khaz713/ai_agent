import os


def get_files_info(working_directory, directory="."):
    path = os.path.join(working_directory, directory)
    if os.path.abspath(working_directory) not in os.path.abspath(path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(path):
        return f'Error: "{directory}" is not a directory'
    files = os.listdir(path)
    return_string = ""
    for file in files:
        file_path = os.path.join(path, file)
        return_string += f'- {file}: file_size={os.path.getsize(file_path)}, is_dir={os.path.isdir(file_path)}\n'
    return return_string