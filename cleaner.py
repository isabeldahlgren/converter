import re
import sys

def replace_pattern_in_file(input_file, output_file, pattern, replacement):
    try:
        with open(input_file, 'r') as file:
            content = file.read()

        # Use regular expression to replace the specified pattern
        modified_content = re.sub(pattern, replacement, content)

        with open(output_file, 'w') as file:
            file.write(modified_content)

        print(f"Replacement successful. Result written to {output_file}.")

    except FileNotFoundError:
        print(f"File not found: {input_file}")

# Example usage:
input_file_path = 'sample.md'
output_file_path = 'sample.md'
pattern = r'<!-- (\d)* -->'
replacement = '<!---->'
replace_pattern_in_file(input_file_path, output_file_path, pattern, replacement)

