import os
from functions.config import file_length

def get_file_contents(working_directory, file_path):

    target_file = os.path.join(working_directory, file_path)

    if not os.path.exists(target_file):
        raise FileNotFoundError(f"Error: {target_file} does not exist.")
    
    if not os.path.isfile(target_file):
        raise IsADirectoryError(f"Error: {target_file} is not a file.")
    
    target_real = os.path.realpath(target_file)
    working_real = os.path.realpath(working_directory)

    if not target_real.startswith(working_real + os.sep) and target_real != working_real:
        raise PermissionError(
            f"Error: Cannot read {target_file} "
            f"as it is outside the permitted working directory."
        )

    with open(target_file, 'r', encoding='utf-8') as file:
        contents = file.read(file_length)

    print(f'Contents of {target_file}:\n{contents}')

    return contents