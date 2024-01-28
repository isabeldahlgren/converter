
import sys
import re
from exporter import add_card, update_card


class Flashcard:

    def __init__(self, front, indentation) -> None:
        self.front = re.sub('-', '', front)
        self.indentation = indentation
        self.back = ''
        self.id = ''
        self.tag = ''

    @property
    def card_kind(self) -> str:
        if '<g>' in self.front:
            return 'KaTex and Markdown Cloze'
        else:
            return 'KaTex and Markdown Basic'

    @property
    def cloze_front(self) -> str:
        pattern = re.compile(r'<g>(.*?)</g>')

        occurrence_count = 0
        def replace(match):
            nonlocal occurrence_count
            occurrence_count += 1
            return f'{{{{c{occurrence_count}::{match.group(1)}}}}}'

        return pattern.sub(replace, self.front)
        
    def __repr__(self) -> str:
        return f'{self.front} {self.back} {self.id} {self.tag}'


def count_spaces(input_string):
    return len(input_string) - len(input_string.lstrip(' '))


def clean_string(input_string):
    # Remove spaces, dashes and tickboxes
    cleaned_str = re.sub(r'^\s*- \[ \]', '', input_string)
    cleaned_str = re.sub(r'^\s*- ', '- ', cleaned_str)
    return cleaned_str

def store_id(input_string, id):

    pattern = r'(.*)<!---->(.*)'
    match = re.search(pattern, input_string)
    output_string = input_string

    if match:
        before_comment = match.group(1)
        after_comment = match.group(2)
        output_string = f'{before_comment}<!-- {id} -->{after_comment}'
    
    return output_string


def markdown_to_anki(md_content, deck_name) -> list:

    lines = md_content.split('\n')
    cards = []
    current_card = Flashcard('', 0)
    current_tag = ''
    
    for line in lines:

        if line[0:3] == '###':
            current_tag = line[5:]
        
        # Clean string and get indentation level
        line = rf"{line}"
        current_indentation = count_spaces(line)

        # While the current indentation level is greater, keep adding content to back
        if current_indentation > current_card.indentation:
            current_card.back += clean_string(line) + '\n'

        # When the indentation decreases, stop adding content to the back and try adding card
        elif current_card.front != '':
            # If this card has already been added, extract ID and update
            match = re.search(r'<!-- (\d+) -->', current_card.front)
            if match:
                id = int(match.group(1))
                update_card(id, current_card)
            # Otherwise, create a new one and store front with ID
            else:
                # Replace spaces with -, so it works in Anki
                current_card.tag = re.sub(' ', '-', current_tag)
                result = add_card(deck_name, current_card)
                if result != 'duplicate' and result != None:
                    current_card.id = result
                    cards.append(current_card)

            # Reset card and indentation
            current_card = Flashcard('', 0)
        
        # If detecting the start of a new card
        if re.search(r'<!--', line):
            current_card = Flashcard(clean_string(line), count_spaces(line))
            print("Detected...")

    return cards


def main():

    deck_name = sys.argv[1]
    file_name = sys.argv[2]

    with open(file_name, 'r', encoding='utf-8') as file:
        md_content = file.read()
        added_cards = markdown_to_anki(md_content, deck_name)
   
    # Once a new card is added, update the markdown file
    # for added_card in added_cards:
    #    md_content = md_content.replace(added_card.front, store_id(added_card.front, added_card.id))

    with open(file_name, 'w') as file:
        file.write(md_content)
    
    print("Successfully updated all cards.")

if __name__ == "__main__":
    main()


