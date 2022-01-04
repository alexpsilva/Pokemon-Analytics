from src.types.enums.logger_level import LOGGER_LEVEL
from src.utils.logger import Logger
from src.types.enums.battle_formats import BATTLE_FORMATS
from src.showdown_api import ShowdownAPI
import json

api = ShowdownAPI()
format = BATTLE_FORMATS.GEN8BDSP_BATTLE_FESTIVAL_DOUBLES
logger = Logger(LOGGER_LEVEL.INFO)

ladder = api.ladder(format)
top_players = [i['userid'] for i in ladder['toplist']]

output_filename = 'output_teams.txt'
recent_teams = {}
placing = 0
while placing < 50:
  placing += 1
  if placing >= len(top_players):
    Logger().error(f'There is no #{placing} on the ladder')
    break
  
  player = top_players[placing]
  Logger().info(f'Fetching replays for #{placing} {player}')
  recent_replays = api.recent_replays(format=format, username=player)
  if len(recent_replays) == 0:
    Logger().warn(f'No replays found for player {player}')
    continue

  for replay in recent_replays:
    battle = api.replay(replay['id'])
    
    player_position = 'p1' if battle['log'].players['p1'] == player else 'p2'
    team = battle['log'].teams[player_position]
    used_pokemon = frozenset(str(pokemon.name) for pokemon in team.pokemon)

    other_team = recent_teams.get(player, {}).get(used_pokemon)
    if other_team is None:
      recent_teams.setdefault(player, {}).setdefault(used_pokemon, team)
    else:
      Logger().info(f'Merging two {used_pokemon} teams')
      other_team.merge(team)

with open(output_filename, 'w') as file:
  Logger().info(f'Outputing teams into {output_filename}')
  for player, teams in recent_teams.items():
    file.write(f'\n---------- {player}\'s teams: -----------\n')
    for i, team in enumerate(teams.values()):
      file.write(f'\n{team}\n')
      if i < len(teams) - 1:
        file.write('-------------------')
