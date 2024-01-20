
import sys
import re
from export_cards import add_or_update


def count_spaces(input_string):
    count = len(input_string) - len(input_string.lstrip(' '))
    return count


def clean_string(input_str):
    cleaned_str = input_str.replace('**', '')
    cleaned_str = cleaned_str.replace('*', '')
    cleaned_str = re.sub(r'^\s*- \[ \] ', '', cleaned_str)
    cleaned_str = re.sub(r'\$(.*?)\$', r'\\(\1\\)', cleaned_str)
    cleaned_str = re.sub(r'^\s*- ', '- ', cleaned_str)
    return cleaned_str


def markdown_to_anki(md_content):

    cards = []
    lines = md_content.split('\n')
    current_card = {'front': '', 'back': ''}
    current_indentation = 0
    
    for line in lines:

        prev_indentation = current_indentation
        current_indentation = count_spaces(line)

        # If detecting the start of a new card
        if re.match(r'^\s*- \[ \] ', line):
            current_card = {'front': clean_string(line), 'back': ''}
            continue

        # While the current indentation level is greater, keep adding content to back
        if current_indentation >= prev_indentation:
            current_card['back'] += clean_string(line) + '<br>'
        else:
            if current_card['front'] != '':
                parts = current_card['back'].rsplit("<br>", 1)
                current_card['back'] = "".join(parts)
                cards.append(current_card)
            current_card = {'front': '', 'back': ''}

    return cards


def main():

    name = sys.argv[1].upper()
    file_name = f"{name}.md"
    file_path = f"/Users/isabeldahlgren/vimwiki/{name}.md"

    with open(file_name, 'r', encoding='utf-8') as file:
        md_content = file.read()

    flashcards = markdown_to_anki(md_content)
    for flashcard in flashcards:
        add_or_update(name, flashcard)
    
    print("Successfully updated all cards.")

if __name__ == "__main__":
    main()
