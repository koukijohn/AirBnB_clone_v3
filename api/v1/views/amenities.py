#!/usr/bin/python3
'''
    This is our Amenities module.
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
        for amenity in models.storage.all("Amenity").values():
            emptylist.append(amenity.to_dict())
        return emptylist
    else:
        amenity = models.storage.get("Amenity", id)
        if amenity is None:
            return None
        return amenity.to_dict()


def post_method(body):
    '''
        This is our post method.
    '''
    new_amenity = models.classes["Amenity"]()
    for k, v in body.items():
        setattr(new_amenity, k, v)
    models.storage.save()
    return new_amenity.to_dict()


def put_method(id, body):
    '''
        This is our put method.
    '''
    old_amenity = models.storage.get("Amenity", id)
    if old_amenity is None:
        return None
    for k, v in body.items():
        setattr(old_amenity, k, v)
    models.storage.save()
    return old_amenity.to_dict()


def delete_method(id):
    '''
        This is our delete method.
    '''
    old_amenity = models.storage.get("Amenity", id)
    if old_amenity is None:
        return None
    models.storage.delete(old_amenity)
    models.storage.save()
    return {}


@app_views.route('/amenity/', methods=['POST', 'GET', 'PUT', 'DELETE'])
@app_views.route('/amenity/<id>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def amenity_main(id=None):
    '''
        This will ...
    '''
    if request.method == 'GET':
        result = get_method(id)
        if result is None:
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
        if result is None:
            abort(404)
        return jsonify(result), 200
    elif request.method == 'DELETE':
        result = delete_method(id)
        if result is None:
            abort(404)
        return jsonify(result), 200
    else:
        pass
