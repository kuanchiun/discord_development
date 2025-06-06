from typing import Optional, Dict, List
from random import random
from pathlib import Path
from discord import Member

import yaml

from ..item.base_item import BaseItem
from ..item.scroll.scroll import Scroll, PreventScroll
from ..player.player import Player

ITEM_PATH = Path("yaml/items")

#############
# Shop class
#############
class Shop:
    def __init__(self):
        self.commodities = self.load_shop_commodity()
    
    def load_shop_commodity(self) -> Dict[str, "BaseItem"]:
        """取得商店販售物品資訊

        Returns
        -------
        Dict[str, BaseItem]
            商店物品販售資訊
        """
        filepath = ITEM_PATH / "shop.yaml"
        with open(filepath, "r", encoding = "utf-8") as file:
            data = yaml.safe_load(file)
            
        commodities = {}
        for commodity in data["items"]:
            if commodity["item_type"] == "scroll":
                commodities[commodities["item_id"]] = Scroll.from_dict(commodity)
            elif commodity["item_type"] == "prevent_scroll":
                commodities[commodities["item_id"]] = PreventScroll.from_dict(commodity)
        
        return commodities
    
    def list_all_commodity(self) -> List[BaseItem]:
        """列出商店所有販售物品

        Returns
        -------
        List[BaseItem]
            販售物品清單
        """
        return list(self.commodities.values)
    
    
    def purchase(self, user: Member, item_id: str, amount: int) -> str:
        """購買物品

        Parameters
        ----------
        user : Member
            用戶
        item_id : str
            物品ID
        amount : int
            數量

        Returns
        -------
        str
            購買提示
        """
        user_id = user.id
        purchase_item = self.commodities[item_id]
        purchase_money = purchase_item.get_purchase_money() * amount
        player = Player.load(user_id)

        if player.iteminventory.money < purchase_money:
            return "⚠️ 系統提示：持有💎水晶不足！"
        
        player.iteminventory.add(purchase_item, amount)
        player.iteminventory.money -= purchase_money
        
        return f"⚠️ 系統提示：你使用 💎**{purchase_money}** 購買了 **{amount}** 張 **{purchase_item.get_display_name}**！"
    