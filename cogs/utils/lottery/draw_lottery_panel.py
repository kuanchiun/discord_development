from discord import Member, Interaction, ButtonStyle
from discord.ui import Button, View
from collections import Counter

import asyncio

from ..player.player import Player
from .lottery import Lottery
from .draw_view import DrawView
from .draw_page_view import DrawEmbedPageView
from .lottery_utils import (
    create_multi_draw_embeds,
    create_single_draw_embed,
    create_multi_draw_effect_embed,
    create_single_draw_effect_embed
)
from .draw_demonstrate_choice import DrawDemonstrateView

########################
# DrawLotteryView class
########################
class DrawLotteryView(View):
    def __init__(self, user: Member, player: Player, lottery: Lottery):
        super().__init__(timeout = 30)
        
        self.add_item(DrawLotteryOnceButton(
            label = "單抽！ 💎100",
            user = user,
            player = player,
            lottery = lottery
        ))
        self.add_item(DrawLotteryTenTimesButton(
            label = "十連抽！ 💎1000",
            user = user,
            player = player,
            lottery = lottery
        ))
        self.add_item(DrawLotteryCancelButton(user = user))
        
##############################
# DrawLotteryOnceButton class
##############################
class DrawLotteryOnceButton(Button):
    def __init__(self, label: str, user: Member, player: Player, lottery: Lottery):
        super().__init__(label = label, style = ButtonStyle.primary)
        self.user = user
        self.user_id = user.id
        self.player = player
        self.lottery = lottery
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的介面喔！",
                                                    ephemeral = True)
            return
        
        loot_result = self.lottery.process_draw(user_id = self.user_id, player = self.player, times = 1)
        
        if isinstance(loot_result, list):
            embed = create_single_draw_effect_embed(loot_result[0].get_rarity())
            await interaction.response.edit_message(
                content = None,
                embed = embed,
                view = None
            )
            await asyncio.sleep(4)
            embed = create_single_draw_embed(loot_result[0])
            view = DrawView(embed = embed, user = self.user)
            message = await interaction.original_response()
            await message.edit(
                content = f"🎁 單抽結果：",
                embed = embed,
                view = view
            )
        elif isinstance(loot_result, str):
            await interaction.response.edit_message(
                content = loot_result,
                view = None
            )

##################################
# DrawLotteryTenTimesButton class
##################################
class DrawLotteryTenTimesButton(Button):
    def __init__(self, label: str, user: Member, player: Player, lottery: Lottery):
        super().__init__(label = label, style = ButtonStyle.primary)
        self.user = user
        self.user_id = user.id
        self.player = player
        self.lottery = lottery
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的介面喔！",
                                                    ephemeral = True)
            return
        
        loots_result = self.lottery.process_draw(user_id = self.user_id, player = self.player, times = 10)
        
        if isinstance(loots_result, list):
            rarity_count, embeds, single_embeds = create_multi_draw_embeds(loots_result)
            counter = Counter(loot.get_rarity() for loot in loots_result)
            embed = create_multi_draw_effect_embed(counter)
            await interaction.response.edit_message(
                content = None,
                embed = embed,
                view = None
            )
            await asyncio.sleep(4)
            view = DrawDemonstrateView(user = self.user,
                                       embeds = embeds, 
                                       single_embeds = single_embeds)
            message = await interaction.original_response()
            await message.edit(
                content = f"抽卡結果：\n{rarity_count}\n請選擇展示方式：",
                embed = None,
                view = view
            )
        elif isinstance(loots_result, str):
            await interaction.response.edit_message(
                content = loots_result,
                view = None
            )

################################
# DrawLotteryCancelButton class
################################
class DrawLotteryCancelButton(Button):
    def __init__(self, user: Member):
        super().__init__(label = "關閉", style = ButtonStyle.secondary)
        self.user = user
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的介面喔！",
                                                    ephemeral = True)
            return
        
        await interaction.response.edit_message(content = "系統提示：已關閉", view = None)
