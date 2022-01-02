from src.types.pokemon import Pokemon
from src.types.enums.tiers import TIERS
from src.exceptions.battle_log import InvalidGameType, InvalidPlayer, InvalidPokemon, InvalidTier
from src.types.enums.game_types import GAME_TYPES
from src.types.enums.battle_log_sections import BATTLE_LOG_SECTIONS
from typing import Dict, List, Optional, Set, TypedDict

class PlayerMapping(TypedDict):
  p1: Optional[str]
  p2: Optional[str]

class TeamMapping(TypedDict):
  p1: List[Pokemon]
  p2: List[Pokemon]

class BattleLog():
  players: PlayerMapping = {'p1': None, 'p2': None}
  teams: TeamMapping = {'p1': [], 'p2': []}
  game_type: GAME_TYPES
  generation: int
  tier: TIERS
  rated: bool
  current_section: BATTLE_LOG_SECTIONS = BATTLE_LOG_SECTIONS.GAME_PREVIEW
  current_turn: int = 1
  
  def __init__(self, log: str):
    def update_battle_section(line: List[str]) -> None:
      if len(line) == 1:
        if line[0] == 'clearpoke':
          self.current_section = BATTLE_LOG_SECTIONS.TEAM_PREVIEW
        elif line[0] == 'start':
          self.current_section = BATTLE_LOG_SECTIONS.BATTLE
      elif len(line) == 2:
        if line[0] == 'win':
          self.current_section = BATTLE_LOG_SECTIONS.POSBATTLE

    def parse_game_preview_line(line: List[str]) -> None:
      if len(line) == 1:
        if line[0] == 'rated':
          self.rated = True
      elif len(line) == 2:
        if line[0] == 'gametype':
          self.game_type = self.map_log_to_gametype(line[1])
        elif line[0]  == 'gen':
          self.generation = int(line[1])
        elif line[0] == 'tier':
          self.tier = self.map_log_to_tier(line[1])
      elif len(line) == 5:
        if line[0] == 'player':
          self.players[line[1]] = line[2]

    def parse_team_preview_line(line: List[str]) -> None:
      if len(line) == 3 and line[0] == 'poke':
        if line[0] == 'poke':
          pokemon_name = line[2].split(', ')[0] # Pokemon are named as '<Name>, <Gender>'
          self.teams[line[1]].append(Pokemon(pokemon_name))

    def parse_battle_line(line: List[str]) -> None:
      if len(line) == 2:
        if line[0] == 'turn':
          self.current_turn = int(line[1])
      elif len(line) == 4:
        if line[0] == '-ability':
          raw_player, pokemon_name = line[1].split(': ')

          if raw_player == 'p1a':
            player = 'p1'
          elif raw_player == 'p2a':
            player = 'p2'
          else:
            raise InvalidPlayer

          possible_pokemon = [i for i in self.teams[player] if i.name == pokemon_name]
          if len(possible_pokemon) != 1:
            raise InvalidPokemon
          pokemon = possible_pokemon[0]

          pokemon.set_ability(line[2])
        elif line[0] == 'move':
          raw_player, pokemon_name = line[1].split(': ')

          if raw_player == 'p1a':
            player = 'p1'
          elif raw_player == 'p2a':
            player = 'p2'
          else:
            raise InvalidPlayer

          possible_pokemon = [i for i in self.teams[player] if i.name == pokemon_name]
          if len(possible_pokemon) != 1:
            raise InvalidPokemon
          pokemon = possible_pokemon[0]

          pokemon.add_move(line[2])
            

    handler_by_section = {
      BATTLE_LOG_SECTIONS.GAME_PREVIEW: parse_game_preview_line,
      BATTLE_LOG_SECTIONS.TEAM_PREVIEW: parse_team_preview_line,
      BATTLE_LOG_SECTIONS.BATTLE: lambda x: None,
      BATTLE_LOG_SECTIONS.POSBATTLE: lambda x: None,
    }

    for raw_line in log.split('\n'):
      line = list(filter(lambda x: x, raw_line.split('|')))
      if len(line) == 0:
        continue
      
      update_battle_section(line)
      # print(f'({self.current_section.value}) {line}')
      handler_by_section[self.current_section](line)
    
    print(f'players: {self.players}')
    print(f'teams: {self.teams}')
    print(f'game_type: {self.game_type}')
    print(f'generation: {self.generation}')
    print(f'tier: {self.tier}')
    print(f'rated: {self.rated}')
    print(f'current_section: {self.current_section}')
    

  @staticmethod
  def map_log_to_gametype(raw: str) -> GAME_TYPES:
    if raw == 'singles':
      return GAME_TYPES.SINGLES
    elif raw == 'doubles':
      return GAME_TYPES.DOUBLES
    else:
      raise InvalidGameType

  @staticmethod
  def map_log_to_tier(raw: str) -> TIERS:
    if raw[-2:] == 'OU':
      return TIERS.OU
    elif raw[-2:] == 'UU':
      return TIERS.UU
    elif raw[-2:] == 'NU':
      return TIERS.NU
    elif raw[-2:] == 'RU':
      return TIERS.RU
    else:
      raise InvalidTier
