from src.utils.logger import Logger
from typing import Dict, Optional
from src.services.data.dto.moves import MoveResponseEntry
from src.utils.singleton import Singleton
import src.services.data.showdown

class MoveService(metaclass=Singleton):
  _data: Dict[str, MoveResponseEntry] = {}

  def __init__(self):
    Logger().info(f'Initializing Move repository')
    response = src.services.data.showdown.ShowdownAPI().moves()

    for raw_move in response.values():
      self._data[raw_move['name']] = {
        'num': raw_move['num'],
        'accuracy': raw_move['accuracy'],
        'basePower': raw_move['basePower'],
        'category': raw_move['category'],
        'isNonstandard': raw_move.get('isNonstandard'),
        'name': raw_move['name'],
        'pp': raw_move['pp'],
        'priority': raw_move['priority'],
        'flags': raw_move['flags'],
        'isZ': raw_move.get('isZ'),
        'critRatio': raw_move.get('critRatio'),
        'secondary': raw_move.get('secondary'),
        'target': raw_move['target'],
        'type': raw_move['type'],
        'contestType': raw_move.get('contestType'),
        'desc': raw_move.get('desc'),
        'shortDesc': raw_move.get('shortDesc'),
      }

  def get_move(self, name: str) -> Optional[MoveResponseEntry]:
    return self._data.get(name)
  

