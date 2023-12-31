#!/usr/bin/python3
"""View for the link between Place objects and Amenity objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'], strict_slashes=False)
def get_amenities(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify([amenity.to_dict() for amenity in place.amenities])
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(place_id, amenity_id):
    """Deletes a Amenity object"""
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if amenity in place.amenities:
                storage.delete(amenity)
                storage.save()
                return jsonify({})
            abort(404)
        abort(404)
    abort(404)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'], strict_slashes=False)
def post_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    place = storage.get(Place, place_id)
    if place:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            if amenity in place.amenities:
                return jsonify(amenity.to_dict())
            place.amenities.append(amenity)
            storage.save()
            return jsonify(amenity.to_dict())
        abort(404)
    abort(404)
