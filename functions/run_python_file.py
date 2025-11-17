import os 
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    working_dir_abs = os.path.abspath(working_directory)
    file_path_abs = os.path.abspath(os.path.join(working_dir_abs, file_path))
    if not file_path_abs.startswith(working_dir_abs):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(file_path_abs):
        return f'Error: File "{file_path}" not found.'
    if not file_path_abs.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'

    try:
        args_list = ["python3", file_path_abs] + args
        completed_process = subprocess.run(args_list, timeout = 30, capture_output = True)
        
        stdout_str = completed_process.stdout
        stderr_str = completed_process.stderr

        output = f'STDOUT: {stdout_str} \n STDERR: {stderr_str}'

        if not completed_process.returncode == 0:
            output += f'\nProcess exited with code X'
        elif not completed_process:
            return "No output produced."

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the specified python file along with the optionally passed arguments with a timeout for execution of 30s. Returns stdout, stderr and the relevant return code, or the relevant error if failed",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path for the file which is supposed to be executed",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Arguments to pass along with the file path for program execution",
                items=types.Schema(type=types.Type.STRING,
                                   description="each argument which has to be passed while program execution")
            ),
        },
    ),
)

