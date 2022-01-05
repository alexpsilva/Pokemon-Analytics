from typing import Dict

from .exceptions.pokemon import InvalidPokemon

from src.entities.pokemon import Pokemon

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
      self._data[raw_pokemon['name']] = raw_pokemon
      for cosmetic_form in raw_pokemon.get('cosmeticFormes', []):
        self._data[cosmetic_form] = raw_pokemon

  def get_pokemon(self, name: str) -> Pokemon:
    if name not in self._data:
      Logger().error(f'There is no "{name}" pokemon in the current pokedex')
      raise InvalidPokemon
    
    data = self._data[name]
    params = {'name': data['name']}
    
    possible_abilities = data['abilities']
    if len(possible_abilities.values()) == 1:
      params['ability'] = possible_abilities['0']

    return Pokemon(**params)
  

