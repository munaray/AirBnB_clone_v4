#!/usr/bin/python3
"""Defines a route /status on the object app_views that returns a JSON"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns a JSON"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    """Returns a JSON"""
    from models import storage
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    return jsonify({key: storage.count(value) for key, value in classes.items()})
