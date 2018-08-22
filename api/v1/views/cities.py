#!/usr/bin/python3
'''
    This is our cities module.
'''
import models
from api.v1.views import app_views
from flask import jsonify, request, abort

def get_method(state_id):
    '''
        This is our get method.
    '''
    if id is None:
        emptylist = []
        for cities in models.storage.all("City").values():
            if cities.state_id == state_id:
                emptylist.append(cities.to_dict())
        return emptylist
    else:
        cities = models.storage.get("City", id)
        if cities is None:
            return None
        return cities.to_dict()


def post_method(state_id, body):
    '''
        This is our post method.
    '''
    new_city = models.classes["City"]()
    setattr(new_city, "state_id", state_id)
    for k, v in body.items():
        setattr(new_city, k, v)
    models.storage.save()
    return new_city.to_dict()


def put_method(city_id, body):
    '''
        This is our put method.
    '''
    old_city = models.storage.get("City", city_id)
    if old_city is None:
        return None
    for k, v in body.items():
        setattr(old_city, k, v)
    models.storage.save()
    return old_city.to_dict()


def delete_method(city_id):
    '''
        This is our delete method.
    '''
    old_city = models.storage.get("City", city_id)
    if old_city is None:
        return None
    models.storage.delete(old_city)
    models.storage.save()
    return {}


@app_views.route('/cities/<city_id>', methods=['PUT', 'DELETE'])
@app_views.route('/states/<state_id>/cities/', methods=['POST', 'GET'])
def cities_main(city_id=None, state_id=None):
    '''
        This will ...
    '''
    if request.method == 'GET':
        result = get_method(state_id)
        if result is None:
            abort(404)
        return jsonify(result)

    elif request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if "name" not in request.json:
            abort(400, "Missing name")
        body = request.get_json()
        result = post_method(state_id, body)
        return jsonify(result), 201

    elif request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        if "name" not in request.json:
            abort(400, "Missing name")
        body = request.get_json()
        result = put_method(city_id, body)
        if result is None:
            abort(404)
        return jsonify(result), 200
    elif request.method == 'DELETE':
        result = delete_method(city_id)
        if result is None:
            abort(404)
        return jsonify(result), 200
    else:
        pass
