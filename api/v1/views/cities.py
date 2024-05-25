#!/usr/bin/python3
"""cities"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State
from datetime import datetime
import uuid


@app_views.route('/states/<state_id>/cities', methods=['GET'])
@app_views.route('/states/<state_id>/cities/', methods=['GET'])
def list_cities_of_state(state_id):
    '''Retrieves a list of all City objects'''
    all_states = storage.all("State").values()
    state_obj = next((obj for obj in all_states if obj.id == state_id), None)
    if not state_obj:
        abort(404)
    list_cities = [city.to_dict() for city in state_obj.cities]
    return jsonify(list_cities)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
@app_views.route('/states/<state_id>/cities/', methods=['POST'])
def create_city(state_id):
    '''Creates a City'''
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    state_obj = storage.get("State", state_id)
    if not state_obj == []:
        abort(404)
    city_data = request.get_json()
    city_data['state_id'] = state_id
    new_city = City(**city_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    '''Retrieves a City object'''
    city_obj = storage.get("City", city_id)
    if not city_obj:
        abort(404)
    return jsonify(city_obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    '''Deletes a City object'''
    city_obj = storage.get("City", city_id)
    if not city_obj:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=['PUT'])
def updates_city(city_id):
    '''Updates a City object'''
    city_obj = storage.get("City", city_id)
    if not city_obj:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    city_data = request.get_json()
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in city_data.items():
        if key not in ignore_keys:
            setattr(city_obj, key, value)
    storage.save()
    return jsonify(city_obj.to_dict()), 200
