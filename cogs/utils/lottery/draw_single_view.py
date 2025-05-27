from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import Button, View
from typing import List

from .draw_public_button import PublicDrawEmbedButton

class DrawSingleView(View):
    def __init__(self, 
                 user: Member,
                 embeds: List[Embed], 
                 single_embeds: List[Embed],
                 timeout = 30):
        super().__init__(timeout = timeout)
        self.user = user
        self.embeds = embeds
        self.single_embeds = single_embeds
        
        self.current_page = 0
        self.total_pages = len(single_embeds)
        
        self.next_button = DrawSingleNextPageButton(label = "➡ 下一個", user = user)
        self.public_button = PublicDrawEmbedButton(embeds = embeds, user = user)
        self.end_button = CancelDrawSingleButton(label = "關閉介面", user = user)
        
        self.add_item(self.next_button)
        self.add_item(self.public_button)
        self.add_item(self.end_button)
        
        self.update_button_state()
        
    def update_button_state(self):
        self.next_button.disabled = self.current_page >= self.total_pages - 1
    
class DrawSingleNextPageButton(Button):
    def __init__(self, label: str, user: Member):
        super().__init__(label = label, style = ButtonStyle.primary)
        self.user = user
    
    async def callback(self, interaction: Interaction):
        view: DrawSingleView = self.view
        view.current_page += 1
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"**{self.user.display_name}** 的十連抽結果：第 {view.current_page + 1} / {view.total_pages}",
            embed = view.single_embeds[view.current_page],
            view = view
        )

class CancelDrawSingleButton(Button):
    def __init__(self, label: str, user: Member):
        super().__init__(label = label, style = ButtonStyle.secondary)
        self.user = user
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的介面喔", 
                                                    ephemeral = True)
            return

        await interaction.response.edit_message(content = "⚠️ 系統提示：已關閉抽卡結果", 
                                                embed = None,
                                                view = None)