from src.utils.logger import Logger
from src.enums.types import TYPES
from src.services.repositories.exceptions.pokemon import InvalidMove
from src.services.repositories.move import MoveService

class Move():
  name: str
  type: TYPES
  
  accuracy: int
  base_power: int
  priority: int
  max_pp: int
  current_pp: int

  def __init__(self, name):
    data = MoveService().get_move(name)
    if data is None:
      Logger().error(f'There is no "{name}" move in the current pokedex')
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
  
  def __hash__(self):
    return hash(self.name)