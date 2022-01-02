from src.types.responses.replay import Replay, ReplayResponse
from src.types.responses.ladder import LadderResponse
from src.types.battle_log import BattleLog
from src.parser import parse_list
from typing import Dict, List, Optional, Union
from datetime import datetime
import requests

from requests.api import request

from src.types.enums.battle_formats import BATTLE_FORMATS
from .exceptions.api import *

class ShowdownAPI:
  HOSTS = {
    'MAIN': 'pokemonshowdown.com',
    'REPLAYS': 'replay.pokemonshowdown.com',
    'POKEDEX': 'play.pokemonshowdown.com',
    'SMOGON': 'www.smogon.com',
  }

  PROTOCOL = 'https'

  def __init__(self):
    pass

  def _build_url(self, host: str, path: str) -> str:
    return f'{self.PROTOCOL}://{host}/{path}'

  @staticmethod
  def _validate_battle_format(format: BATTLE_FORMATS) -> str:
    if format not in BATTLE_FORMATS:
      raise InvalidBattleFormat
    return format.value

  @staticmethod
  def _validate_username(username: str) -> str:
    if type(username) is not str:
      raise InvalidUsername
    return username

  @staticmethod
  def _validate_stat_date(date: Optional[str]) -> Union[str, None]:
    if type(date) is not str:
      raise InvalidStatDate
    return date

  def ladder(self, _format: BATTLE_FORMATS) -> LadderResponse:
    if _format is None:
      raise InvalidBattleFormat
    
    format = self._validate_battle_format(_format)
    url = self._build_url(self.HOSTS['MAIN'], f'ladder/{format}.json')
    return requests.get(url).json()
  
  def replay(self, replay_id: str) -> Replay:
    if type(replay_id) is not str:
      raise InvalidReplayID
    
    url = self._build_url(self.HOSTS['REPLAYS'], f'{replay_id}.json')
    response = requests.get(url).json()
    response['log'] = BattleLog(response['log'])
    return response

  def recent_replays(self, username: Optional[str]=None, format: Optional[BATTLE_FORMATS]=None) -> ReplayResponse:
    params: Dict[str, str] = {}
    if format is not None:
      params['format'] = self._validate_battle_format(format)
    
    if username is not None:
      params['user'] = self._validate_username(username)
    
    url = self._build_url(self.HOSTS['REPLAYS'], 'search.json')
    return requests.get(url, params).json()

  def latest_stat(self) -> Union[str, None]:
    base_url = self._build_url(self.HOSTS['SMOGON'], 'stats')
    html_stats = requests.get(base_url).text

    date_format = '%Y-%m'
    date_regexp = r'[0-9]{4}-[0-9]{2}\/'
    dates = [datetime.strptime(bucket[:-1], date_format) for bucket in parse_list(html_stats, date_regexp)]

    if not dates:
      return None
    return sorted(dates, reverse=True)[0].strftime(date_format)
  
  def moveset(self, _format: BATTLE_FORMATS, rating=None, date: Optional[str]=None):
    if _format is not None:
      format = self._validate_battle_format(_format)

    if date is None:
      date = self.latest_stat()
    else:
      date = self._validate_stat_date(date)

    # (to-do)

  def format(self, _format: BATTLE_FORMATS):
    format = self._validate_battle_format(_format)
    pass

  # def user(self, username) -> JSON:
  #   url = self._build_url(self.POKEMON_SHOWDOWN_HOSTS['MAIN'], f'{username}.json')