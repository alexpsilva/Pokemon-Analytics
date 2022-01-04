from src.utils.logger import Logger
from src.types.team import Team
from src.types.pokemon import Pokemon
from src.types.enums.tiers import TIERS
from src.exceptions.battle_log import InvalidPokemon
from src.types.enums.game_types import GAME_TYPES
from src.types.enums.battle_log_sections import BATTLE_LOG_SECTIONS
from typing import Dict, List, Optional, Set, TypedDict

class PlayerMapping(TypedDict):
  p1: Optional[str]
  p2: Optional[str]

class TeamMapping(TypedDict):
  p1: Team
  p2: Team

class BattleLog():

  def __init__(self, log: str):
    self.players: PlayerMapping = {'p1': None, 'p2': None}
    self.teams: TeamMapping = {'p1': Team(), 'p2': Team()}
    self.game_type: GAME_TYPES = GAME_TYPES.SINGLES
    self.generation: int = 8
    self.tier: TIERS = TIERS.OU
    self.rated: bool = False
    self.current_section: BATTLE_LOG_SECTIONS = BATTLE_LOG_SECTIONS.GAME_PREVIEW
    self.current_turn: int = 1

    def parse_player(player_name: str) -> str:
      return player_name[:2]

    def update_battle_section(line: List[str]) -> None:
      if len(line) == 1:
        if line[0] == 'clearpoke':
          self.current_section = BATTLE_LOG_SECTIONS.TEAM_PREVIEW
        elif line[0] == 'start':
          self.current_section = BATTLE_LOG_SECTIONS.BATTLE
      elif len(line) == 2:
        if line[0] == 'win':
          self.current_section = BATTLE_LOG_SECTIONS.POSBATTLE
      Logger().info(f'Starting {self.current_section} section')

    def parse_game_preview_line(line: List[str]) -> None:
      if len(line) == 1:
        if line[0] == 'rated':
          self.rated = True
          Logger().debug(f'Game set to rated')
      elif len(line) == 2:
        if line[0] == 'gametype':
          self.game_type = GAME_TYPES(line[1])
          Logger().debug(f'Game set to {self.game_type} battle')
        elif line[0]  == 'gen':
          self.generation = int(line[1])
          Logger().debug(f'Game using GEN {self.generation} pokemon')
        # elif line[0] == 'tier':
        #   self.tier = TIERS(line[1][-2: ])
      elif len(line) == 5:
        if line[0] == 'player':
          player_id = line[1]
          player_name = line[2]
          self.players[player_id] = player_name
          Logger().debug(f'Player {player_id} named {player_name}')

    def parse_team_preview_line(line: List[str]) -> None:
      if len(line) == 3 and line[0] == 'poke':
        if line[0] == 'poke':
          pokemon_name = line[2].split(', ')[0] # Pokemon are named as '<Name>, <Gender>'
          self.teams[line[1]].add(Pokemon(pokemon_name))

    def parse_battle_line(line: List[str]) -> None:
      if len(line) == 2:
        if line[0] == 'turn':
          self.current_turn = int(line[1])
          Logger().debug(f'Starting turn {self.current_turn}')
      elif len(line) == 4 or len(line) == 5:
        if line[0] == 'switch':
          raw_player, pokemon_name = line[1].split(': ')
          player = parse_player(raw_player)

          if Pokemon(pokemon_name) not in self.teams[player]:
            self.teams[player].add(Pokemon(pokemon_name))
            Logger().debug(f'Adding {pokemon_name} to {player}\'s team')
        elif line[0] == '-ability':
          raw_player, pokemon_name = line[1].split(': ')
          player = parse_player(raw_player)
          ability = line[2]

          pokemon = self.teams[player].get(Pokemon(pokemon_name))
          if pokemon is None:
            Logger().error(f'{pokemon_name} is not a part of {player}\'s team. Currently, it has:')
            Logger().error(self.teams[player])
            raise InvalidPokemon

          pokemon.set_ability(ability)
          Logger().debug(f'Setting {player}\'s ability to {ability}')
        elif line[0] == 'move':
          raw_player, pokemon_name = line[1].split(': ')
          player = parse_player(raw_player)
          move = line[2]

          pokemon = self.teams[player].get(Pokemon(pokemon_name))
          if pokemon is None:
            Logger().error(f'{pokemon_name} is not a part of {player}\'s team. Currently, it has:')
            Logger().error(self.teams[player])
            raise InvalidPokemon

          pokemon.add_move(move)
          Logger().debug(f'Adding move {move} to {player}\'s {pokemon_name}')
            

    handler_by_section = {
      BATTLE_LOG_SECTIONS.GAME_PREVIEW: parse_game_preview_line,
      BATTLE_LOG_SECTIONS.TEAM_PREVIEW: lambda x: None,
      BATTLE_LOG_SECTIONS.BATTLE: parse_battle_line,
      BATTLE_LOG_SECTIONS.POSBATTLE: lambda x: None,
    }

    for raw_line in log.split('\n'):
      Logger().debug(f'Parsing: {raw_line}')
      line = list(filter(lambda x: x, raw_line.split('|')))
      if len(line) == 0:
        Logger().debug(f'Skipping empty line')
        continue
      
      update_battle_section(line)
      handler_by_section[self.current_section](line)
    
    # print(f'players: {self.players}')
    # print(f'teams: {self.teams}')
    # print(f'game_type: {self.game_type}')
    # print(f'generation: {self.generation}')
    # print(f'tier: {self.tier}')
    # print(f'rated: {self.rated}')
    # print(f'current_section: {self.current_section}')
