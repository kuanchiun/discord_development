from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import View
from typing import List

from .draw_all_view import DrawAllView
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
        self.message = None 
        
        self.add_item(ShowAllDrawResultsButton(user = user, 
                                               label = "一次展示", 
                                               embeds = embeds))
        self.add_item(ShowSingleDrawResultButton(user = user, 
                                                  label = "單張個別展示", 
                                                  embeds = embeds,
                                                  single_embeds = single_embeds))
        self.add_item(CloseDrawDemonstrateButton(user = user,
                                                  label = "關閉介面"))
    
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉介面",
                view = None
            )
        return 
    
    
#################################
# DrawOnceDemonsrateButton class
#################################
class ShowAllDrawResultsButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, embeds: List[Embed]):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.embeds = embeds
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        view = DrawAllView(self.embeds, self.user)
        await interaction.response.edit_message(
            content = f"⚠️ 系統提示：**{self.user.display_name}** 的十連抽結果：第 1 / 2 頁",
            embed = view.embeds[0],
            view = view
        )
        view.message = await interaction.original_response()
        return
        

####################################
# DrawSingleDemonstrateButton class
####################################
class ShowSingleDrawResultButton(BaseUserRestrictedButton):
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
        view.message = await interaction.original_response()
        return

###################################
# CloseDrawDemonstrateButton class
###################################
class CloseDrawDemonstrateButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return

        await interaction.response.edit_message(content = "⚠️ 系統提示：已關閉抽卡結果", 
                                                embed = None,
                                                view = None)
        return