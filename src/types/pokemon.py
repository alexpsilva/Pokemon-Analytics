from src.types.move import Move
from typing import List, Optional

class Pokemon():
  def __init__(self, name: str):
    self.name = name
    self.ability: Optional[str] = None
    self.moves: List[Move] = []
  
  def __repr__(self):
    moves_str = '\n'.join([f' - {move}' for move in self.moves])
    return f'{self.name} ({self.ability}):\n{moves_str}'
  
  def __eq__(self, other):
    return self.name == other.name
  
  def set_ability(self, ability: str):
    self.ability = ability

  def add_move(self, move: str):
    if len([i for i in self.moves if i.name == move]) == 0:
      self.moves.append(Move(move))