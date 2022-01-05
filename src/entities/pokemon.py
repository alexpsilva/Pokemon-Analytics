from src.utils.logger import Logger
from typing import List, Optional

from src.entities.move import Move

class Pokemon():
  def __init__(
    self, 
    name: str, 
    ability: Optional[str] = None, 
    item: Optional[str] = None, 
    moves: Optional[List[Move]] = []
  ): 
    self.name: str = name
    self.ability: Optional[str] = ability
    self.item: Optional[str] = item
    self.moves: List[Move] = moves or []
  
  def __repr__(self) -> str:
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
  
  def __eq__(self, other) -> bool:
    return self.name == other.name
  
  def set_ability(self, ability: str) -> None:
    self.ability = ability

  def set_item(self, item: str) -> None:
    self.item = item

  def add_move(self, move: Move) -> None:
    if move in self.moves:
      Logger().info(f'Did not teach {move.name} to {self.name} because it already knows this move')
      return

    self.moves.append(move)

    if len(self.moves) > 4:
      Logger().warn(f'{self.name} has learned his {len(self.moves)}th move')
    