

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
        cleaned_back = cleaned_back.replace('- ', '')
        return cleaned_back
    
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
        
    def __repr__(self) -> str:
        return f'Front: {self.front}, Back: {self.back}, Reference: {self.reference}, Tag: {self.tag}'


def count_spaces(input_string):
    return len(input_string) - len(input_string.lstrip(' '))

def markdown_to_cards(md_content, deck_name) -> list:

    lines = md_content.split('\n')
    cards = []
    current_card = Flashcard()
    topic, lecture = '', ''
    
    for line in lines:

        # Extract lecture and topic
        if line[0:4] == '### ':
            lecture = line[4:]
        if line[0:5] == '#### ':
            topic = line[5:]
        
        current_indentation = count_spaces(line)

        if current_indentation > current_card.indentation:
            current_card.back += line.lstrip() + '\n'
        else:

            current_card.tag = (lecture, topic)
            
            # If this card has already been added, extract ID and update
            match = re.search(r'<!-- (\d+) -->', current_card.front)
            if match:
                id = int(match.group(1))
                update_card(id, current_card)
            else:
                result = add_card(deck_name, current_card)
                if result not in ['None', 'duplicate'] and current_card.front != '':
                    current_card.id = result
                    cards.append(current_card)
        
        if re.search(r'<!--', line):
            current_card = Flashcard()
            current_card.front = line

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


