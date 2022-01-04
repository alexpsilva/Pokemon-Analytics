from src.types.enums.logger_level import LOGGER_LEVEL
from src.utils.logger import Logger
from src.types.enums.battle_formats import BATTLE_FORMATS
from src.showdown_api import ShowdownAPI
import json

api = ShowdownAPI()
format = BATTLE_FORMATS.GEN8BDSP_BATTLE_FESTIVAL_DOUBLES
logger = Logger(LOGGER_LEVEL.DEBUG)

ladder = api.ladder(format)
top_players = [i['userid'] for i in ladder['toplist']]
players_with_replays = []

recent_replays = []
for player in top_players:
  Logger().info(f'Fetching replays for {player}')
  recent_replays = api.recent_replays(format=format, username=player)
  if len(recent_replays) > 3:
    players_with_replays.append(player)
    break

recent_teams = {}
for replay in recent_replays:
  battle = api.replay(replay['id'])

  for player in ['p1', 'p2']:
    player_name = battle['log'].players[player]
    team = battle['log'].teams[player]
    used_pokemon = tuple(str(pokemon.name) for pokemon in team.pokemon)

    if recent_teams.get(player_name, {}).get(used_pokemon) is None:
      recent_teams.setdefault(player_name, {}).setdefault(used_pokemon, team)
    else:
      Logger().info(f'Merging two {used_pokemon} (type) teams')
      pass # (to-do) merge info from both iterations of this team


for player in players_with_replays:
  teams = recent_teams.get(player, {})
  Logger().info(f'---------- {player}\'s teams: -----------')
  for i, team in enumerate(teams.values()):
    Logger().info(f'\n{team}\n')
    if i < len(teams) - 1:
      Logger().info('-------------------')
