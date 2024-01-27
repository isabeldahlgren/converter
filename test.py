
import re

def cloze_front(input_string) -> str:
    return re.sub(r'<g>(.*?)<\/g>', r'{{c1::\1}}', input_string)

def replace_b_tags(input_string):
    # Define a regular expression pattern to match <b>...</b> tags
    pattern = re.compile(r'<g>(.*?)</g>')

    # Initialize occurrence count
    occurrence_count = 0

    # Use a lambda function as the replacement to add the desired format with occurrence count
    def replace(match):
        nonlocal occurrence_count
        occurrence_count += 1
        return f'{{{{c{occurrence_count}::{match.group(1)}}}}}'

    # Use the updated lambda function in the sub method
    result = pattern.sub(replace, input_string)

    return result

# Example usage
input_text = "<g>hello</g> world <g>I</g> am here to <g>help</g>"
output_text = replace_b_tags(input_text)

print(output_text)
print(cloze_front(input_text))