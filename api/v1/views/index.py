#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.amenity import Amenity
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.review import Review


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_route():
    """
    Function that returns a JSON with the status.
    """
    if request.method == 'GET':
        resp = {"status": "OK"}
        return jsonify(resp)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats_route():
    """
    Function to return the count of each class instances.
    """
    if request.method == 'GET':
        response = {}
        clases = {
            "amenities": Amenity,
            "cities": City,
            "places": Place,
            "reviews": Review,
            "states": State,
            "users": User
        }
        for key, value in clases.items():
            response[key] = storage.count(value)
        return jsonify(response)
