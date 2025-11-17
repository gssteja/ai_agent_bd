import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""




def main():
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
        ]
    )
  
    args = sys.argv[1:]
    verbose = False
    if args and args[-1] == '--verbose':
        verbose = True
        args = args[:-1]


    user_prompt = "".join(args).strip()
    if not user_prompt:
        print("Please provide a prompt")
        sys.exit(1)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)]),]
    
    for i in range(0,20):
        
        try:
            response = client.models.generate_content(
            model='gemini-2.0-flash-001', contents=messages, 
            config=types.GenerateContentConfig(
                tools=[available_functions], 
                system_instruction=system_prompt)
            )

            for candidate in response.candidates:
                messages.append(candidate.content)
            
            done = (not response.function_calls) and bool(response.text)
            if done:
                print(response.text)
                break

            response_function_calls = response.function_calls
            if response_function_calls:
                for function_call_part in response_function_calls:
                    print(f" - Calling function: {function_call_part.name}")
                    call_result = call_function(function_call_part, verbose)
                    messages.append(types.Content(role="user", parts=call_result.parts))
                    
                    fr = getattr(call_result.parts[0], "function_response", None)
                    if not fr or not fr.response:
                        raise RuntimeError("No function response in tool content")
                    if verbose:
                        print(f"-> {fr.response}")
                continue
           
        except Exception as e:
            if verbose:
                print(f"Error: {e}")
            break

        if verbose:

            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count
        
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        
            print(f"Function call result: {call_result}")

if __name__ == "__main__":
    main()
