import yaml
import math
import discord

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional, List, Union
from random import choice
from collections import Counter

from discord import Embed, Member, Interaction, ButtonStyle
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
        super().__init__(label = label, style = ButtonStyle.primary)
        self.user = user
        self.user_id = user.id
        self.lottery = lottery
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("❌ 系統提示：這不是你的介面喔！",
                                                    ephemeral = True)
            return
        
        loot_result = self.lottery.process_draw(self.user, times = 1)
        
        if isinstance(loot_result, list):
            embed = create_single_draw_embed(loot_result[0])
            view = PublicDrawView(embed = embed, user = self.user)
            await interaction.response.edit_message(
                content = f"🎁 單抽結果：",
                embed = embed,
                view = view
            )
        elif isinstance(loot_result, str):
            await interaction.response.edit_message(
                content = loot_result,
                view = None
            )

class DrawLotteryTenTimesButton(Button):
    def __init__(self, label: str, user: Member, lottery: Lottery):
        super().__init__(label = label, style = ButtonStyle.primary)
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
                content = f"🎁 十連抽結果：第 1 / 2 頁",
                embed = embeds[0],
                view = view
            )
        elif isinstance(loots_result, str):
            await interaction.response.edit_message(
                content = loots_result,
                view = None
            )
            
class PublicDrawView(View):
    def __init__(self, embed: Embed, user: Member, timeout: int = 30):
        super().__init__(timeout = timeout)
        self.embed = embed
        self.user = user
        
        self.add_item(PublicDrawButton(self.embed, self.user))
        

class PublicDrawButton(Button):
    def __init__(self, embed: Embed, user: Member):
        super().__init__(label = "📢 公開顯示", style = ButtonStyle.primary)
        self.embed = embed
        self.user = user
    
    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("❌ 這不是你的抽獎結果喔！", ephemeral=True)
            return
        
        view = PublicDrawView(self.embeds, self.user)
        await interaction.response.send_message(
            content = f"🎁 {interaction.user.display_name} 公開了他的單抽結果",
            embed = self.embed,
            view = view  # ✅ 使用公開版本
        )

class BaseDrawPageView(View):
    def __init__(self, embeds: List[Embed], user: Member, timeout: int = 30):
        super().__init__(timeout = timeout)
        self.embeds = embeds
        self.user = user
        self.current_page = 0
        self.total_pages = len(embeds)

        self.prev_button = DrawPreviousPageButton(label = "⬅ 上一頁", user = user)
        self.next_button = DrawNextPageButton(label = "➡ 下一頁", user = user)

        self.add_item(self.prev_button)
        self.add_item(self.next_button)

        self.update_button_state()

    def update_button_state(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.total_pages - 1

class DrawEmbedPageView(BaseDrawPageView):
    def __init__(self, embeds: List[Embed], user: Member):
        super().__init__(embeds, user, timeout = 30)
        self.public_button = PublicDrawEmbedButton(embeds, user)
        self.add_item(self.public_button)

class PublicDrawEmbedPageView(BaseDrawPageView):
    def __init__(self, embeds: List[Embed], user: Member):
        super().__init__(embeds, user, timeout = 60) 

class DrawPreviousPageButton(Button):
    def __init__(self, label: str, user: Member):
        super().__init__(label = label, style = ButtonStyle.primary)
        self.user = user
    
    async def callback(self, interaction: Interaction):
        view: BaseDrawPageView = self.view
        view.current_page -= 1
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"🎁 **{self.user.display_name}** 的十連抽結果：第 {view.current_page + 1} / {view.total_pages} 頁",
            embed = view.embeds[view.current_page],
            view = view
        )

class DrawNextPageButton(Button):
    def __init__(self, label: str, user: Member):
        super().__init__(label = label, style = ButtonStyle.primary)
        self.user = user
    
    async def callback(self, interaction: Interaction):
        view: BaseDrawPageView = self.view
        view.current_page += 1
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"🎁 **{self.user.display_name}** 的十連抽結果：第 {view.current_page + 1} / {view.total_pages} 頁",
            embed = view.embeds[view.current_page],
            view = view
        )

class PublicDrawEmbedButton(Button):
    def __init__(self, embeds: List[Embed], user: Member):
        super().__init__(label = "📢 公開顯示", style = ButtonStyle.primary)
        self.embeds = embeds
        self.user = user

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("❌ 這不是你的抽獎結果喔！", ephemeral=True)
            return
        
        view = PublicDrawEmbedPageView(self.embeds, self.user)
        msg = await interaction.response.send_message(
            content = f"🎁 {interaction.user.display_name} 公開了他的十連抽結果：第 1 / {len(self.embeds)} 頁",
            embed = self.embeds[0],
            view = view  # ✅ 使用公開版本
        )
        view.message = await interaction.original_response()