
import json
import urllib.request


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}


def make_note(deck_name, flashcard, allow_duplicates):

    note = {
        "deckName": deck_name,
        "modelName": "Basic",
        "fields": {"Front": flashcard['front'], "Back": flashcard['back']},
        "tags": [""],
    }

    if allow_duplicates:
        return {**note, "options": {"allowDuplicate": True}}
    else:
        return note


def make_updated_note(id, flashcard):

    note = {
            "id": id,
            "fields": {
                "Front": flashcard['front'],
                "Back": flashcard['back']
            },
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

def request_update(id, flashcard):
    invoke('updateNote', note=make_updated_note(id, flashcard))

def add_or_update(name, flashcard):

    result = invoke('addNote', note=make_note(name, flashcard, False))
    if result == 'duplicate':
        id = invoke('findCards', query=flashcard['front'])
        if id is None:
            # Can't use \ to search in Anki
            new_front = flashcard['front'].replace('\\', '\\\\')
            id = invoke('findCards', query=new_front)
        
        request_update(id[0], flashcard)


