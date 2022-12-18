#!/usr/bin/python3
"""Starting the connection."""


from api.v1.views import app_views
from flask import Flask, make_response, jsonify
from models import storage
import os

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """
    After each request, this method .close() on
    the current SQLAlchemy Session
    """
    storage.close()


@app.errorhandler(404)
def handler_404(exception):
    """
    Handles 404 errors.
    """
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    host_api = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port_api = os.getenv('HBNB_API_PORT', 5000)

    app.run(port=port_api, host=host_api, threaded=True)
