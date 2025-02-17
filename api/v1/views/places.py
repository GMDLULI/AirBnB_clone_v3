#!/usr/bin/python3
"""Place view module"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places")
def all_places(city_id):
    '''Returns a list of all the places'''
    if not storage.get("City", city_id):
        abort(404)

    places_list = []
    for place in storage.all("Place").values():
        if place.city_id == city_id:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>")
def place(place_id):
    '''Returns an instance of the specified object'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=['DELETE'])
def delete_place(place_id):
    '''Deletes the specified place'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    '''Creates the specified test'''
    # Check if city exists
    if not storage.get("City", city_id):
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    user_id = request.get_json().get('user_id')
    if not user_id:
        abort(400, description="Missing user_id")

    if not storage.get("User", user_id):
        abort(404)

    if not request.get_json().get('name'):
        abort(400, description="Missing name")

    place = Place()
    place.name = request.get_json()['name']
    place.city_id = city_id
    place.user_id = user_id
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['PUT'])
def update_place(place_id):
    '''Updates the place with the id passed'''
    place = storage.get("Place", place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k == "id" or k == "created_at" or k == "updated_at" \
           or k == "user_id" or k == "city_id":
            continue
        else:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
