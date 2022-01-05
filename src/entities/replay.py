from typing import Dict, Optional

from src.services.repositories.exceptions.replay import PokemonNotInTeam

from src.utils.logger import Logger

from src.enums.tiers import TIERS
from src.enums.game_types import GAME_TYPES
from src.enums.player_position import PLAYER_POSITION
from src.entities.team import Team

from src.services.repositories.pokemon import PokemonService
from src.services.repositories.move import MoveService


class Replay():

  def __init__(self):
    self.players: Dict[PLAYER_POSITION, Optional[str]] = {
      PLAYER_POSITION.P1: None, 
      PLAYER_POSITION.P2: None
    }
    self.teams: Dict[PLAYER_POSITION, Team] = {
      PLAYER_POSITION.P1: Team(), 
      PLAYER_POSITION.P2: Team(),
    }
    self.game_type: GAME_TYPES = GAME_TYPES.SINGLES
    self.generation: int = 8
    self.tier: TIERS = TIERS.OU
    self.rated: bool = False
    self.current_turn: int = 1
  
  def add_pokemon(self, pokemon_name: str, player: PLAYER_POSITION) -> None:
    pokemon = self.teams[player].get_pokemon(pokemon_name)
    if pokemon is None:
      self.teams[player].add(PokemonService().get_pokemon(pokemon_name))
      Logger().debug(f'Adding {pokemon_name} to {player}\'s team')

  def set_pokemon_item(self, pokemon_name: str, player: PLAYER_POSITION, item: str) -> None:
    pokemon = self.teams[player].get_pokemon(pokemon_name)
    if pokemon is None:
      Logger().error(f'{pokemon_name} is not a part of {player}\'s team. Currently, it has:')
      Logger().error(f'\n{self.teams[player]}\n')
      raise PokemonNotInTeam

    pokemon.set_item(item)
    Logger().debug(f'Setting {player}\'s {pokemon_name} item to {item}')

  def set_pokemon_ability(self, pokemon_name: str, player: PLAYER_POSITION, ability: str) -> None:
    pokemon = self.teams[player].get_pokemon(pokemon_name)
    if pokemon is None:
      Logger().error(f'{pokemon_name} is not a part of {player}\'s team. Currently, it has:')
      Logger().error(f'\n{self.teams[player]}\n')
      raise PokemonNotInTeam

    pokemon.set_ability(ability)
    Logger().debug(f'Setting {player}\'s {pokemon_name} ability to {ability}')
  
  def add_pokemon_move(self, pokemon_name: str, player: PLAYER_POSITION, move_name: str) -> None:
    pokemon = self.teams[player].get_pokemon(pokemon_name)
    if pokemon is None:
      Logger().error(f'{pokemon_name} is not a part of {player}\'s team. Currently, it has:')
      Logger().error(f'\n{self.teams[player]}\n')
      raise PokemonNotInTeam

    move = MoveService().get_move(move_name)
    pokemon.add_move(move)
    Logger().debug(f'Adding move {move} to {player}\'s {pokemon_name}')