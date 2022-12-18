#!/usr/bin/python3
"""
Create a new view for User objects
that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, make_response, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retrieve_user_objs_route():
    """Retrieves the list of all User objects."""
    objs = storage.all(User).values()
    objs_list = []
    for instance in objs:
        objs_list.append(instance.to_dict())
    return jsonify(objs_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def retrieve_user_objs_id_route(user_id):
    """Retrieves the list of all User objects with a specified id."""
    obj = storage.get(User, user_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletes_user_route(user_id):
    """Deletes an object."""
    obj = storage.get(User, user_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def creates_instance_user_route():
    """Creates a new object."""
    obj_attr = request.get_json()
    if obj_attr is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in obj_attr:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in obj_attr:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    new_instance = User(**obj_attr)
    new_instance.save()
    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updates_user_route(user_id):
    """Updates an object."""
    obj = storage.get(User, user_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)

    obj_attr = request.get_json()
    if obj_attr is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    for key, val in obj_attr.items():
        if key != ('id', 'updated_at', 'created_at'):
            setattr(obj, key, val)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
