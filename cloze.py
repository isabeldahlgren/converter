
import sys
import re
from exp import add_card, update_card


# TODO Create card class


def count_spaces(input_string):
    return len(input_string) - len(input_string.lstrip(' '))


def clean_string(input_string):
    cleaned_str = re.sub(r'^\s*- \[ \] ', '', input_string)
    cleaned_str = re.sub(r'^\s*- ', '- ', cleaned_str)
    return cleaned_str

def get_type(flashcard):
    if '<o>' in flashcard['front']:
        return 'KaTex and Markdown Cloze'
    else:
        return 'KaTex and Markdown Basic'


def markdown_to_anki(md_content, deck_name):

    lines = md_content.split('\n')
    current_card = {'front': '', 'back': ''}
    added_cards = []
    current_indentation = 0
    card_indentation = 0
    
    for line in lines:

        # Clean string and get indentation level
        line = rf"{line}"
        current_indentation = count_spaces(line)

        # While the current indentation level is greater, keep adding content to back
        if current_indentation > card_indentation:
            current_card['back'] += clean_string(line) + '\n'
        # When the indentation decreases, stop adding content to the back and try adding card
        elif current_card['front'] != '':

            # If this card has already been added, extract ID and update
            match = re.search(r'<!-- (\d+) -->', current_card['front'])
            if match:
                id = int(match.group(1))
                card_type = get_type(current_card)
                update_card(id, current_card, card_type)
            # Otherwise, create a new one and store front with ID
            else:
                card_type = get_type(current_card)
                result = add_card(deck_name, current_card, card_type)
                if result != 'duplicate':
                    added_cards.append((result, current_card['front']))

            # Reset card and indentation
            current_card = {'front': '', 'back': ''}
            card_indentation = 0
        
        # If detecting the start of a new card
        if re.match(r'^\s*- \[ \] ', line):
            current_card = {'front': clean_string(line), 'back': ''}
            card_indentation = current_indentation

    return added_cards


def main():

    deck_name = sys.argv[1].upper()
    file_name = f"{deck_name}.md"

    with open(file_name, 'r', encoding='utf-8') as file:
        md_content = file.read()
        added_cards = markdown_to_anki(md_content, deck_name)
   
    # Once a new card is added, update the markdown file
    for added_card in added_cards:
        md_content = md_content.replace(added_card[1], f"{added_card[1]} <!-- {added_card[0]} -->")

    with open(file_name, 'w') as file:
        file.write(md_content)
    
    print("Successfully updated all cards.")

if __name__ == "__main__":
    main()

