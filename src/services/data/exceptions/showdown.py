class ShowdownAPIError(Exception):
  pass

class InvalidBattleFormat(ShowdownAPIError):
  pass

class InvalidUsername(ShowdownAPIError):
  pass
  
class InvalidReplayID(ShowdownAPIError):
  pass

class InvalidStatDate(ShowdownAPIError):
  pass