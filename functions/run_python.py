import os
import subprocess
from google.genai import types


def run_python_file(working_directory, filename, args=None):
    file_path = os.path.abspath(os.path.join(working_directory, filename))
    if os.path.abspath(working_directory) not in os.path.abspath(file_path):
        return f'Error: Cannot execute "{filename}" as it is outside the permitted working directory'
    if not os.path.exists(file_path):
        return f'Error: File "{filename}" not found.'
    if not filename.endswith('.py'):
        return f'Error: "{filename}" is not a Python file.'
    try:
        commands = ["python", file_path]
        if args:
            commands.extend(args)
        completed_process = subprocess.run(
            commands,
            cwd=os.path.abspath(working_directory),
            capture_output=True,
            text=True,
            timeout=30
        )
        output = ''
        if completed_process.stdout:
            output += f'STDOUT: {completed_process.stdout}\n'
        if completed_process.stderr:
            output += f'STDERR: {completed_process.stderr}\n'
        if completed_process.returncode != 0:
            output += f'Process exited with code {completed_process.returncode}\n'
        if len(completed_process.stdout) == 0 and len(completed_process.stderr) == 0:
            output = 'No output produced.'
        return output
    except Exception as e:
        return f'Error: executing Python file: {e}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments. If there are no optional arguments provided run the program without them.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "filename": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional arguments to pass to the Python interpreter.",
            )
        },
    ),
)