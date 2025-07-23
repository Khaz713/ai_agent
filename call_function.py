from google.genai import types

from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python import schema_run_python_file, run_python_file
from functions.write_file_content import schema_write_file_content, write_file

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file_content,
    ]
)

functions_names = [
    "get_files_info",
    "get_file_content",
    "run_python_file",
    "write_file_content"
]

def call_function(function_call_part, verbose):
    function_name = function_call_part.name
    function_args = function_call_part.args
    working_directory = 'calculator'
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f"Calling function: {function_name}")
    if function_name not in functions_names:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    if function_name == "run_python_file":
        function_result = run_python_file(working_directory, **function_args)
    if function_name == "write_file_content":
        function_result = write_file(working_directory, **function_args)
    if function_name == "get_files_info":
        function_result = get_files_info(working_directory, **function_args)
    if function_name == "get_file_content":
        function_result = get_file_content(working_directory, **function_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )

