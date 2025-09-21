from functions.get_file_info import get_files_info
from functions.get_file_contents import get_file_contents
from functions.write_file import write_file
from functions.run_python_file import run_python_file

cases = [
    ('calculator', 'main.py'),  # print calc instructions
    ('calculator', 'main.py', ['3 + 5']),  # simple addition
    ('calculator', 'tests.py'),  # run tests
    ('calculator', 'nonexistent.py'),  # file does not exist
    ('calculator', '../main.py'),  # path traversal attempt outside working directory
]

for case in cases:
    try:
        run_python_file(*case)
    except FileNotFoundError as e:
        print(f"[Not Found] {e}")
    except NotADirectoryError as e:
        print(f"[Invalid Directory] {e}")
    except PermissionError as e:
        print(f"[Permission Error] {e}")
    except Exception as e:
        print(f"[Unexpected Error] {e}")


