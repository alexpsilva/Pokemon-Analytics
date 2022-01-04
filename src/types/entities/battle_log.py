from src.utils.logger import Logger
from typing import Optional, TypedDict
from src.exceptions.battle_log import InvalidPokemon
from src.types.enums.tiers import TIERS
from src.types.enums.game_types import GAME_TYPES
from src.types.entities.team import Team
from src.types.entities.pokemon import Pokemon


class PlayerMapping(TypedDict):
  p1: Optional[str]
  p2: Optional[str]

class TeamMapping(TypedDict):
  p1: Team
  p2: Team

class BattleLog():

  def __init__(self):
    self.players: PlayerMapping = {'p1': None, 'p2': None}
    self.teams: TeamMapping = {'p1': Team(), 'p2': Team()}
    self.game_type: GAME_TYPES = GAME_TYPES.SINGLES
    self.generation: int = 8
    self.tier: TIERS = TIERS.OU
    self.rated: bool = False
    self.current_turn: int = 1
  
  def add_pokemon(self, pokemon_name: str, player: str) -> None:
    if Pokemon(pokemon_name) not in self.teams[player]:
      self.teams[player].add(Pokemon(pokemon_name))
      Logger().debug(f'Adding {pokemon_name} to {player}\'s team')

  def set_pokemon_item(self, pokemon_name: str, player: str, item: str) -> None:
    pokemon = self.teams[player].get(Pokemon(pokemon_name))
    if pokemon is None:
      Logger().error(f'{pokemon_name} is not a part of {player}\'s team. Currently, it has:')
      Logger().error(self.teams[player])
      raise InvalidPokemon

    pokemon.set_item(item)
    Logger().debug(f'Setting {player}\'s {pokemon_name} item to {item}')

  def set_pokemon_ability(self, pokemon_name: str, player: str, ability: str) -> None:
    pokemon = self.teams[player].get(Pokemon(pokemon_name))
    if pokemon is None:
      Logger().error(f'{pokemon_name} is not a part of {player}\'s team. Currently, it has:')
      Logger().error(self.teams[player])
      raise InvalidPokemon

    pokemon.set_ability(ability)
    Logger().debug(f'Setting {player}\'s {pokemon_name} ability to {ability}')
  
  def add_pokemon_move(self, pokemon_name: str, player: str, move: str) -> None:
    pokemon = self.teams[player].get(Pokemon(pokemon_name))
    if pokemon is None:
      Logger().error(f'{pokemon_name} is not a part of {player}\'s team. Currently, it has:')
      Logger().error(self.teams[player])
      raise InvalidPokemon

    pokemon.add_move(move)
    Logger().debug(f'Adding move {move} to {player}\'s {pokemon_name}')