#!/usr/bin/python3
"""
Create a new view for Reviw objects
that handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from flask import jsonify, make_response, request


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review_per_place(place_id):
    """Review route to handle http method for requested reviews by place."""

    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)

    all_review = storage.all(Review)
    review_places = [obj.to_dict() for obj in all_review.values()
                     if obj.place_id == place_id]
    return jsonify(review_places)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def retrieve_review_objs_id(review_id):
    """Retrieves the list of all Place objects with a specified id."""
    obj = storage.get(Review, review_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletes_places_reviews_route(review_id):
    """Deletes an object."""
    obj = storage.get(Review, review_id)
    if obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_place_review_route(place_id):
    req_json = request.get_json()
    if req_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    else:
        if 'text' not in req_json:
            return make_response(jsonify({'error': 'Missing text'}), 400)
        if 'user_id' not in req_json:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)

    place_obj = storage.get(Place, place_id)
    user_obj = storage.get(User, req_json['user_id'])

    if place_obj is None or user_obj is None:
        return make_response(jsonify({'error': 'Not found'}), 404)
    else:
        new_instance = Review(**req_json)
        new_instance.place_id = place_id
        new_instance.save()

    return make_response(jsonify(new_instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def updates_places_reviews_route(review_id):
    """Updates an object."""
    obj = storage.get(Review, review_id)
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
