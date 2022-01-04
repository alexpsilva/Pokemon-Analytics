from src.types.entities.pokemon import Pokemon
from src.types.enums.game_types import GAME_TYPES
from typing import List, Optional
from src.utils.logger import Logger
from src.types.enums.battle_log_sections import BATTLE_LOG_SECTIONS
from src.types.entities.battle_log import BattleLog


def parse_battle_log(log: str) -> BattleLog:
  battle_log = BattleLog()
  
  log_section: BATTLE_LOG_SECTIONS = BATTLE_LOG_SECTIONS.GAME_PREVIEW
  handler_by_section = {
    BATTLE_LOG_SECTIONS.GAME_PREVIEW: parse_game_preview_line,
    BATTLE_LOG_SECTIONS.TEAM_PREVIEW: lambda x, y: None,
    BATTLE_LOG_SECTIONS.BATTLE: parse_battle_line,
    BATTLE_LOG_SECTIONS.POSBATTLE: lambda x, y: None,
  }

  for raw_line in log.split('\n'):
    Logger().debug(f'Parsing: {raw_line}')
    line = list(filter(lambda x: x, raw_line.split('|')))
    if len(line) == 0:
      Logger().debug(f'Skipping empty line')
      continue
    
    log_section = update_battle_section(line) or log_section
    handler_by_section[log_section](line, battle_log)
    
  return battle_log

def update_battle_section(line: List[str]) -> Optional[BATTLE_LOG_SECTIONS]:
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

def parse_game_preview_line(line: List[str], battle_log: BattleLog) -> None:
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
  elif len(line) == 5:
    if line[0] == 'player':
      player_id = line[1]
      player_name = line[2]
      battle_log.players[player_id] = player_name
      Logger().debug(f'Player {player_id} named {player_name}')

def parse_team_preview_line(line: List[str], battle_log: BattleLog) -> None:
  if len(line) == 3 and line[0] == 'poke':
    if line[0] == 'poke':
      pokemon_name = line[2].split(', ')[0] # Pokemon are named as '<Name>, <Gender>'
      battle_log.teams[line[1]].add(Pokemon(pokemon_name))

def parse_battle_line(line: List[str], battle_log: BattleLog) -> None:
  if len(line) == 2:
    if line[0] == 'turn':
      battle_log.current_turn = int(line[1])
      Logger().debug(f'Starting turn {battle_log.current_turn}')
  elif len(line) == 4 or len(line) == 5:
    if line[0] == 'switch':
      raw_player, pokemon_name = line[1].split(': ')
      player = battle_log.parse_player(raw_player)
      battle_log.add_pokemon(pokemon_name, player)
    elif line[0] == '-ability':
      raw_player, pokemon_name = line[1].split(': ')
      player = battle_log.parse_player(raw_player)
      battle_log.set_pokemon_ability(pokemon_name, player, line[2])
    elif line[0] == 'move':
      raw_player, pokemon_name = line[1].split(': ')
      player = battle_log.parse_player(raw_player)
      move = line[2]
      battle_log.add_pokemon_move(pokemon_name, player, move)
  
  for index, message in enumerate(line):
    if '[from] ability' in message:
      ability = message.split(': ')[1]
      raw_player, pokemon_name = line[index + 1].split(': ')
      player = battle_log.parse_player(raw_player.replace('[of] ', ''))
      battle_log.set_pokemon_ability(pokemon_name, player, ability)