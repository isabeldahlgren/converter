import re

def replace_patterns(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Define patterns and replacements as tuples
    patterns_and_replacements = [
        (r'\*\*Thm.(.*)\*\*', r'**Thm.**\1'),
        (r'\*Proof.(.*)\*', r'*Proof.*\1'),
        (r'\*\*Lemma.(.*)\*\*', r'**Lemma.**\1'),
        (r'\*\*Cor.(.*)\*\*', r'**Cor.**\1')
    ]

    # Iterate over patterns and replacements
    modified_content = content
    for pattern, replacement in patterns_and_replacements:
        modified_content = re.sub(pattern, replacement, modified_content)

    # Write the modified content to the output file
    with open(output_file, 'w') as f:
        f.write(modified_content)

# Replace patterns in lectures.md and write to output.md
replace_patterns('lectures.md', 'output.md')
