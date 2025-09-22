import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_info import get_files_info
from functions.get_file_contents import get_file_contents
from functions.write_file import write_file
from functions.run_python_file import run_python_file
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_contents = types.FunctionDeclaration(
    name="get_file_contents",
    description="Reads and returns the contents of a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="A list of arguments to pass to the Python script.",
            ),
        },
        required=["file_path"],
    ),
)

schema_call_function = types.FunctionDeclaration(
    name="call_function",
    description="Logs the function call details for debugging purposes.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "function_call_part": types.Schema(
                type=types.Type.OBJECT,
                description="The function call part containing the name and arguments of the function to be called.",
            ),
            "verbose": types.Schema(
                type=types.Type.BOOLEAN,
                description="If true, prints detailed function call information; otherwise, prints a summary.",
            ),
        },
        required=["function_call_part"],
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_contents,
        schema_write_file,
        schema_run_python_file,
        schema_call_function,
    ]
)

system_prompt = system_prompt = """You are a helpful AI coding agent.
When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files
All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

user_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)])
]
response = client.models.generate_content(
    model = "gemini-2.0-flash-001",
    contents = messages,
    config = types.GenerateContentConfig(
        tools=[available_functions], 
        system_instruction=system_prompt,)
)

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count
if response.function_calls:
    fc = response.function_calls[0]
    func_name = fc.name
    func_args = fc.args
    fc.args['working_directory'] = "./calculator"

if len(sys.argv) < 2:
    sys.exit("Please provide a prompt as a command-line argument.")
else:
#if sys.argv[2] == "--verbose":
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")

if response.function_calls:
    print(f"Calling function: {fc.name}({fc.args})")
    call_function(fc)
else:
    print(response.text)
    
print(f"Response tokens: {response_tokens}")