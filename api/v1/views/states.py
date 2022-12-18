#!/usr/bin/python3
"""
Create a new view for State objects
that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import jsonify, make_response, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_state_objs_route():
    """Retrieves the list of all State objects."""
    objs = storage.all(State).values()
    objs_list = []
    for instance in objs:
        objs_list.append(instance.to_dict())
    return jsonify(objs_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_state_objs_id_route(state_id):
    """Retrieves the list of all State objects with a specified id."""
    obj = storage.get(State, state_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletes_state_route(state_id):
    """Deletes an object."""
    obj = storage.get(State, state_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def creates_instance_state_route():
    """Creates a new object."""
    obj_attr = request.get_json()
    if obj_attr is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in obj_attr:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_instance = State(**obj_attr)
    new_instance.save()
    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def updates_state_route(state_id):
    """Updates an object."""
    obj = storage.get(State, state_id)
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
