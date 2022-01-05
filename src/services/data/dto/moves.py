from typing import Dict, Optional, TypedDict

class SecondaryEffect(TypedDict):
  chance: int
  boosts: Dict[str, int]

class MoveResponseEntry(TypedDict):
  num: int
  accuracy: bool
  basePower: int
  category: str
  isNonstandard: str
  name: str
  pp: int
  priority: int
  flags: Dict
  isZ: str
  critRatio: int
  secondary: Optional[SecondaryEffect]
  target: str
  type: str
  contestType: str
  desc: str
  shortDesc: str

MovesResponse = Dict[str, MoveResponseEntry]
