from src.utils.logger import Logger

from src.enums.battle_formats import BATTLE_FORMATS
from src.enums.player_position import PLAYER_POSITION

from src.services.repositories.replay import ReplayService
from src.services.data.showdown import ShowdownAPI


def reconstruct_teams(output_filename: str, format: BATTLE_FORMATS, min_placing: int = 50):
  api = ShowdownAPI()
  ladder = api.ladder(format)
  top_players = [i['userid'] for i in ladder['toplist']]

  recent_teams = {}
  placing = 0
  while placing < min_placing:
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

    for replay_summary in recent_replays:
      raw_replay = api.replay(replay_summary['id'])
      player_position = PLAYER_POSITION.P1 if raw_replay['p1id'] == player else PLAYER_POSITION.P2
      
      replay = ReplayService().parse(raw_replay['log'])
      team = replay.teams[player_position]
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