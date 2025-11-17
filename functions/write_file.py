import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.join(working_dir_abs, file_path)
    
    if not file_path_abs.startswith(working_dir_abs):
        return f'Error: Cannot write "{file_path}" as it is outside the permitted working directory'

    try:
        if not os.path.exists(file_path_abs):
            os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
        with open(file_path_abs, "w") as file: 
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as error: 
        print(f"Error: {error}")


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes a specific passed content to a specified file and returns the length of the number of character written, if failed - throws an error",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to which the content is to be written",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content which has to be written to the specified file"
            ),
        },
    ),
)

