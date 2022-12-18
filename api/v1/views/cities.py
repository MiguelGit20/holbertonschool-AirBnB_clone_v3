#!/usr/bin/python3
"""
Create a new view for City objects
that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, make_response, request


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def retrieve_city_objs_route(state_id):
    """Retrieves the list of all City objects by a state."""
    obj_id = storage.get(State, state_id)
    if obj_id is not None:
        obj = storage.all(City)
        cities_list = []
        for o in obj.values():
            if o.state_id == state_id:
                cities_list.append(o.to_dict())
        return jsonify(cities_list)
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieve_city_obj_route(city_id):
    """Retrieves a city with a specified id."""
    obj_id = storage.get(City, city_id)
    if obj_id is not None:
        return jsonify(obj_id.to_dict())
    return make_response(jsonify({'error': 'Not found'}), 404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletes_city_route(city_id):
    """Deletes an object."""
    obj = storage.get(City, city_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def creates_instance_city_route(state_id):
    """Creates a new object."""
    obj_attr = request.get_json()
    if obj_attr is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in obj_attr:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    obj_id = storage.get(State, state_id)
    if obj_id is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    new_instance = City(**obj_attr)
    new_instance.state_id = state_id
    new_instance.save()
    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def updates_city_route(city_id):
    """Updates an object."""
    obj = storage.get(City, city_id)
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
