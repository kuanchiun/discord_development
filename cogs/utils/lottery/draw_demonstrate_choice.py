from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import Button, View
from typing import List

from .draw_page_view import DrawEmbedPageView
from .draw_single_view import DrawSingleView

class DrawDemonstrateView(View):
    def __init__(self, 
                 user: Member,
                 embeds: List[Embed], 
                 single_embeds: List[Embed],
                 timeout = 30):
        super().__init__(timeout = timeout)
        
        self.add_item(DrawOnceDemonsrateButton("一次展示", 
                                               user = user, 
                                               embeds = embeds))
        self.add_item(DrawSingleDemonstrateButton("單張個別展示", 
                                                  user = user, 
                                                  embeds = embeds,
                                                  single_embeds = single_embeds))
        

class DrawOnceDemonsrateButton(Button):
    def __init__(self, label: str, user: Member, embeds: List[Embed]):
        super().__init__(label = label, style = ButtonStyle.primary)
        self.user = user
        self.embeds = embeds
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的介面喔", 
                                                    ephemeral = True)
            return
        
        view = DrawEmbedPageView(self.embeds, self.user)
        await interaction.response.edit_message(
            content = f"⚠️ 系統提示：**{self.user.display_name}** 的十連抽結果：第 1 / 2 頁",
            embed = view.embeds[0],
            view = view
        )

class DrawSingleDemonstrateButton(Button):
    def __init__(self, 
                 label: str, 
                 user: Member, 
                 embeds: List[Embed],
                 single_embeds: List[Embed]):
        super().__init__(label = label, style = ButtonStyle.primary)
        self.user = user
        self.embeds = embeds
        self.single_embeds = single_embeds
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的介面喔", 
                                                    ephemeral = True)
            return
        
        view = DrawSingleView(user = self.user,
                              embeds = self.single_embeds,
                              single_embeds = self.single_embeds)
        await interaction.response.edit_message(
                content = f"**{self.user.display_name}** 的十連抽結果：第 1 / 10",
                embed = view.single_embeds[0],
                view = view
        )
        