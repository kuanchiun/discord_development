from dataclasses import dataclass, field
from typing import Optional, Dict, List
from random import random, choice, choices

from pathlib import Path

from .player import Player
from .base_item import BaseItem

LOTTERY_PATH = Path("yaml/")
RARITY_LIST = ["N", "R", "SR", "UR"]
RARITY_PROBABILITY = {
    "N": 63,
    "R": 25,
    "SR": 10,
    "UR": 2
}
ITEM_PROBABILITY = {
    "equipments": 66.66667,
    "items": 33.33333
}

@dataclass
class Lottery:
    pool: Dict[Dict[str, BaseItem]]
    
    
    def get_lottery_pool(self):
        pool = {}
        
        for rarity in RARITY_LIST:
            file_path = LOTTERY_PATH / f"{rarity}.yaml"
            with open():
                ...