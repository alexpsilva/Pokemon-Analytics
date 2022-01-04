from src.utils.logger import Logger
from typing import List, Optional
from src.types.entities.pokemon import Pokemon

class Team():
  def __init__(self, pokemon: Optional[List[Pokemon]] = None):
    self.pokemon = pokemon or []
  
  def __repr__(self):
    return '\n\n'.join([str(i) for i in self.pokemon])
  
  def __contains__(self, pokemon: Pokemon):
    return pokemon in self.pokemon

  def add(self, pokemon: Pokemon) -> None:
    self.pokemon.append(pokemon)
  
  def get(self, pokemon: Pokemon) -> Optional[Pokemon]:
    possible = [i for i in self.pokemon if i == pokemon]
    return possible[0] if possible else None
  
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
      
      pokemon.moves = list(set(pokemon.moves + other_pokemon.moves))
    Logger().debug(f'Finished merging teams')
      




  