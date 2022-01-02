from src.types.enums.battle_formats import BATTLE_FORMATS
from src.showdown_api import ShowdownAPI
import json

api = ShowdownAPI()
print(api.replay('gen8ou-1401834445'))
