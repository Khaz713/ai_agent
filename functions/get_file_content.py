import os
from config import MAX_CHARS

def get_file_content(working_directory, file):
    file_path = os.path.join(working_directory, file)
    if os.path.abspath(working_directory) not in os.path.abspath(file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(file_path, 'r') as file:
            file_content_string = file.read()
            if MAX_CHARS < len(file_content_string):
                file_content_string = f'{file_content_string[:MAX_CHARS]}\n [...File "{file_path}" truncated at 10000 characters]'

            return file_content_string
    except Exception as e:
        return f'Error: {e}'
