#!/usr/bin/python3
'''
    This is our Review module.
'''
import models
from api.v1.views import app_views
from flask import jsonify, request, abort


def get_method_reviews(review_id=None):
    '''
        This is our get method.
    '''
    if review_id is None:
        return None
    else:
        review = models.storage.get("Review", review_id)
        if review is None:
            return None
        return review.to_dict()


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
        places_reviews = [x.to_dict() for x in place.reviews]
        return places_reviews


def post_method(place_id, body):
    '''
        This is our post method.
    '''
    place = models.storage.get("Place", place_id)
    if place is None:
        return None
    new_review = models.classes["Review"]()
    setattr(new_review, "place_id", place.id)
    for k, v in body.items():
        setattr(new_review, k, v)
    models.storage.new(new_review)
    models.storage.save()
    return new_review.to_dict()


def put_method(review_id, body):
    '''
        This is our put method.
    '''
    blacklist = ["id", "user_id", "place_id", "created_at", "updated_at"]
    old_review = models.storage.get("Review", review_id)
    if old_review is None:
        return None
    for k, v in body.items():
        if k not in blacklist:
            setattr(old_review, k, v)
    models.storage.save()
    return old_review.to_dict()


def delete_method(review_id):
    '''
        This is our delete method.
    '''
    old_review = models.storage.get("Review", review_id)
    if old_review is None:
        return None
    models.storage.delete(old_review)
    models.storage.save()
    return {}


@app_views.route('/places/<place_id>/reviews', methods=['POST', 'GET',
                                                        'PUT', 'DELETE'])
@app_views.route('/reviews/<review_id>', methods=['GET', 'PUT',
                                                  'DELETE', 'POST'])
def review_main(review_id=None, place_id=None):
    '''
        This will ...
    '''
    if request.method == 'GET':
        if review_id:
            result = get_method_reviews(review_id)
        else:
            result = get_method_places(place_id)
        if result is None:
            abort(404)
        return jsonify(result), 200

    elif request.method == 'POST':
        if not request.json:
            abort(400, "Not a JSON")
        if "user_id" not in request.json:
            abort(400, "Missing user_id")
        if "text" not in request.json:
            abort(400, "Missing text")
        body = request.get_json()
        result = post_method(place_id, body)
        if result is None:
            abort(404)
        return jsonify(result), 201

    elif request.method == 'PUT':
        if not request.json:
            abort(400, "Not a JSON")
        body = request.get_json()
        result = put_method(review_id, body)
        if result is None:
            abort(404)
        return jsonify(result), 200
    elif request.method == 'DELETE':
        result = delete_method(review_id)
        if result is None:
            abort(404)
        return jsonify(result), 200
    else:
        pass
