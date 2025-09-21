def write_file(working_directory, file_path, content):
    import os

    target_file = os.path.join(working_directory, file_path)

    target_real = os.path.realpath(target_file)
    working_real = os.path.realpath(working_directory)

    if not target_real.startswith(working_real + os.sep) and target_real != working_real:
        raise PermissionError(
            f"Error: Cannot write to {target_file} "
            f"as it is outside the permitted working directory."
        )
    
    if not os.path.exists(target_file):
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

    with open(target_file, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f'Wrote to {target_file} successfully \n ({len(content)} characters written)')

    return True