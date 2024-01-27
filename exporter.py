

import json
import urllib.request


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def make_note(deck_name, flashcard, allow_duplicates):

    if flashcard.card_kind == 'KaTex and Markdown Basic':

        note = {
            "deckName": deck_name,
            "modelName": flashcard.card_kind,
            "fields": {"Front": flashcard.front, "Back": flashcard.back},
            "tags": [""],
        }
    
    else:

        note = {
            "deckName": deck_name,
            "modelName": flashcard.card_kind,
            "fields": {"Text": flashcard.cloze_front, "Back Extra": flashcard.back},
            "tags": [""],
        }

    if allow_duplicates:
        return {**note, "options": {"allowDuplicate": True}}
    else:
        print("Made note")
        print(note)
        return note


def make_updated_note(id, flashcard):

    if flashcard.card_kind == 'KaTex and Markdown Basic':

        note = {
            "id": id,
            "fields": {"Front": flashcard.front, "Back": flashcard.back},
        }

    else:

        note = {
            "id": id,
            "fields": {"Text": flashcard.cloze_front, "Back Extra": flashcard.back},
        }

    return note


def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        pass
    if response['error'] == 'cannot create note because it is a duplicate':
        return 'duplicate'
    return response['result']


def add_card(deck_name, flashcard):
    result = invoke('addNote', note=make_note(deck_name, flashcard, False))
    return result


def update_card(id, flashcard):
    result = invoke('updateNote', note=make_updated_note(id, flashcard))
    return result


