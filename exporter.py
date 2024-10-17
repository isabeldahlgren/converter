import json
import urllib.request


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def make_note(deck_name, flashcard, allow_duplicates):

    if flashcard.card_kind == 'Custom':

        note = {
            "deckName": deck_name,
            "modelName": "Custom",
            "fields": {"Front": flashcard.front, "Back": flashcard.back, "Reference": flashcard.reference},
            "tags": [flashcard.tag],
        }
    
    else:

        note = {
            "deckName": deck_name,
            "modelName": flashcard.card_kind,
            "fields": {"Text": flashcard.cloze_front, "Back Extra": '', "Reference": flashcard.reference},
            "tags": [flashcard.tag],
        }

    if allow_duplicates:
        return {**note, "options": {"allowDuplicate": True}}
    else:
        return note


def make_updated_note(id, flashcard):

    if flashcard.card_kind == 'Custom':

        note = {
            "id": id,
            "modelName": 'Custom',
            "fields": {"Front": flashcard.front, "Back": flashcard.back, "Reference": flashcard.reference},
            "tags": [flashcard.tag],
        }

    else:

        note = {
            "id": id,
            "modelName": flashcard.card_kind,
            "fields": {"Text": flashcard.cloze_front, "Back Extra": '', "Reference": flashcard.reference},
            "tags": [flashcard.tag],
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
    result = invoke('updateNoteModel', note=make_updated_note(id, flashcard))
    return result


def delete_card(id):
    result = invoke('updateNote', note={id})
