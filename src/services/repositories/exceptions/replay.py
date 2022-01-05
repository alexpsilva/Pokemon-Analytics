class ReplayParseError(Exception):
  pass

class InvalidGameType(ReplayParseError):
  pass

class InvalidTier(ReplayParseError):
  pass

class InvalidPlayer(ReplayParseError):
  pass

class PokemonNotInTeam(ReplayParseError):
  pass

class InvalidBattleLogLine(ReplayParseError):
  pass