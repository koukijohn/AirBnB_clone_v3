#!/usr/bin/python3
'''
    This module contains our routes for our status and stats.
'''
from api.v1.views import app_views
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
