from typing import Dict, List, Optional, Tuple

from .exceptions.replay import InvalidBattleLogLine

from src.utils.logger import Logger

from src.enums.game_types import GAME_TYPES
from src.enums.battle_log_sections import REPLAY_LOG_SECTIONS
from src.enums.player_position import PLAYER_POSITION

from src.entities.replay import Replay

from src.services.repositories.pokemon import PokemonService


class ReplayService():

  def __init__(self):
    self.pokemon_name_mapping: Dict[PLAYER_POSITION, Dict[str, str]] = {}

  @staticmethod
  def parse_player_name(player_name: str) -> PLAYER_POSITION:
    return PLAYER_POSITION(player_name[:2])

  @staticmethod
  def parse_pokemon_name(pokemon_name: str) -> str:
    # Pokemon are named as '<Name>, L<Level>, <Gender>'
    return pokemon_name.split(', ')[0]
  
  @staticmethod
  def expect_line_segments(line: List[str], num_segments: int):
    if len(line) < num_segments:
      raise InvalidBattleLogLine


  def parse(self, log: str) -> Replay:
    replay = Replay()
    log_section: REPLAY_LOG_SECTIONS = REPLAY_LOG_SECTIONS.GAME_PREVIEW

    for raw_line in log.split('\n'):
      Logger().debug(f'Parsing: {raw_line}')
      line = list(filter(lambda x: x, raw_line.split('|')))
      if len(line) == 0:
        Logger().debug(f'Skipping empty line')
        continue
      
      log_section = self.update_battle_section(line) or log_section
      self.parse_log_line(line, replay)
    
    Logger().info(f'Finished parsing the battle log')
    return replay

  def update_battle_section(self, line: List[str]) -> Optional[REPLAY_LOG_SECTIONS]:
    if len(line) == 1:
      if line[0] == 'clearpoke':
        Logger().info(f'Starting {REPLAY_LOG_SECTIONS.TEAM_PREVIEW} section')
        return REPLAY_LOG_SECTIONS.TEAM_PREVIEW
      elif line[0] == 'start':
        Logger().info(f'Starting {REPLAY_LOG_SECTIONS.BATTLE} section')
        return REPLAY_LOG_SECTIONS.BATTLE
    elif len(line) == 2:
      if line[0] == 'win':
        Logger().info(f'Starting {REPLAY_LOG_SECTIONS.POSBATTLE} section')
        return REPLAY_LOG_SECTIONS.POSBATTLE

  def parse_log_header(self, line: List[str]) -> Tuple[str, PLAYER_POSITION]:
    self.expect_line_segments(line, 2)
    raw_player, pokemon_nickname = line[1].split(': ')
    player = self.parse_player_name(raw_player)
    pokemon_name = self.pokemon_name_mapping[player][pokemon_nickname]
    return pokemon_name, player

  def parse_log_line(self, line: List[str], replay: Replay) -> None:
    action = line[0]
    if action == 'gametype':
      self.expect_line_segments(line, 2)
      replay.game_type = GAME_TYPES(line[1])
      Logger().debug(f'Game set to {replay.game_type} battle')
    elif action == 'gen':
      self.expect_line_segments(line, 2)
      replay.generation = int(line[1])
      Logger().debug(f'Game using GEN {replay.generation} pokemon')
    elif action == 'poke':
      self.expect_line_segments(line, 3)
      pokemon_name = self.parse_pokemon_name(line[2])
      player = self.parse_player_name(line[1])
      pokemon = PokemonService().get_pokemon(pokemon_name)
      replay.teams[player].add(pokemon)
    elif action == 'switch' or action == 'drag':
      self.expect_line_segments(line, 3)
      pokemon_name = self.parse_pokemon_name(line[2])
      raw_player, pokemon_nickname = line[1].split(': ')
      player = self.parse_player_name(raw_player)
      replay.add_pokemon(pokemon_name, player)
      self.pokemon_name_mapping.setdefault(player, {}).setdefault(pokemon_nickname, pokemon_name)
    elif action == '-enditem':
      self.expect_line_segments(line, 3)
      pokemon, player = self.parse_log_header(line)
      replay.set_pokemon_item(pokemon, player, line[2])
    elif action == '-ability':
      self.expect_line_segments(line, 3)
      pokemon, player = self.parse_log_header(line)
      replay.set_pokemon_ability(pokemon, player, line[2])
    elif action == 'move':
      self.expect_line_segments(line, 3)
      pokemon, player = self.parse_log_header(line)
      replay.add_pokemon_move(pokemon, player, line[2])
    
    
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

        replay.set_pokemon_ability(pokemon_name, player, ability)
      if '[from] item' in message:
        item = message.split(': ')[1]
        raw_player, pokemon_nickname = line[1].split(': ')
        player = self.parse_player_name(raw_player)
        pokemon_name = self.pokemon_name_mapping[player][pokemon_nickname]

        replay.set_pokemon_item(pokemon_name, player, item)