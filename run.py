import sys
import subprocess
from pathlib import Path

def execute_and_log(executable_path, config_path, option, file_path, output_directory):
    output_name = file_path.stem
    output_directory = Path(output_directory)
    output_directory.mkdir(parents=True, exist_ok=True)  # Ensure the output directory exists

    log_file_path = output_directory / f"{output_name}_log.txt"  # Log file for this specific file

    # Constructing the command with additional parameters
    command = [executable_path, config_path, str(option), str(file_path)]

    # Run the executable and capture the output in the log file
    with open(log_file_path, 'w') as log_file:
        subprocess.run(command, text=True, stdout=log_file, stderr=subprocess.STDOUT)

    return log_file_path

def main(directory, executable, config_path, option, output_directory):
    directory = Path(directory)  # Convert to Path object if not already
    output_directory = Path(output_directory)  # Ensure this is a Path object

    for item in directory.iterdir():  # Iterate through items in the directory
        if item.is_file():  # Process only files
            log_file = execute_and_log(executable, config_path, option, item, output_directory)
            print(f"Processed {item.name}; log saved to {log_file}")

if __name__ == "__main__":
    if len(sys.argv) > 5:
        test_dir = sys.argv[1]
        executable_path = sys.argv[2]
        config_path = sys.argv[3]
        option = sys.argv[4]
        output_path = sys.argv[5]
        main(test_dir, executable_path, config_path, option, output_path)
    else:
        print("Usage: script.py <test_dir> <executable_path> <config_path> <option> <output_directory>")