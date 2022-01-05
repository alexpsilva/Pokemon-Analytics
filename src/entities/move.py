from typing import Optional
from src.enums.types import TYPES

class Move():

  def __init__(
      self, 
      name: str, 
      max_pp: int, 
      type: TYPES, 
      accuracy: float, 
      priority: int = 0, 
      base_power: Optional[int] = None, 
      current_pp: Optional[int] = None
    ):
    self.name: str = name
    self.max_pp: int = max_pp
    self.current_pp: int = current_pp or self.max_pp
    self.type: TYPES = type
    self.priority: int = priority
    self.accuracy: float = accuracy
    self.base_power: Optional[int] = base_power

  def __repr__(self):
    return f'{self.name} ({self.current_pp}/{self.max_pp})'
  
  def __eq__(self, other):
    return self.name == other.name
  
  def __hash__(self):
    return hash(self.name)