from typing import TypedDict, List

class LadderEntry(TypedDict):
  userid: str
  username: str
  w: int
  l: int
  t: int
  gxe: int
  r: float
  rd: float
  sigma: float
  rptime: str
  rpr: float
  rprf: float
  rpsigma: float
  elo: float

class LadderResponse(TypedDict):
  formatid: str
  format: str
  toplist: List[LadderEntry]

