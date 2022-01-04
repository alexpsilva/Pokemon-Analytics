from src.types.enums.tiers import TIERS
from src.types.enums.types import TYPES
from typing import Dict, Optional, TypedDict, List

PokemonBaseStats = TypedDict('PokemonBaseStats', {
  'hp': int,
  'atk': int,
  'def': int,
  'spa': int,
  'spd': int,
  'spe': int,
})

class PokemonGenderRatio(TypedDict):
  M: float
  F: float

PokemonAbilities = TypedDict('PokemonAbilities', {
  '0': str,
  '1': Optional[str],
  'H': Optional[str],
})

class PokemonResponseEntry(TypedDict):
  num: int
  name: str
  types: List[TYPES]
  genderRatio: Optional[PokemonGenderRatio]
  baseStats: PokemonBaseStats
  abilities: PokemonAbilities
  heightm: float
  weightkg: float
  color: str
  evos: List[str]
  eggGroups: List[str]
  tier: Optional[TIERS]

PokemonResponse = Dict[str, PokemonResponseEntry]