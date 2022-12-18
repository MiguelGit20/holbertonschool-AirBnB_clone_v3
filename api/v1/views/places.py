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

@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def places_per_city(city_id=None):
    """
        places route to handle http method for requested places by city
    """
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if request.method == 'GET':
        all_places = storage.all(Place)
        city_places = [obj.to_json() for obj in all_places.values()
                       if obj.city_id == city_id]
        return jsonify(city_places)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        user_id = req_json.get("user_id")
        if user_id is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        user_obj = storage.get('User', user_id)
        if user_obj is None:
            return make_response(jsonify({'error': 'Not found'}), 404)
        if req_json.get("name") is None:
            return make_response(jsonify({'error': 'Not found'}), 404)

        req_json['city_id'] = city_id
        new_object = Place(**req_json)
        new_object.save()
        return make_response(jsonify(new_object.to_json()), 201)

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def retrieve_place_objs_id(place_id):
    """Retrieves the list of all Place objects with a specified id."""
    obj = storage.get(Place, place_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete(place_id):
    """Deletes an object."""
    obj = storage.get(Place, place_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update(place_id):
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
