from typing import List


class Move():
  name: str
  max_pp: int
  current_pp: int

  def __init__(self, name):
    self.name = name
  
  def __repr__(self):
    return f'{self.name} ({self.current_pp}/{self.max_pp}'

class Pokemon():
  name: str
  ability: str
  moves: List[Move]

  def __init__(self, name):
    self.name = name
  
  def __repr__(self):
    moves_str = '\n'.join([f' - {move}' for move in self.moves])
    return f'{self.name}:\n{moves_str}'
  
  def set_ability(self, ability: str):
    self.ability = ability

  def add_move(self, move: str):
    self.moves.append(Move(move))