from src.utils.singleton import Singleton
from src.enums.logger_level import LOGGER_LEVEL

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Logger(metaclass=Singleton):

  def __init__(self, _level: LOGGER_LEVEL = LOGGER_LEVEL.ERROR):
    self.level = _level
  
  def log(self, msg: str):
    if self.level.value >= LOGGER_LEVEL.LOG.value:
      print(f'[log] {msg}')
  
  def error(self, msg: str):
    if self.level.value >= LOGGER_LEVEL.ERROR.value:
      print(bcolors.FAIL + f'[error] {msg}' + bcolors.ENDC)
  
  def warn(self, msg: str):
    if self.level.value >= LOGGER_LEVEL.WARNING.value:
      print(bcolors.WARNING + f'[warning] {msg}' + bcolors.ENDC)
  
  def info(self, msg: str):
    if self.level.value >= LOGGER_LEVEL.INFO.value:
      print(bcolors.OKCYAN + f'[info] {msg}' + bcolors.ENDC)
  
  def debug(self, msg: str):
    if self.level.value >= LOGGER_LEVEL.DEBUG.value:
      print(bcolors.OKGREEN + f'[debug] {msg}' + bcolors.ENDC)