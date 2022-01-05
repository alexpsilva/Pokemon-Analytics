from src.services.repositories.pokemon import PokemonService
from src.services.repositories.move import MoveService
from typing import Optional, TypedDict

from src.services.repositories.exceptions.battle_log import PokemonNotInTeam

from src.utils.logger import Logger

from src.enums.tiers import TIERS
from src.enums.game_types import GAME_TYPES
from src.entities.team import Team


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
    pokemon = self.teams[player].get(pokemon_name)
    if pokemon is None:
      self.teams[player].add(PokemonService().get_pokemon(pokemon_name))
      Logger().debug(f'Adding {pokemon_name} to {player}\'s team')

  def set_pokemon_item(self, pokemon_name: str, player: str, item: str) -> None:
    pokemon = self.teams[player].get(pokemon_name)
    if pokemon is None:
      Logger().error(f'{pokemon_name} is not a part of {player}\'s team. Currently, it has:')
      Logger().error(self.teams[player])
      raise PokemonNotInTeam

    pokemon.set_item(item)
    Logger().debug(f'Setting {player}\'s {pokemon_name} item to {item}')

  def set_pokemon_ability(self, pokemon_name: str, player: str, ability: str) -> None:
    pokemon = self.teams[player].get(pokemon_name)
    if pokemon is None:
      Logger().error(f'{pokemon_name} is not a part of {player}\'s team. Currently, it has:')
      Logger().error(self.teams[player])
      raise PokemonNotInTeam

    pokemon.set_ability(ability)
    Logger().debug(f'Setting {player}\'s {pokemon_name} ability to {ability}')
  
  def add_pokemon_move(self, pokemon_name: str, player: str, move_name: str) -> None:
    pokemon = self.teams[player].get(pokemon_name)
    if pokemon is None:
      Logger().error(f'{pokemon_name} is not a part of {player}\'s team. Currently, it has:')
      Logger().error(self.teams[player])
      raise PokemonNotInTeam

    move = MoveService().get_move(move_name)
    pokemon.add_move(move)
    Logger().debug(f'Adding move {move} to {player}\'s {pokemon_name}')