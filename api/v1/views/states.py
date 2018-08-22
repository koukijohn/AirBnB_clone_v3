#!/usr/bin/python3
'''
    This is our states module.
'''
import models
from api.v1.views import app_views
from flask import jsonify, request, abort

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

@app_views.route('/states/', methods = ['POST', 'GET', 'PUT', 'DELETE'])
@app_views.route('/states/<id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def get_states(id=None):
    '''
        This will ...
    '''
    if request.method == 'GET':
        result = get_method(id)
        if result == None:
            abort(404)
        return jsonify(result)

    elif request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if "name" not in request.json:
            abort(400, "Missing name")
        body = request.get_json()
        result = post_method(body)
        return jsonify(result), 201

    elif request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        if "name" not in request.json:
            abort(400, "Missing name")
        body = request.get_json()
        result = put_method(id, body)
        if result == None:
            abort(404)
        return jsonify(result), 200
    elif request.method == 'DELETE':
        result = delete_method(id)
        if result == None:
            abort(404)
        return jsonify(result), 200
    else:
        pass
