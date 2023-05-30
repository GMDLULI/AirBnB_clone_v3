#!/usr/bin/python3
"""State module """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_all_states():
    """gets all objects by id"""
    all_obj = []
    for state in storage.all("State").values():
        all_obj.append(state.to_dict())
    return jsonify(all_obj)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_method_state(state_id):
    """gets state by id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def del_method_state(state_id):
    """deletes state"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}, 200))


@app_views.route('/states', methods=['POST'])
def create_state():
    """creates a state"""
    if not request.get_json():
        return make_reponse(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in request.get_json():
        return make_reposnse(jsonify({"error": "Missing name"}), 400)

    state = State()
    state.name = request.get_json()['name']
    state.save()
    storage.new(state)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_method(state_id):
    """updates states method"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(state, key, value)
    storage.save()

    return make_response(jsonify(obj.to_dict(), 200))
