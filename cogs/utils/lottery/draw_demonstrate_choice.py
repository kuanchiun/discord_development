from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import Button, View
from typing import List

from .draw_page_view import DrawEmbedPageView
from .draw_single_view import DrawSingleView
from ..basebutton import BaseUserRestrictedButton

############################
# DrawDemonstrateView class
############################
class DrawDemonstrateView(View):
    def __init__(self, 
                 user: Member,
                 embeds: List[Embed], 
                 single_embeds: List[Embed],
                 timeout = 60):
        super().__init__(timeout = timeout)
        self.message = None  # 待會儲存訊息物件（用來編輯）
        
        self.add_item(DrawOnceDemonsrateButton(user = user, 
                                               label = "一次展示", 
                                               embeds = embeds))
        self.add_item(DrawSingleDemonstrateButton(user = user, 
                                                  label = "單張個別展示", 
                                                  embeds = embeds,
                                                  single_embeds = single_embeds))
        self.add_item(CancelDrawDemonstrateButton(user = user,
                                                  label = "關閉介面"))
    
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉抽卡結果。",
                view = None
            )
    
    
#################################
# DrawOnceDemonsrateButton class
#################################
class DrawOnceDemonsrateButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, embeds: List[Embed]):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.embeds = embeds
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        view = DrawEmbedPageView(self.embeds, self.user)
        await interaction.response.edit_message(
            content = f"⚠️ 系統提示：**{self.user.display_name}** 的十連抽結果：第 1 / 2 頁",
            embed = view.embeds[0],
            view = view
        )
        message = await interaction.original_response()
        view.message = message
        

####################################
# DrawSingleDemonstrateButton class
####################################
class DrawSingleDemonstrateButton(BaseUserRestrictedButton):
    def __init__(self, 
                 user: Member, 
                 label: str, 
                 embeds: List[Embed],
                 single_embeds: List[Embed]):
        
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.embeds = embeds
        self.single_embeds = single_embeds
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        view = DrawSingleView(user = self.user,
                              embeds = self.single_embeds,
                              single_embeds = self.single_embeds)
        await interaction.response.edit_message(
                content = f"**{self.user.display_name}** 的十連抽結果：第 1 / 10",
                embed = view.single_embeds[0],
                view = view
        )
        message = await interaction.original_response()
        view.message = message

####################################
# CancelDrawDemonstrateButton class
####################################
class CancelDrawDemonstrateButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return

        await interaction.response.edit_message(content = "⚠️ 系統提示：已關閉抽卡結果", 
                                                embed = None,
                                                view = None)