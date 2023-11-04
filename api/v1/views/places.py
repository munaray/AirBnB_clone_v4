#!/usr/bin/python3
"""View for Place objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects"""
    city = storage.get(City, city_id)
    if city:
        return jsonify([place.to_dict() for place in city.places])
    abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'user_id' not in request.get_json():
            abort(400, 'Missing user_id')
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        user = storage.get(User, request.get_json()['user_id'])
        if user:
            new_place = Place(**request.get_json())
            new_place.city_id = city_id
            new_place.save()
            return jsonify(new_place.to_dict()), 201
        abort(404)
    abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, 'Not a JSON')
        for key, value in request.get_json().items():
            if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
                setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """Retrieves all Place objects depending of the JSON in the body"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    places = storage.all(Place).values()
    if 'states' in request.get_json() and len(request.get_json()['states']) > 0:
        places = [place for place in places if place.city.state_id in request.get_json()['states']]
    if 'cities' in request.get_json() and len(request.get_json()['cities']) > 0:
        places = [place for place in places if place.city_id in request.get_json()['cities']]
    if 'amenities' in request.get_json() and len(request.get_json()['amenities']) > 0:
        places = [place for place in places if all(amenity.id in [amenity.id for amenity in place.amenities] for amenity in request.get_json()['amenities'])]
    return jsonify([place.to_dict() for place in places])
