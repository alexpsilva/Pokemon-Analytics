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

    for player in ['p1']:
      player_name = battle['log'].players[player]
      team = battle['log'].teams[player]
      used_pokemon = tuple(str(pokemon.name) for pokemon in team.pokemon)

      other_team = recent_teams.get(player_name, {}).get(used_pokemon)
      if other_team is None:
        recent_teams.setdefault(player_name, {}).setdefault(used_pokemon, team)
      else:
        Logger().info(f'Merging two {used_pokemon} teams')
        other_team.merge(team)

for player, teams in recent_teams.items():
  Logger().info(f'---------- {player}\'s teams: -----------')
  for i, team in enumerate(teams.values()):
    Logger().info(f'\n{team}\n')
    if i < len(teams) - 1:
      Logger().info('-------------------')
