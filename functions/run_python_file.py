def run_python_file(working_directory, file_path, args=[]):
    import os
    import subprocess
    import sys

    target_file = os.path.join(working_directory, file_path)

    try:
        # Pre-checks
        if not os.path.exists(target_file):
            raise FileNotFoundError(f'Error: File "{file_path}" not found.')

        if not target_file.endswith('.py'):
            raise ValueError(f"Error: {file_path} is not a Python file.")

        target_real = os.path.realpath(target_file)
        working_real = os.path.realpath(working_directory)

        if not target_real.startswith(working_real + os.sep) and target_real != working_real:
            raise PermissionError(
                f'Error: Cannot execute "{file_path}" '
                f"as it is outside the permitted working directory."
            )

        # Run subprocess
        command = [sys.executable, target_file] + args
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30,
            check=True
        )

        if not result.stdout.strip():
            print("No output produced")
            return ""
        else:
            print(f"Output of {target_file}:\nSTDOUT:{result.stdout}")
            print(f"Process exited with code {result.returncode}")
            return result.stdout

    except (FileNotFoundError, ValueError, PermissionError) as e:
        # Redirect pre-check exceptions as "stderr"
        print(str(e), file=sys.stderr)
        return str(e)

    except subprocess.CalledProcessError as e:
        # Execution error
        print(f"Error executing {target_file}:\nSTDERR:{e.stderr}", file=sys.stderr)
        return e.stderr
