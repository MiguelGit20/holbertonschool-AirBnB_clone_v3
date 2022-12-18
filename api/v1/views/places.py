#!/usr/bin/python3
"""
Create a new view for Place objects
that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from flask import jsonify, make_response, request


@app_views.route('/cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_per_city(city_id=None):
    """Places route to handle http method for requested places by city."""

    if request.method == 'GET':
        city_obj = storage.get(City, city_id)
        if city_obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        all_places = storage.all(Place)
        city_places = [obj.to_dict() for obj in all_places.values()
                       if obj.city_id == city_id]
        return jsonify(city_places)

    if request.method == 'POST':
        city_obj = storage.get(City, city_id)
        if city_obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        req_json = request.get_json()
        if req_json is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'user_id' not in req_json:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        u_id = req_json['user_id']
        user_obj = storage.get('User', u_id)
        if user_obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        if 'name' not in req_json:
            return make_response(jsonify({'error': 'Missing name'}), 400)

        new_instance = Place(**req_json)
        new_instance.city_id = city_id
        new_instance.user_id = u_id
        new_instance.save()
        return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def retrieve_place_objs_id(place_id):
    """Retrieves the list of all Place objects with a specified id."""
    obj = storage.get(Place, place_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletes_place_route(place_id):
    """Deletes an object."""
    obj = storage.get(Place, place_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def updates_place_route(place_id):
    """Updates an object."""
    obj = storage.get(Place, place_id)
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
