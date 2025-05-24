import yaml
import math
import discord

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional, List, Union
from random import choice

from discord import Embed, Member, Interaction
from discord.ui import Button, View

from .lottery import Lottery
from .scroll import Scroll
from .prototype import Prototype
from .equipment import Equipment
from .player import Player
from .base_item import BaseItem

FIGURE_PATH = "https://raw.githubusercontent.com/kuanchiun/discord_development/main/figures/{rarity}/{item_id}.png"
PART_MAPPING = {
    "head": "頭部",
    "chest": "身體",
    "legs": "腿部",
    "feet": "腳部",
    "earring": "耳飾",
    "necklace": "項鍊",
    "bracelet": "手鐲",
    "ring": "戒指"
}
ITEM_TYPE_MAPPING = {
    "equipment": "裝備",
    "scroll": "卷軸",
    "prototype": "原型武器"
}


def create_single_draw_embed(loot: BaseItem) -> Embed:
    rarity = loot.get_rarity()
    item_id = loot.get_item_id()
    
    embed = Embed(
        title = f"單抽結果：{loot.get_display_name()}",
        description = loot.get_description(),
        color = discord.Color.gold()
    )
    
    embed.add_field(name = "【稀有度】", value = loot.get_rarity(), inline = True)
    embed.add_field(name = "【物品類型】", value = ITEM_TYPE_MAPPING[loot.get_item_type()], inline = True)
    
    if isinstance(loot, Equipment):
        embed.add_field(
            name = "【裝備屬性】",
            value = (
                "```" +
                f"裝備部位：{PART_MAPPING[loot.part]}" + 
                f"VIT： +{loot.attribute_bonus["VIT"]:>3}  WIS： +{loot.attribute_bonus["WIS"]:>3}" +
                f"STR： +{loot.attribute_bonus["STR"]:>3}  INT： +{loot.attribute_bonus["INT"]:>3}" +
                f"DEX： +{loot.attribute_bonus["DEX"]:>3}  AGI： +{loot.attribute_bonus["AGI"]:>3}" +
                f"MND： +{loot.attribute_bonus["MND"]:>3}  LUK： +{loot.attribute_bonus["LUK"]:>3}" +
                "```"
            ),
            inline = False
        )
    
    embed.set_thumbnail(url = FIGURE_PATH.format(rarity = rarity, display_name = item_id))
    
    return embed

def create_multi_draw_embeds(loots: List[BaseItem]) -> List[Embed]:
    embeds = []
    
    for page in range(0, len(loots), 5):
        embed = Embed(
            title = "十連抽結果",
            description = f"顯示第 {page // 5 + 1}頁 / 共 {len(loots) // 5} 頁",
            color = discord.Color.gold()
        )
        
        for i, loot in enumerate(loots[page:page + 5], start = 1):
            display_name = loot.get_display_name()
            rarity = loot.get_rarity()
            item_type = loot.get_item_type()
            description = loot.get_description()
            
            embed.add_field(
                name = f"{page + i}. {display_name}",
                value = f"【稀有度】\n{rarity}\n【物品類型】{ITEM_TYPE_MAPPING[item_type]}\n【物品說明】\n{description}",
                inline = False
            )
        
        embeds.append(embed)
    
    return embeds   

class DrawLotteryView(View):
    def __init__(self, user: Member, lottery: Lottery):
        super().__init__(timeout = 30)
        self.user = user
        self.user_id = user.id
        self.lottery = lottery
        
        self.add_item(DrawLotteryOnceButton(
            label = "單抽！",
            user = self.user,
            lottery = self.lottery
        ))
        
class DrawLotteryOnceButton(Button):
    def __init__(self, label: str, user: Member, lottery: Lottery):
        super().__init__(label = label, style = discord.ButtonStyle.primary)
        self.user = user
        self.user_id = user.id
        self.lottery = lottery
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("❌ 系統提示：這不是你的介面喔！",
                                                    ephemeral = True)
            return
        
        loot = self.lottery.process_draw(self.user, times = 1)
        
        if isinstance(loot, list):
            await interaction.response.edit_message(
                embed = create_single_draw_embed(loot[0])
            )
        elif isinstance(loot, str):
            await interaction.response.edit_message(
                content = loot
            )

class DrawLotteryTenTimesButton(Button):
    ...
        
        
        