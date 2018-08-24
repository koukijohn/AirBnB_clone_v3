#!/usr/bin/python3
'''
    This is our Places module.
'''
import models
from api.v1.views import app_views
from flask import jsonify, request, abort


def get_method_places(place_id=None):
    '''
        This is our get method.
    '''
    if place_id is None:
        return None
    else:
        place = models.storage.get("Place", place_id)
        if place is None:
            return None
        return place.to_dict()


def get_method_cities(city_id=None):
    '''
        This is our get method.
    '''
    if city_id is None:
        return None
    else:
        city = models.storage.get("City", city_id)
        if city is None:
            return None
        cities_places = [x.to_dict() for x in city.places]
        return cities_places


def post_method(city_id, body):
    '''
        This is our post method.
    '''
    city = models.storage.get("City", city_id)
    if city is None:
        return None
    new_place = models.classes["Place"]()
    setattr(new_place, "city_id", city.id)
    for k, v in body.items():
        setattr(new_place, k, v)
    models.storage.new(new_place)
    models.storage.save()
    return new_place.to_dict()


def put_method(place_id, body):
    '''
        This is our put method.
    '''
    blacklist = ["id", "user_id", "city_id", "created_at", "updated_at"]
    old_place = models.storage.get("Place", place_id)
    if old_place is None:
        return None
    for k, v in body.items():
        if k not in blacklist:
            setattr(old_place, k, v)
    models.storage.save()
    return old_place.to_dict()


def delete_method(place_id):
    '''
        This is our delete method.
    '''
    old_place = models.storage.get("Place", place_id)
    if old_place is None:
        return None
    models.storage.delete(old_place)
    models.storage.save()
    return {}


@app_views.route('/cities/<city_id>/places', methods=['POST', 'GET',
                                                    'PUT', 'DELETE'])
@app_views.route('/places/<place_id>', methods=['GET', 'PUT',
                                                'DELETE', 'POST'])
def place_main(place_id=None, city_id=None):
    '''
        This will ...
    '''
    if request.method == 'GET':
        if place_id:
            result = get_method_places(place_id)
        else:
            result = get_method_cities(city_id)
        if result is None:
            abort(404)
        return jsonify(result), 200

    elif request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if "user_id" not in request.json:
            abort(400, "Missing user_id")
        if "name" not in request.json:
            abort(400, "Missing name")
        body = request.get_json()
        result = post_method(body)
        return jsonify(result), 201

    elif request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        body = request.get_json()
        result = put_method(place_id, body)
        if result is None:
            abort(404)
        return jsonify(result), 200
    elif request.method == 'DELETE':
        result = delete_method(place_id)
        if result is None:
            abort(404)
        return jsonify(result), 200
    else:
        pass
