class APIError(Exception):
  pass

class InvalidBattleFormat(APIError):
  pass

class InvalidUsername(APIError):
  pass
  
class InvalidReplayID(APIError):
  pass

class InvalidStatDate(APIError):
  pass