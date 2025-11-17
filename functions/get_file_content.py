from functions.config import MAX_CHARACTER_LIMIT
import os
from google.genai import types

def get_file_content(working_directory, file_path):

    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.join(working_dir_abs, file_path)
    
    if not file_path_abs.startswith(working_dir_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(file_path_abs):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(file_path_abs, "r") as file: 
            file_content_string = file.read()
            if len(file_content_string) > MAX_CHARACTER_LIMIT:
                file_content_string = f'[{file_content_string[:MAX_CHARACTER_LIMIT]}...File "{file_path_abs}" truncated at 10000 characters]'
            return file_content_string
    except Exception as error:
            print(f"Error: {error}")


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the file contents of a specified file, constrained to the working directory and to a max character limit of 10000",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path from which the content should be retrieved, relative to the working directory. If not provided, throws an error",
            ),
        },
    ),
)







