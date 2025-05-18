import discord
from discord.ext import commands
from discord import app_commands, Embed, Member, Interaction
from discord.ui import View, Button, button
from random import choice, choices
import yaml
from typing import Dict

LOTTERY_POOL_PATH_LIST = [
    "yaml/equipments/N.yaml",
    "yaml/equipments/R.yaml",
    "yaml/equipments/SR.yaml",
    "yaml/equipments/UR.yaml",
    "yaml/items/N.yaml",
    "yaml/items/R.yaml",
    "yaml/items/SR.yaml",
    "yaml/items/UR.yaml"
]

RARITY_WEIGHTS = {
    "UR": 1, 
    "SR": 10,
    "R": 29,
    "N": 60
}

PART_MAPPING = {
    "pre-weapon": "原型武器",
    "head": "頭部",
    "chest": "身體",
    "legs": "腿部",
    "feet": "腳部",
    "earring": "耳飾",
    "necklace": "項鍊",
    "bracelet": "手鐲",
    "ring": "戒指"
}

def load_lottery_pool() -> Dict:
    rarities = list(RARITY_WEIGHTS.keys())
    lottery_pool = {rarity:[] for rarity in rarities}
    
    for rarity in rarities:
        with open(f"yaml/equipments/{rarity}.yaml", "r", encoding = "utf-8") as f:
            equipments = yaml.safe_load(f)[rarity]
        #with open(f"yaml/items/{rarity}.yaml", "r", encoding = "utf-8") as f:
        #    items = yaml.safe_load(f)[rarity]
        
        lottery_pool[rarity] += equipments
        #lottery_pool[rarity] += items
    
    return lottery_pool

def draw_item(lottery_pool: Dict) -> Dict:
    rarities = list(RARITY_WEIGHTS.keys())
    weights = list(RARITY_WEIGHTS.values())
    
    chosen_rarity = choices(rarities, weights = weights, k = 1)[0]
    
    candidates = lottery_pool.get(chosen_rarity, [])
    if not candidates:
        return None
    
    loot = choice(candidates)
    
    return loot
    
def get_lottery_embed(loot: Dict, user: Member) -> Embed:
    ...

