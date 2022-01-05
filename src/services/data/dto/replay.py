from src.entities.battle_log import BattleLog
from typing import List, Optional, TypedDict

class ReplaySummary(TypedDict):
  uploadtime: int
  id: str
  format: str
  p1: str
  p2: str

ReplaySumaryResponse = List[ReplaySummary]

class ReplayResponse(ReplaySummary):
  log: str
  views: int
  p1id: str
  p2id: str
  formatid: str
  rating: int
  private: int
  password: Optional[str]