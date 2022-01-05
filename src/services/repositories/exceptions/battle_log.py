class BattleLogParseError(Exception):
  pass

class InvalidGameType(BattleLogParseError):
  pass

class InvalidTier(BattleLogParseError):
  pass

class InvalidPlayer(BattleLogParseError):
  pass

class PokemonNotInTeam(BattleLogParseError):
  pass

class InvalidBattleLogLine(BattleLogParseError):
  pass