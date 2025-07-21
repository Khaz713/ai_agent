import os


def write_file(working_directory, filename, content):
    file_path = os.path.join(working_directory, filename)
    if os.path.abspath(working_directory) not in os.path.abspath(file_path):
        return f'Error: Cannot write to "{filename}" as it is outside the permitted working directory'
    if not os.path.exists(file_path):
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        except Exception as e:
            return f"Error: creating directory: {e}"
    if os.path.exists(file_path) and os.path.isdir(file_path):
        return f'Error: "{file_path}" is a directory, not a file'
    try:
        with open(file_path, 'w') as f:
            f.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'