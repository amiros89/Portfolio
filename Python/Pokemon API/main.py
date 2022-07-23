from flask import Flask, jsonify, request
from pymongo import MongoClient
from classes import Pokemon
import json
import os

app = Flask(__name__)

client = MongoClient(os.getenv('mongo'))
db = client.pokemon
col = db.Pokemons


@app.route('/')
def index():
    return jsonify({'Message': 'Welcome to Pokemon API!'})


@app.route('/pokemon', methods=["POST"])
def create_pokemon():
    pokemon = json.loads(request.data)
    if not col.find_one({"name": pokemon["name"]}, {"_id": 0}) and not col.find_one({"number": pokemon["number"]},
                                                                                    {"_id": 0}):
        col.insert_one(pokemon)
        return {}
    else:
        data = {"error": "pokemon already exist"}
        return jsonify(data), 400


@app.route('/pokemon/<string:name>', methods=["GET"])
def get_pokemon(name: str):
    pokemon = col.find_one({"name": name}, {"_id": 0})
    if pokemon:
        return jsonify(pokemon)
    else:
        resp = {"Error": f"Pokemon '{name}' not found"}
        return jsonify(resp), 404


@app.route('/pokemon', methods=["GET"])
def get_all_pokemon():
    documents = [doc for doc in col.find({}, {"_id": 0})]
    return jsonify(documents)


@app.route('/pokemon/<string:name>', methods=["PUT"])
def update_pokemon(name: str):
    exists = col.find_one({"name": name}, {"_id": 0})
    if exists:
        data = json.loads(request.data)
        pokemon = Pokemon(name=data["name"], type=data["type"], generation=data["generation"], number=data["number"],
                          pokedex_entry=data["pokedex_entry"])
        query_filter = {"name": name}
        new_values = {"$set":
            {
                "name": pokemon.name,
                "type": pokemon.type,
                "generation": pokemon.generation,
                "number": pokemon.number,
                "pokedex_entry": pokemon.pokedex_entry
            }
        }
        col.update_one(query_filter, new_values)
        return {}
    else:
        resp = {"Error": f"Pokemon {name} not found"}
        return jsonify(resp), 404


@app.route('/pokemon/<string:name>', methods=["DELETE"])
def delete_pokemon(name: str):
    pokemon = col.find_one({"name": name}, {"_id": 0})
    if pokemon:
        col.delete_one(pokemon)
        return {}
    else:
        data = {"error": "pokemon not found"}
        return jsonify(data), 404


@app.route('/pokemon', methods=["DELETE"])
def delete_all_pokemon():
    col.drop()
    return {}


app.run(host="0.0.0.0")
