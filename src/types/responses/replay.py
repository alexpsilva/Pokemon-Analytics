from src.types.battle_log import BattleLog
from typing import List, Optional, TypedDict

class ReplaySummary(TypedDict):
  uploadtime: int
  id: str
  format: str
  p1: str
  p2: str

ReplayResponse = List[ReplaySummary]

class Replay(ReplaySummary):
  log: BattleLog
  views: int
  p1id: str
  p2id: str
  formatid: str
  rating: int
  private: int
  password: Optional[str]