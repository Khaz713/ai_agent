import os
from config import MAX_CHARS
from google.genai import types


def get_file_content(working_directory, file):
    file_path = os.path.join(working_directory, file)
    if os.path.abspath(working_directory) not in os.path.abspath(file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(file_path, 'r') as file:
            file_content_string = file.read(MAX_CHARS)
            if MAX_CHARS < os.path.getsize(file_path):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

            return file_content_string
    except Exception as e:
        return f'Error: {e}'


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the content of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read from, relative to the working directory.",
            ),
        },
    ),
)
