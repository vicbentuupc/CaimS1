import os
import shutil


def process_file(input_file_path, output_file_path):
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        for line in input_file:
            for char in line:
                if char.isdigit():
                        output_file.write(' ')
                
                output_file.write(char.lower())


def copy_structure_and_process(input_dir, output_dir):
    # Walk through the input directory, including subdirectories
    for root, dirs, files in os.walk(input_dir):
        # Construct the corresponding path in the output directory
        relative_path = os.path.relpath(root, input_dir)
        output_subdir = os.path.join(output_dir, relative_path)

        # Create the same subdirectory structure in the output directory
        os.makedirs(output_subdir, exist_ok=True)

        # Process each file in the current directory
        for file_name in files:
            input_file_path = os.path.join(root, file_name)
            output_file_path = os.path.join(output_subdir, file_name)
            
            # Process the file (e.g., copy it or modify and save it)
            process_file(input_file_path, output_file_path)
            print(f"Processed {input_file_path} to {output_file_path}")

if __name__ == "__main__":
    input_dir = "data/novels"
    output_dir = "processed_data/novels"

    copy_structure_and_process(input_dir, output_dir)
