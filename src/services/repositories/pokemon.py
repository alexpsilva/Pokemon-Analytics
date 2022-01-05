from typing import Dict

from .exceptions.pokemon import InvalidPokemon

from src.utils.logger import Logger
from src.utils.singleton import Singleton

from src.services.data.showdown import ShowdownAPI
from src.services.data.dto.pokemon import PokemonResponseEntry

class PokemonService(metaclass=Singleton):
  _data: Dict[str, PokemonResponseEntry] = {}

  def __init__(self):
    Logger().info(f'Initializing Pokemon repository')
    response = ShowdownAPI().pokemon()

    for raw_pokemon in response.values():
      pokemon_data: PokemonResponseEntry = {
        "num": raw_pokemon['num'],
        "name": raw_pokemon['name'],
        "types": raw_pokemon['types'],
        "genderRatio": raw_pokemon.get('genderRatio'),
        "baseStats": {
          "hp": raw_pokemon['baseStats']['hp'],
          "atk": raw_pokemon['baseStats']['atk'],
          "def": raw_pokemon['baseStats']['def'],
          "spa": raw_pokemon['baseStats']['spa'],
          "spd": raw_pokemon['baseStats']['spd'],
          "spe": raw_pokemon['baseStats']['spe'],
        },
        "abilities": raw_pokemon['abilities'],
        "heightm": raw_pokemon['heightm'],
        "weightkg": raw_pokemon['weightkg'],
        "color": raw_pokemon['color'],
        "evos": raw_pokemon.get('evos') or [],
        "eggGroups": raw_pokemon['eggGroups'],
        "tier": raw_pokemon.get('tier'),
        "cosmeticFormes": raw_pokemon.get('cosmeticFormes') or []
      }
      self._data[raw_pokemon['name']] = pokemon_data
      for cosmetic_form in pokemon_data['cosmeticFormes']:
        self._data[cosmetic_form] = pokemon_data

  def get_pokemon(self, name: str) -> PokemonResponseEntry:
    if name not in self._data:
      Logger().error(f'There is no "{name}" pokemon in the current pokedex')
      raise InvalidPokemon
    return self._data[name]
  

