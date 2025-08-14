import asyncio
from collections import Counter

from discord import ButtonStyle, Interaction, Member
from discord.ui import View

from ..basebutton import BaseUserRestrictedButton
from ..player.player import Player
from .draw_demonstrate_choice import DrawDemonstrateView
from .draw_view import DrawView
from .lottery import Lottery
from .lottery_utils import (create_multi_draw_effect_embed,
                            create_multi_draw_embeds,
                            create_single_draw_effect_embed,
                            create_single_draw_embed,
                            create_summarize_rarity_embed)


########################
# DrawLotteryView class
########################
class DrawLotteryView(View):
    def __init__(self, user: Member, player: Player, lottery: Lottery):
        super().__init__(timeout = 30)
        self.message = None
        
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
        self.add_item(DrawLotteryCancelButton(user = user, label = "關閉介面"))
    
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉介面",
                embed = None,
                view = None
            )
        return
        
##############################
# DrawLotteryOnceButton class
##############################
class DrawLotteryOnceButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, player: Player, lottery: Lottery):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.user_id = user.id
        self.player = player
        self.lottery = lottery
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
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
            view.message = message
        elif isinstance(loot_result, str):
            await interaction.response.edit_message(
                content = loot_result,
                view = None
            )
        return

##################################
# DrawLotteryTenTimesButton class
##################################
class DrawLotteryTenTimesButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, player: Player, lottery: Lottery):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.user_id = user.id
        self.player = player
        self.lottery = lottery
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        loots_result = self.lottery.process_draw(user_id = self.user_id, player = self.player, times = 10)
        
        if isinstance(loots_result, list):
            embeds, single_embeds = create_multi_draw_embeds(loots_result)
            counter = Counter(loot.get_rarity() for loot in loots_result)
            embed = create_multi_draw_effect_embed(counter)
            await interaction.response.edit_message(
                content = None,
                embed = embed,
                view = None
            )
            await asyncio.sleep(4)
            embed = create_summarize_rarity_embed(loots_result)
            view = DrawDemonstrateView(user = self.user,
                                       embeds = embeds, 
                                       single_embeds = single_embeds)
            message = await interaction.original_response()
            await message.edit(
                content = f"請選擇展示方式：",
                embed = embed,
                view = view
            )
            view.message = message
        elif isinstance(loots_result, str):
            await interaction.response.edit_message(
                content = loots_result,
                view = None
            )
        return

################################
# DrawLotteryCancelButton class
################################
class DrawLotteryCancelButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        await interaction.response.edit_message(content = "系統提示：已關閉", embed = None, view = None)
        return
