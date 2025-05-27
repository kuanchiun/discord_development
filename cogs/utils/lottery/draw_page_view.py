from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import Button, View
from typing import List

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
        self.add_item(CancelDrawPageButton("關閉介面", user = user))

        self.update_button_state()

    def update_button_state(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.total_pages - 1

class DrawEmbedPageView(BaseDrawPageView):
    def __init__(self, embeds: List[Embed], user: Member):
        from .draw_public_button import PublicDrawEmbedButton
        super().__init__(embeds = embeds, user = user, timeout = 30)
        self.public_button = PublicDrawEmbedButton(embeds, user)
        self.add_item(self.public_button)

class PublicDrawEmbedPageView(BaseDrawPageView):
    def __init__(self, embeds: List[Embed], user: Member):
        super().__init__(embeds = embeds, user = user, timeout = 60)

class DrawPreviousPageButton(Button):
    def __init__(self, label: str, user: Member):
        super().__init__(label = label, style = ButtonStyle.primary)
        self.user = user
    
    async def callback(self, interaction: Interaction):
        view: BaseDrawPageView = self.view
        view.current_page -= 1
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"⚠️ 系統提示：**{self.user.display_name}** 的十連抽結果：第 {view.current_page + 1} / {view.total_pages} 頁",
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
            content = f"⚠️ 系統提示：**{self.user.display_name}** 的十連抽結果：第 {view.current_page + 1} / {view.total_pages} 頁",
            embed = view.embeds[view.current_page],
            view = view
        )

class CancelDrawPageButton(Button):
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