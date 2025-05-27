from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import Button
from typing import List

from .draw_page_view import PublicDrawEmbedPageView

##############################
# PublicDrawEmbedButton class
##############################
class PublicDrawEmbedButton(Button):
    def __init__(self, embeds: List[Embed], user: Member):
        super().__init__(label = "📢 公開顯示", style = ButtonStyle.primary)
        self.embeds = embeds
        self.user = user

    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的抽獎結果喔！", ephemeral=True)
            return
        
        view = PublicDrawEmbedPageView(self.embeds, self.user)
        msg = await interaction.response.send_message(
            content = f"⚠️ 系統提示：{interaction.user.display_name} 公開了他的十連抽結果：第 1 / {len(self.embeds)} 頁",
            embed = self.embeds[0],
            view = view  # ✅ 使用公開版本
        )
        view.message = await interaction.original_response()