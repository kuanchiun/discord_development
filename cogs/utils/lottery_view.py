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

from .lottery import Lottery
from .scroll import Scroll
from .prototype import Prototype
from .equipment import Equipment
from .player import Player
from .base_item import BaseItem

FIGURE_PATH = "https://raw.githubusercontent.com/kuanchiun/discord_development/main/figures/{rarity}/{figure_id}.png"
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
RARITY_EMOJI = {
    "N": "⚪️",
    "R": "🔵",
    "SR": "🟣",
    "UR": "🟡"
}

def create_single_draw_embed(loot: BaseItem) -> Embed:
    rarity = loot.get_rarity()
    figure_id = loot.get_figure_id()
    
    embed = Embed(
        title = f"{RARITY_EMOJI[rarity]} {loot.get_display_name()}",
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
                f"裝備部位：{PART_MAPPING[loot.part]}\n" + 
                f"VIT： +{loot.attribute_bonus["VIT"]:>3}  WIS： +{loot.attribute_bonus["WIS"]:>3}\n" +
                f"STR： +{loot.attribute_bonus["STR"]:>3}  INT： +{loot.attribute_bonus["INT"]:>3}\n" +
                f"DEX： +{loot.attribute_bonus["DEX"]:>3}  AGI： +{loot.attribute_bonus["AGI"]:>3}\n" +
                f"MND： +{loot.attribute_bonus["MND"]:>3}  LUK： +{loot.attribute_bonus["LUK"]:>3}\n" +
                "```"
            ),
            inline = False
        )
        
    embed.set_thumbnail(url = FIGURE_PATH.format(rarity = rarity, figure_id = figure_id))
    
    return embed

def create_multi_draw_embeds(loots: List[BaseItem]) -> List[Embed]:
    embeds = []
    rarity_count = summarize_rarity(loots)
    
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
                name = f"{RARITY_EMOJI[rarity]}  {page + i}. {display_name}",
                value = (
                    f"> **稀有度：** {rarity}\n" + 
                    f"> **類型：** {ITEM_TYPE_MAPPING[item_type]}\n" + 
                    f"> **說明：** {description}"
                ),
                inline = False
            )
        
        embed.set_footer(text = rarity_count)
        
        embeds.append(embed)
    
    return embeds 

def summarize_rarity(items):
    counter = Counter(item.rarity for item in items)
    texts = "📊 稀有度統計： "
    for rarity in ["UR", "SR", "R", "N"]:
        texts += f"{RARITY_EMOJI[rarity]} {rarity}: {counter[rarity]} "
    
    return texts

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

        # 初始化按鈕
        self.prev_button = Button(label = "⬅ 上一頁", style = discord.ButtonStyle.secondary)
        self.next_button = Button(label = "➡ 下一頁", style = discord.ButtonStyle.secondary)

        self.prev_button.callback = self.go_previous
        self.next_button.callback = self.go_next
        self.public_button = PublicDrawButton(self.embeds, self.user)

        self.add_item(self.prev_button)
        self.add_item(self.next_button)
        self.add_item(self.public_button)

        self.update_button_state()
    
    def update_button_state(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.total_pages - 1
    
    async def go_previous(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("❌ 這不是你的選單。", ephemeral=True)
            return

        self.current_page -= 1
        self.update_button_state()
        await interaction.response.edit_message(
            content = f"十連抽結果：第 {self.current_page + 1} / {self.total_pages} 頁",
            embed = self.embeds[self.current_page],
            view = self
        )
    
    async def go_next(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("❌ 這不是你的選單。", ephemeral=True)
            return

        self.current_page += 1
        self.update_button_state()
        await interaction.response.edit_message(
            content = f"十連抽結果：第 {self.current_page + 1} / {self.total_pages} 頁",
            embed = self.embeds[self.current_page],
            view = self
        )

class PublicDrawEmbedPageView(View):
    def __init__(self, embeds: List[Embed], user: Member):
        super().__init__(timeout=30)
        self.embeds = embeds
        self.user = user
        self.current_page = 0
        self.total_pages = len(embeds)
        self.user_display_name = user.display_name
        self.message: Optional[discord.Message] = None  # 👈 用來記錄發出的訊息

        self.prev_button = Button(label = "⬅ 上一頁", style = discord.ButtonStyle.secondary)
        self.next_button = Button(label = "➡ 下一頁", style = discord.ButtonStyle.secondary)

        self.prev_button.callback = self.go_previous
        self.next_button.callback = self.go_next

        self.add_item(self.prev_button)
        self.add_item(self.next_button)

        self.update_button_state()
    
    async def on_timeout(self):
        # 禁用所有按鈕
        for child in self.children:
            if isinstance(child, Button):
                child.disabled = True

        # 嘗試更新原始訊息
        if self.message:
            try:
                await self.message.edit(view = self)
            except discord.NotFound:
                pass  # 訊息已刪除，安全忽略
    
    def update_button_state(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.total_pages - 1
    
    async def go_previous(self, interaction: discord.Interaction):
        self.current_page -= 1
        self.update_button_state()
        await interaction.response.edit_message(
            content = f"{self.user_display_name}的十連抽結果：第 {self.current_page + 1} / {self.total_pages} 頁",
            embed = self.embeds[self.current_page],
            view = self
        )
    
    async def go_next(self, interaction: discord.Interaction):
        self.current_page += 1
        self.update_button_state()
        await interaction.response.edit_message(
            content = f"{self.user_display_name}的十連抽結果：第 {self.current_page + 1} / {self.total_pages} 頁",
            embed = self.embeds[self.current_page],
            view = self
        )

class PublicDrawButton(Button):
    def __init__(self, embeds: List[Embed], user: Member):
        super().__init__(label="📢 公開顯示", style=discord.ButtonStyle.primary)
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
        