from typing import List, Optional
from src.types.pokemon import Pokemon

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
  
  