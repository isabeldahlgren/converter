
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
    def card_kind(self) -> str:
        if '__' in self._back or '__' in self._front:
            return 'KaTex and Markdown Cloze'
        else:
            return 'Custom'

    @property
    def cloze_front(self) -> str:
        pattern = re.compile(r'__(.*?)__')
        occurrence_count = 0
        def replace(match):
            nonlocal occurrence_count
            occurrence_count += 1
            return f'{{{{c{occurrence_count}::{match.group(1)}}}}}'
        cloze_front = pattern.sub(replace, self.front)
        cloze_indented = pattern.sub(replace, self.back)
        return f'{cloze_front}\n{cloze_indented}'
    
    @property
    def front(self):
        pattern = r'<!--( (\d+) )?-->'
        cleaned_front = re.sub(pattern, '', self._front)
        if cleaned_front.count('\n') <= 1:
            cleaned_front = cleaned_front.replace('- ', '')
        cleaned_front = cleaned_front.replace('- *Proof.*', '\n*Proof.*')
        return cleaned_front
    
    @front.setter
    def front(self, string):
        self._front = string
    
    @property
    def back(self):
        pattern = r'- cf\. .*?\n'
        cleaned_back = re.sub(pattern, '', self._back)
        if cleaned_back.count('\n') <= 1:
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
    
    def __str__(self) -> str:
        return f'Front: {self.front}, Back: {self.back}, Reference: {self.reference}, Tag: {self.tag}'


def count_spaces(input_string):
    return len(input_string) - len(input_string.lstrip(' '))


def markdown_to_cards(md_content, deck_name) -> list:

    lines = md_content.split('\n')
    cards = []
    topic, lecture = '', ''
    current_card = Flashcard()
    adding_content = False
    prev_line, prev_prev_line = '', ''
    
    for line in lines:

        if len(line) == 0:
            continue

        current_indentation = count_spaces(line)

        if line[0:3] == '## ':
            lecture = line[3:]
            prev_line, prev_prev_line = line, prev_line
            continue
        elif line[0:4] == '### ':
            topic = line[4:]
            prev_line, prev_prev_line = line, prev_line
            continue
        elif not adding_content and '<!--' not in line:
            prev_line, prev_prev_line = line, prev_line
            continue

        if current_indentation > current_card.indentation:
            current_card._back += line.lstrip() + '\n'
        elif current_card._front != '':

            adding_content = False  # Finalise card
            if 'Proof.' in current_card.front:
                current_card._front = prev_prev_line.strip('- ') + '\n' + prev_line.strip('- ') + '\n' + current_card._front
            current_card.tag = (lecture, topic)
            match = re.search(r'<!-- (\d+) -->', current_card._front)  # Check if card has been stored
            if match:
                id = int(match.group(1))
                result = update_card(id, current_card)
            elif current_card not in cards:
                result = add_card(deck_name, current_card)
                if result != None and result != 'duplicate':
                    current_card.id = result
                    cards.append(current_card)

        if '<!--' in line:
            current_card = Flashcard()
            current_card.front = line
            current_card.indentation = current_indentation
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

    print("Done.")

if __name__ == "__main__":
    main()
