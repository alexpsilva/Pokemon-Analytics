class BattleLogParseError(Exception):
  pass

class InvalidGameType(BattleLogParseError):
  pass

class InvalidTier(BattleLogParseError):
  pass

class InvalidPlayer(BattleLogParseError):
  pass

class InvalidPokemon(BattleLogParseError):
  pass

class InvalidBattleLogLine(BattleLogParseError):
  pass