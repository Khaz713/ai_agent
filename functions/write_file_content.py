import os
from google.genai import types


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


schema_write_file_content = types.FunctionDeclaration(
    name="write_file_content",
    description="Write or overwrite file with provided content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filename": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write or overwrite to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to be written to the file.",
            )
        },
    ),
)
