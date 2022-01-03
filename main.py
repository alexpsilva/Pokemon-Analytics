from src.types.enums.battle_formats import BATTLE_FORMATS
from src.showdown_api import ShowdownAPI
import json

api = ShowdownAPI()
format = BATTLE_FORMATS.GEN8BDSP_BATTLE_FESTIVAL_DOUBLES

ladder = api.ladder(format)
top_players = [i['userid'] for i in ladder['toplist']]

recent_replays = []
for player in top_players:
  print(f'Fetching replays for {player}')
  recent_replays = api.recent_replays(format=format, username=player)
  if len(recent_replays) != 0:
    break

recent_battles = []
for replay in recent_replays:
  battle = api.replay(replay['id'])
  print('--------P1-------')
  print(battle['log'].teams['p1'])
  print('\n--------P2-------')
  print(battle['log'].teams['p2'])

  recent_battles.append(battle)

