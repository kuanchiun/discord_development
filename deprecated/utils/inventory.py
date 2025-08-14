import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from random import choice
from typing import Dict, List, Optional, Union

import discord
from discord import Embed, Interaction, Member
from discord.ui import Button, View

import yaml


def load_init_inventory_item():
    with open("init_inventory_item.yaml", "r", encoding = "utf-8") as f:
        data = yaml.safe_load(f)
        return data["item"]

@dataclass
class Inventory:
    money: int = 0
    equipments: Dict = field(
        default_factory = lambda: {
            "pre-weapon": [],
            "weapon": [],
            "head": [],
            "chest": [],
            "legs": [],
            "feet": [],
            "earring": [],
            "necklace": [],
            "bracelet": [],
            "ring": [],
        }
    )
    items: Dict = field(
        default_factory = lambda: load_init_inventory_item()
    )