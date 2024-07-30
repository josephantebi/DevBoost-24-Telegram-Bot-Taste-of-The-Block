import json
from pprint import pprint

from entities.Restaurant import TasteOfTheBlock


def generate_from_json(file):
    with open(file) as f:
        return TasteOfTheBlock(**json.load(f))
