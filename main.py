from src.services.business.team_reconstruction import reconstruct_teams
from src.enums.logger_level import LOGGER_LEVEL
from src.utils.logger import Logger
from src.enums.battle_formats import BATTLE_FORMATS

logger = Logger(LOGGER_LEVEL.INFO)

reconstruct_teams(
  'output_teams.txt', 
  BATTLE_FORMATS.GEN8BDSP_BATTLE_FESTIVAL_DOUBLES
)
