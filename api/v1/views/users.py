#!/usr/bin/python3
'''
    This is our Users module.
'''
import models
from api.v1.views import app_views
from flask import jsonify, request, abort


def get_method(user_id=None):
    '''
        This is our get method.
    '''
#    print(user_id)
#    print(type(user_id))
    if user_id is None:
        emptylist = []
        for user in models.storage.all("User").values():
            emptylist.append(user.to_dict())
        return emptylist
    else:
        user = models.storage.get("User", user_id)
        if user is None:
            return None
        return user.to_dict()


def post_method(body):
    '''
        This is our post method.
    '''
    new_user = models.classes["User"]()
    for k, v in body.items():
        setattr(new_user, k, v)
    models.storage.new(new_user)
    models.storage.save()
    return new_user.to_dict()


def put_method(user_id, body):
    '''
        This is our put method.
    '''
    blacklist = ["id", "email", "created_at", "updated_at"]
    old_user = models.storage.get("User", user_id)
    if old_user is None:
        return None
    for k, v in body.items():
        if k not in blacklist:
            setattr(old_user, k, v)
    models.storage.save()
    return old_user.to_dict()


def delete_method(user_id):
    '''
        This is our delete method.
    '''
    old_user = models.storage.get("User", user_id)
    if old_user is None:
        return None
    models.storage.delete(old_user)
    models.storage.save()
    return {}


@app_views.route('/users', methods=['POST', 'GET', 'PUT', 'DELETE'])
@app_views.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE', 'POST'])
def user_main(user_id=None):
    '''
        This will ...
    '''
    if request.method == 'GET':
        result = get_method(user_id)
        if result is None:
            abort(404)
        return jsonify(result), 200

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
        body = request.get_json()
        result = put_method(user_id, body)
        if result is None:
            abort(404)
        return jsonify(result), 200
    elif request.method == 'DELETE':
        result = delete_method(user_id)
        if result is None:
            abort(404)
        return jsonify(result), 200
    else:
        pass
