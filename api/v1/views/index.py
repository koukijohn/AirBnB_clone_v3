#!/usr/bin/python3
from api.v1.views import app_views, states
from flask import jsonify, request, abort
from models import storage

@app_views.route('/status')
def status_of_app_views():
    '''
        This will give us the status of our app views.
    '''
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def display_stats():
    '''
        Endpoint that retrieves the number of each object by type.
    '''
    amenities = storage.count("Amenity")
    cities = storage.count("City")
    places = storage.count("Place")
    reviews = storage.count("Review")
    states = storage.count("State")
    users = storage.count("User")

    stats = {
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "reviews": reviews,
        "states": states,
        "users": users
    }
    return jsonify(stats)

@app_views.route('/states/', methods = ['POST', 'GET', 'PUT', 'DELETE'])
@app_views.route('/states/<id>', methods = ['POST', 'GET', 'PUT', 'DELETE'])
def get_states(id=None):
    '''
        This will ...
    '''
    if request.method == 'GET':
        result = states.get_method(id)
        if result == None:
            abort(404)
        return jsonify(result)

    elif request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if "name" not in request.json:
            abort(400, "Missing name")
        body = request.get_json()
        result = states.post_method(body)
        return jsonify(result), 201

    elif request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        if "name" not in request.json:
            abort(400, "Missing name")
        body = request.get_json()
        result = states.put_method(id, body)
        if result == None:
            abort(404)
        return jsonify(result), 200
    elif request.method == 'DELETE':
        result = states.delete_method(id)
        if result == None:
            abort(404)
        return jsonify(result), 200
    else:
        pass
