from src.utils.logger import Logger
from typing import Dict, List, Optional, Tuple
from src.services.repositories.exceptions.battle_log import InvalidBattleLogLine
from src.enums.game_types import GAME_TYPES
from src.enums.battle_log_sections import BATTLE_LOG_SECTIONS
from src.entities.pokemon import Pokemon
from src.entities.battle_log import BattleLog


class BattleLogParser():

  def __init__(self):
    self.pokemon_name_mapping: Dict[str, Dict[str, str]] = {}

  @staticmethod
  def parse_player_name(player_name: str) -> str:
    return player_name[:2]

  @staticmethod
  def parse_pokemon_name(pokemon_name: str) -> str:
    # Pokemon are named as '<Name>, L<Level>, <Gender>'
    return pokemon_name.split(', ')[0]

  def parse(self, log: str) -> BattleLog:
    battle_log = BattleLog()
    
    log_section: BATTLE_LOG_SECTIONS = BATTLE_LOG_SECTIONS.GAME_PREVIEW
    handler_by_section = {
      BATTLE_LOG_SECTIONS.GAME_PREVIEW: self.parse_game_preview_line,
      BATTLE_LOG_SECTIONS.TEAM_PREVIEW: self.parse_team_preview_line,
      BATTLE_LOG_SECTIONS.BATTLE: self.parse_battle_line,
      BATTLE_LOG_SECTIONS.POSBATTLE: lambda x, y: None,
    }

    for raw_line in log.split('\n'):
      Logger().debug(f'Parsing: {raw_line}')
      line = list(filter(lambda x: x, raw_line.split('|')))
      if len(line) == 0:
        Logger().debug(f'Skipping empty line')
        continue
      
      log_section = self.update_battle_section(line) or log_section
      handler_by_section[log_section](line, battle_log)
    
    Logger().info(f'Finished parsing the battle log')
    return battle_log

  def update_battle_section(self, line: List[str]) -> Optional[BATTLE_LOG_SECTIONS]:
    if len(line) == 1:
      if line[0] == 'clearpoke':
        Logger().info(f'Starting {BATTLE_LOG_SECTIONS.TEAM_PREVIEW} section')
        return BATTLE_LOG_SECTIONS.TEAM_PREVIEW
      elif line[0] == 'start':
        Logger().info(f'Starting {BATTLE_LOG_SECTIONS.BATTLE} section')
        return BATTLE_LOG_SECTIONS.BATTLE
    elif len(line) == 2:
      if line[0] == 'win':
        Logger().info(f'Starting {BATTLE_LOG_SECTIONS.POSBATTLE} section')
        return BATTLE_LOG_SECTIONS.POSBATTLE

  def parse_game_preview_line(self, line: List[str], battle_log: BattleLog) -> None:
    if len(line) == 1:
      if line[0] == 'rated':
        battle_log.rated = True
        Logger().debug(f'Game set to rated')
    elif len(line) == 2:
      if line[0] == 'gametype':
        battle_log.game_type = GAME_TYPES(line[1])
        Logger().debug(f'Game set to {battle_log.game_type} battle')
      elif line[0]  == 'gen':
        battle_log.generation = int(line[1])
        Logger().debug(f'Game using GEN {battle_log.generation} pokemon')
      # elif line[0] == 'tier':
      #   self.tier = TIERS(line[1][-2: ])

  def parse_team_preview_line(self, line: List[str], battle_log: BattleLog) -> None:
    if len(line) == 3 and line[0] == 'poke':
      if line[0] == 'poke':
        pokemon_name = self.parse_pokemon_name(line[2])
        battle_log.teams[line[1]].add(Pokemon(pokemon_name))

  def parse_battle_line(self, line: List[str], battle_log: BattleLog) -> None:

    def expect_segments(num_segments: int) -> None:
      if len(line) < num_segments:
        raise InvalidBattleLogLine
    
    def parse_header_segments() -> Tuple[str, str]:
      expect_segments(2)
      raw_player, pokemon_nickname = line[1].split(': ')
      player = self.parse_player_name(raw_player)
      pokemon_name = self.pokemon_name_mapping[player][pokemon_nickname]
      return pokemon_name, player

    action = line[0]
    if action == 'turn':
      expect_segments(2)
      battle_log.current_turn = int(line[1])
      Logger().debug(f'Starting turn {battle_log.current_turn}')
    elif action == 'switch' or action == 'drag':
      expect_segments(3)
      pokemon_name = self.parse_pokemon_name(line[2])
      raw_player, pokemon_nickname = line[1].split(': ')
      player = self.parse_player_name(raw_player)
      battle_log.add_pokemon(pokemon_name, player)
      self.pokemon_name_mapping.setdefault(player, {}).setdefault(pokemon_nickname, pokemon_name)
    elif action == '-enditem':
      expect_segments(3)
      pokemon, player = parse_header_segments()
      battle_log.set_pokemon_item(pokemon, player, line[2])
    elif action == '-ability':
      expect_segments(3)
      pokemon, player = parse_header_segments()
      battle_log.set_pokemon_ability(pokemon, player, line[2])
    elif action == 'move':
      expect_segments(3)
      pokemon, player = parse_header_segments()
      battle_log.add_pokemon_move(pokemon, player, line[2])
    
    
    for index, message in enumerate(line):
      if '[from] ability' in message:
        ability = message.split(': ')[1]

        if len(line) > index + 1 and '[of]' in line[index + 1]:
          raw_player, pokemon_nickname = line[index + 1].split(': ')
          player = self.parse_player_name(raw_player.replace('[of] ', ''))
          pokemon_name = self.pokemon_name_mapping[player][pokemon_nickname]
        else:
          raw_player, pokemon_nickname = line[1].split(': ')
          player = self.parse_player_name(raw_player)
          pokemon_name = self.pokemon_name_mapping[player][pokemon_nickname]

        battle_log.set_pokemon_ability(pokemon_name, player, ability)
      if '[from] item' in message:
        item = message.split(': ')[1]
        raw_player, pokemon_nickname = line[1].split(': ')
        player = self.parse_player_name(raw_player)
        pokemon_name = self.pokemon_name_mapping[player][pokemon_nickname]

        battle_log.set_pokemon_item(pokemon_name, player, item)