import yaml
import math
import discord

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional, List, Union
from random import choice
from collections import Counter

from discord import Embed, Member, Interaction
from discord.ui import Button, View

from .lottery_utils import (
    create_multi_draw_embeds,
    create_single_draw_embed,
)

from .lottery import Lottery
from ..player.player import Player

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
        self.add_item(DrawLotteryTenTimesButton(
            label = "十連抽！",
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
        
        loot_result = self.lottery.process_draw(self.user, times = 1)
        embed = create_single_draw_embed(loot_result[0])
        
        if isinstance(loot_result, list):
            await interaction.response.edit_message(
                content = f"單抽結果：",
                embed = embed,
                view = None
            )
        elif isinstance(loot_result, str):
            await interaction.response.edit_message(
                content = loot_result,
                view = None
            )

class DrawLotteryTenTimesButton(Button):
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
        
        loots_result = self.lottery.process_draw(self.user, times = 10)
        
        if isinstance(loots_result, list):
            embeds = create_multi_draw_embeds(loots_result)
            view = DrawEmbedPageView(embeds = embeds, user = self.user)
            await interaction.response.edit_message(
                content = f"十連抽結果：第 1 / 2 頁",
                embed = embeds[0],
                view = view
            )
        elif isinstance(loots_result, str):
            await interaction.response.edit_message(
                content = loots_result,
                view = None
            )




class DrawEmbedPageView(View):
    def __init__(self, embeds: List[Embed], user: Member):
        super().__init__(timeout = 30)
        self.embeds = embeds
        self.user = user
        self.current_page = 0
        self.total_pages = len(embeds)
        

class PublicDrawEmbedPageView(View):
    def __init__(self, embeds: List[Embed], user: Member):
        super().__init__(timeout = 60)
        self.embeds = embeds
        self.user = user
        self.current_page = 0
        self.total_pages = len(embeds)
    


class DrawPreviousPageButton(Button):
    def __init__(self, label: str, user: Member, lottery: Lottery):
        super().__init__(label = label, style = discord.ButtonStyle.primary)
        self.user = user
        self.user_id = user.id
        self.lottery = lottery
    
    async def callback(self, interaction: Interaction):
        ...
    


class DrawNextPageButton(Button):
    ...
