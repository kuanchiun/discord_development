from typing import Dict, List, Union
from collections import defaultdict
from random import choice, choices
from pathlib import Path
from discord import Member

import yaml

from .player import Player
from .base_item import BaseItem
from .prototype import Prototype
from .scroll import Scroll
from .equipment import Equipment


RULE_PATH = Path("yaml/")
ITEM_PATH = Path("yaml/items")
EQUIPMENT_PATH = Path("yaml/equipments")

class Lottery:
    def __init__(self):
        self.lottery_rule = self.load_lottery_rule()
        self.lottery_pool = self.load_lottery_pool()
        
    def load_lottery_rule(self) -> Dict:
        """取得抽獎規則

        Returns
        -------
        Dict
            抽獎規則字典
        """
        filepath = RULE_PATH / "lottery_rule.yaml"
        with open(filepath, "r", encoding = "utf-8") as file:
            return yaml.safe_load(file)
    
    def load_lottery_pool(self) -> Dict[str, Dict[str, List["BaseItem"]]]:
        """取得抽獎池

        Returns
        -------
        Dict[str, Dict[str, List[BaseItem]]]
            抽獎池
        """
        
        pool = defaultdict(lambda: {"equipment": [], "items": []})
        
        for rarity in self.lottery_rule["RARITY_LIST"]:
            equipments_filepath = EQUIPMENT_PATH / f"{rarity}.yaml"
            items_filepath = ITEM_PATH / f"{rarity}.yaml"
            
            with open(equipments_filepath, "r", encoding = "utf-8") as file:
                data = yaml.safe_load(file)
            for equipment in data["items"]:
                pool[rarity]["equipment"].append(Equipment.from_dict(equipment))
            
            with open(items_filepath, "r", encoding = "utf-8") as file:
                data = yaml.safe_load(file)
            for item in data["items"]:
                if item["item_type"] == "scroll":
                    pool[rarity]["items"].append(Scroll.from_dict(item))
                elif item["item_type"] == "prototype":
                    pool[rarity]["items"].append(Prototype.from_dict(item))
            
        return pool
    
    def draw(self) -> "BaseItem":
        """抽獎一次

        Returns
        -------
        BaseItem
            獎品
        """
        
        rarities = list(self.lottery_rule["RARITY_PROBABILITY"].keys())
        rarity_weights = list(self.lottery_rule["RARITY_PROBABILITY"].values())
        chosen_rarity = choices(rarities, weights=rarity_weights, k=1)[0]

        item_types = list(self.lottery_rule["ITEM_PROBABILITY"].keys())
        item_weights = list(self.lottery_rule["ITEM_PROBABILITY"].values())
        chosen_type = choices(item_types, weights=item_weights, k=1)[0]

        rarity_pool = self.lottery_pool.get(chosen_rarity, {})
        candidates = rarity_pool.get(chosen_type, [])

        if not candidates:
            return None

        loot = choice(candidates)
        return loot

        
    def draw_ten_time(self) -> List["BaseItem"]:
        """抽獎十次

        Returns
        -------
        List[BaseItem]
            十個獎品
        """
        return [self.draw() for _ in range(10)]
    
    
    def process_draw(self, user: Member, times: int = 1) -> Union[List["BaseItem"] | str]:
        """執行抽獎
        
        Parameters
        ----------
        user : Member
            Discord用戶
        times : int
            抽獎次數, by default 1

        Returns
        -------
        List[BaseItem] | str
            獎品列表 | 錯誤訊息

        Raises
        ------
        ValueError
            抽獎次數錯誤
        """
        
        user_id = user.id
        player = Player.load(user_id)
        
        if player.iteminventory.money < self.lottery_rule["COST"] * times:
            return "❌ 你的持有金幣不夠！"
        
        if times == 1:
            loots = [self.draw()]
        elif times == 10:
            loots = self.draw_ten_time()
        else:
            raise ValueError("❌ 抽獎次數必須為1或10")
        
        for item in loots:
            if item is None:
                continue
            if item.get_item_type() == "equipment":
                player.equipinventory.add(item) 
            elif item.get_item_type() in ["prototype", "scroll"]:
                player.iteminventory.add(item)
        
        return loots
                    
        
    def show_lottery_pool(self):
        ...