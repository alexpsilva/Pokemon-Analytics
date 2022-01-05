from src.enums.types import TYPES
from typing import Dict

from .exceptions.move import InvalidMove

from src.entities.move import Move

from src.utils.logger import Logger
from src.utils.singleton import Singleton

from src.services.data.showdown import ShowdownAPI
from src.services.data.dto.moves import MoveResponseEntry

class MoveService(metaclass=Singleton):
  _data: Dict[str, MoveResponseEntry] = {}

  def __init__(self):
    Logger().info(f'Initializing Move repository')
    response = ShowdownAPI().moves()
    self._data = {m['name']: m for m in response.values()}

  def get_move(self, name: str) -> Move:
    if name not in self._data:
      Logger().error(f'There is no "{name}" move in the current pokedex')
      raise InvalidMove
    data = self._data[name]
    return Move(
      data['name'], 
      data['pp'],
      TYPES(data['type']),
      data['accuracy'],
      data['priority'],
      data['basePower']
    )
  

