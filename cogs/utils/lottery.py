from dataclasses import dataclass, field
from typing import Optional, Dict, List
from collections import defaultdict
from random import random, choice, choices
from pathlib import Path

import yaml

from .player import Player
from .base_item import BaseItem
from .prototype import Prototype
from .scroll import Scroll


LOTTERY_PATH = Path("yaml/")
RARITY_LIST = ["N", "R", "SR", "UR"]
RARITY_PROBABILITY = {
    "N": 63,
    "R": 25,
    "SR": 10,
    "UR": 2
}
ITEM_PROBABILITY = {
    "equipments": 33.33333,
    "items": 66.66667
}

def get_lottery_pool() -> Dict[str, List[BaseItem]]:
        pool: Dict[str, List[BaseItem]] = field(default_factory = get_lottery_pool)
        
        for rarity in RARITY_LIST:
            file_path = LOTTERY_PATH / f"{rarity}.yaml"
            with open(file_path, "r", encoding = "utf-8") as file:
                data = yaml.safe_load(file)
            
            for item in data["items"]:
                if item["item_type"] == "scroll":
                    pool[rarity].append(Scroll.from_dict(item))
                elif item["item_type"] == "prototype":
                    pool[rarity].append(Prototype.from_dict(item))
        
        return pool

@dataclass
class Lottery:
    pool: Dict[List[BaseItem]] = get_lottery_pool()
    
    