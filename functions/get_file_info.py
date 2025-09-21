def get_files_info(working_directory, directory="."):
    import os
    import time

    target_directory = os.path.join(working_directory, directory)

    files_info = []
    
    if not os.path.exists(target_directory):
        raise FileNotFoundError(f"Error: {target_directory} does not exist.")
    
    if not os.path.isdir(target_directory):
        raise NotADirectoryError(f"Error: {target_directory} is not a directory.")
    
    target_real = os.path.realpath(target_directory)
    working_real = os.path.realpath(working_directory)

    if not target_real.startswith(working_real + os.sep) and target_real != working_real:
        raise PermissionError(
            f"Error: Cannot list {target_directory} "
            f"as it is outside the permitted working directory."
        )

    for entry in os.scandir(target_directory):
        file_info = {
                "name": entry.name,
                "size_bytes": entry.stat().st_size,
                "last_modified": time.ctime(entry.stat().st_mtime),
                "path": entry.path,
                "is_dir": os.path.isdir(entry.path),
                "is_file": os.path.isfile(entry.path)
                }
        files_info.append(file_info)

    for file_info in files_info:
        print(f'- {file_info["name"]}: file_size={file_info["size_bytes"]} bytes, is_dir={file_info["is_dir"]}')

    return files_info