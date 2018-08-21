#!/usr/bin/python3
'''
    This is our states module.
'''
from flask import jsonify
import models

def get_method(id):
    '''
        This is our get method.
    '''
    if id is None:
        emptylist = []
        for state in models.storage.all("State").values():
            emptylist.append(state.to_dict())
        return emptylist
    else:
        state = models.storage.get("State", id)
        if state is None:
            return None
        return state.to_dict()

def post_method(body):
    '''
        This is our post method.
    '''
    new_state = models.classes["State"]()
    for k, v in body.items():
        setattr(new_state, k, v)
    models.storage.save()
    return new_state.to_dict()

def put_method(id, body):
    '''
        This is our put method.
    '''
    old_state = models.storage.get("State", id)
    if old_state is None:
        return None
    for k, v in body.items():
        setattr(old_state, k, v)
    models.storage.save()
    return old_state.to_dict()

def delete_method(id):
    '''
        This is our delete method.
    '''
    old_state = models.storage.get("State", id)
    if old_state is None:
        return None
    models.storage.delete(old_state)
    models.storage.save()
    return {}
