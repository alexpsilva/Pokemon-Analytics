from src.types.battle_formats import BATTLE_FORMATS
from src.showdown_api import ShowdownAPI

api = ShowdownAPI()
print(api.latest_stat())
