from functions.get_file_contents import get_file_contents
from functions.get_file_info import get_files_info 
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types


def call_function(function_call_part, verbose=False):
    if function_call_part.name not in ["get_files_info", "get_file_contents", "write_file", "run_python_file", "call_function"]:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    
    functions_map = {
        "get_files_info": get_files_info,
        "get_file_contents": get_file_contents,
        "write_file": write_file,
        "run_python_file": run_python_file,
        "call_function": call_function
    }

    function_result = functions_map[function_call_part.name](**function_call_part.args)

    if verbose == False:
        print(f"Calling function: {function_call_part.name}(...)")
    else:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        

    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_call_part.name,
            response={"result": function_result},
        )
    ],
    )

