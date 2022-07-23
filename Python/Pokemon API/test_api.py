import requests
import os
import random
import pytest
from pymongo import MongoClient
from classes import Pokemon

TEST_HOST = "http://localhost:5000"
client = MongoClient(os.getenv('mongo'))
db = client.pokemon
col = db.Pokemons


class TestPokemonApi:
    @pytest.fixture(scope="session")
    def pokemon(self):
        num = random.randint(1, 99999)
        pokemon = Pokemon(name=f"testemon-{num}", generation="3", type="test", number=num,
                          pokedex_entry="test_text")
        print(f"Created pokemon for testing: {pokemon.name}")
        return pokemon

    def get_pokemon_data(self, pokemon):
        data = {
            "name": pokemon.name,
            "generation": pokemon.generation,
            "type": pokemon.type,
            "number": pokemon.number,
            "pokedex_entry": pokemon.pokedex_entry
        }
        return data

    def test_can_create_new_pokemon(self, pokemon):
        data = self.get_pokemon_data(pokemon)
        response = requests.post(url=f"{TEST_HOST}/pokemon", json=data)
        assert response.status_code == 200

    def test_cant_create_pokemon_that_already_exists(self, pokemon):
        data = self.get_pokemon_data(pokemon)
        response = requests.post(url=f"{TEST_HOST}/pokemon", json=data)
        assert response.status_code == 400

    def test_cant_create_pokemon_with_same_number(self, pokemon):
        data = self.get_pokemon_data(pokemon)
        data["name"] = "new_name"
        response = requests.post(url=f"{TEST_HOST}/pokemon", json=data)
        assert response.status_code == 400

    def test_can_delete_existing_pokemon(self, pokemon):
        data = self.get_pokemon_data(pokemon)
        response = requests.delete(url=f"{TEST_HOST}/pokemon", json=data)
        assert response.status_code == 200
