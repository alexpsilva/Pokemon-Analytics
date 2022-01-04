from src.utils.logger import Logger
from typing import List, Optional
from src.exceptions.battle_log import InvalidPokemon
from src.repositories.pokemon import PokemonRepository
from src.types.entities.move import Move

class Pokemon():
  def __init__(self, name: str):
    self.name = name
    self.ability: Optional[str] = None
    self.item: Optional[str] = None
    self.moves: List[Move] = []

    data = PokemonRepository().get_pokemon(name)
    if data is None:
      Logger().error(f'There is no "{name}" pokemon in the current pokedex')
      raise InvalidPokemon

    self.possible_abilities = data['abilities']
    if len(self.possible_abilities.values()) == 1:
      self.ability = self.possible_abilities['0']
  
  def __repr__(self):
    pokemon_str = f'{self.name}'
    moves_str = '\n'.join([f' - {move}' for move in self.moves])

    optionals = []
    if self.ability:
      optionals.append(f'ability: {self.ability}')
    if self.item:
      optionals.append(f'item: {self.item}')
    
    optionals_str = ''
    if optionals:
      optionals_str = ' (' + ' / '.join(optionals) + ')'

    return pokemon_str + optionals_str + ':\n' + moves_str
  
  def __eq__(self, other):
    return self.name == other.name
  
  def set_ability(self, ability: str):
    self.ability = ability

  def set_item(self, item: str):
    self.item = item

  def add_move(self, move: str):
    if len([i for i in self.moves if i.name == move]) == 0:
      self.moves.append(Move(move))