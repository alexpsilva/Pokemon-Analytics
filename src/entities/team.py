from typing import List, Optional

from src.utils.logger import Logger

from src.entities.pokemon import Pokemon
from src.services.repositories.pokemon import PokemonService

class Team():
  def __init__(self, pokemon: Optional[List[Pokemon]] = None):
    self.pokemon = pokemon or []
  
  def __repr__(self):
    return '\n\n'.join([str(i) for i in self.pokemon])
  
  def __contains__(self, pokemon: Pokemon):
    return pokemon in self.pokemon

  def add(self, pokemon: Pokemon) -> None:
    self.pokemon.append(pokemon)
  
  def get_pokemon(self, pokemon_name: str) -> Optional[Pokemon]:
    # Fetch a Pokemon instance because the 'name' may change
    pokemon = PokemonService().get_pokemon(pokemon_name) 
    candidates = [i for i in self.pokemon if i.name == pokemon.name]
    return candidates[0] if candidates else None
  
  def merge(self, other: 'Team') -> None:
    other_pokemon_by_name = {pokemon.name: pokemon for pokemon in other.pokemon}
    for pokemon in self.pokemon:
      other_pokemon = other_pokemon_by_name.get(pokemon.name)
      if other_pokemon is None:
        Logger().warn(f'Ignoring divergent pokemon while merging teams: {pokemon.name}')
        continue
    
      abilities = list({i for i in [other_pokemon.ability, pokemon.ability] if i is not None})
      if len(abilities) > 1:
        Logger().warn(f'Found two {pokemon.name} with different abilities ({pokemon.ability} / {other_pokemon.ability})')
      elif len(abilities) == 1:
        pokemon.ability = abilities[0]

      items = list({i for i in [other_pokemon.item, pokemon.item] if i is not None})
      if len(items) > 1:
        Logger().warn(f'Found two {pokemon.name} with different items ({pokemon.item} / {other_pokemon.item})')
      elif len(items) == 1:
        pokemon.item = items[0]
      
      pokemon.moves = list(set(pokemon.moves + other_pokemon.moves))
    Logger().debug(f'Finished merging teams')
      




  