from src.types.enums.types import TYPES
from src.exceptions.pokemon import InvalidMove
from src.repositories.move import MoveRepository

class Move():
  name: str
  type: TYPES
  
  accuracy: int
  base_power: int
  priority: int
  max_pp: int
  current_pp: int

  def __init__(self, name):
    data = MoveRepository().get_move(name)
    if data is None:
      raise InvalidMove

    self.name = name
    self.max_pp = data['pp']
    self.current_pp = self.max_pp
    self.type = TYPES(data['type'])
    self.priority = data['priority']
    self.accuracy = data['accuracy']
    self.base_power = data['basePower']

  def __repr__(self):
    return f'{self.name} ({self.current_pp}/{self.max_pp})'
  
  def __eq__(self, other):
    return self.name == other.name