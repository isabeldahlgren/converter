

import sys
import re
from exporter import add_card, update_card


class Flashcard:

    def __init__(self) -> None:
        self.indentation = 0
        self._front = ''
        self._back = ''
        self._reference = ''
        self._tag = ''
        self.id = ''
    
    @property
    def front(self):
        return self._front.lstrip('- ')
    
    @front.setter
    def front(self, string):
        pattern = r'-\s*(.*?)\s*<!---->'
        match = re.search(pattern, string)
        if match:
            self._front = match.group(1)
        else:
            self._front = string
    
    @property
    def back(self):
        pattern = r'- cf\..*'
        cleaned_back = re.sub(pattern, '', self._back)
        return cleaned_back.replace('- ', '')
    
    @back.setter
    def back(self, string):
        self._back = string
    
    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, tuple):
        no_spaces_lecture = re.sub(' ', '-', tuple[0])
        no_spaces_topic = re.sub(' ', '-', tuple[1])
        self._tag = f'{no_spaces_lecture}::{no_spaces_topic}'
    
    @property
    def reference(self):
        pattern = r'cf\. (.*)'
        match = re.search(pattern, self._back)
        if match:
            self._reference = match.group(1)
        else:
            self._reference = '-'
        return self._reference
    
    def __str__(self) -> str:
        return f'Front: {self.front}, Back: {self.back}, Reference: {self.reference}, Tag: {self.tag}'


def count_spaces(input_string):
    return len(input_string) - len(input_string.lstrip(' '))


def markdown_to_cards(md_content, deck_name) -> list:

    lines = md_content.split('\n')
    cards = []
    topic, lecture, previous_indentation = '', '', 0
    current_card = Flashcard()
    adding_content = True
    
    for line in lines:
        
        if len(line) == 0:
            continue
        
        current_indentation = count_spaces(line)
        if line[0:4] == '### ':
            lecture = line[4:]
            continue
        elif line[0:5] == '#### ':
            topic = line[5:]
            continue
        elif not adding_content and '<!--' not in line:
            continue
        
        if current_indentation > previous_indentation:
            current_card._back += line.lstrip()
        elif current_card.back != '':
            adding_content = False  # Finalise card
            current_card.tag = (lecture, topic)

            match = re.search(r'<!-- (\d+) -->', current_card.front)  # Check if card has been stored
            if match:
                id = int(match.group(1))
                update_card(id, current_card)
            elif current_card not in cards:
                result = add_card(deck_name, current_card)
                if result not in ['None', 'duplicate']:
                    current_card.id = result
                cards.append(current_card)

        previous_indentation = current_indentation

        if '<!--' in line:
            current_card = Flashcard()
            current_card.front = line
            adding_content = True

    return cards


def main():

    deck_name = sys.argv[1]
    file_name = sys.argv[2]

    with open(file_name, 'r', encoding='utf-8') as file:
        md_content = file.read()
        added_cards = markdown_to_cards(md_content, deck_name)
   
    for added_card in added_cards:
        md_content = md_content.replace(f'{added_card.front} <!---->', f'{added_card.front} <!-- {added_card.id} -->')

    with open(file_name, 'w') as file:
        file.write(md_content)

if __name__ == "__main__":
    main()


