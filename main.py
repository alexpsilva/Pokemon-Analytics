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

recent_replays = []
for player in top_players:
  Logger().info(f'Fetching replays for {player}')
  recent_replays = api.recent_replays(format=format, username=player)
  if len(recent_replays) != 0:
    break

recent_battles = []
for replay in recent_replays:
  battle = api.replay(replay['id'])

  p1_team = battle['log'].teams['p1']
  p2_team = battle['log'].teams['p2']
  Logger().debug(f'P1 team:\n{p1_team}\n')
  Logger().debug(f'P2 team:\n{p2_team}\n')

  recent_battles.append(battle)

