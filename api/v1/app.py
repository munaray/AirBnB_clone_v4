#!/usr/bin/python3
"""API routes for the app"""
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from os import getenv

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})

HBNB_API_HOST = getenv('HBNB_API_HOST') or '0.0.0.0'
HBNB_API_PORT = getenv('HBNB_API_PORT') or 5000

app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown_db(exception):
    """Close storage"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Return JSON error"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
