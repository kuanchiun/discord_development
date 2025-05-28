from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import Button, View
from typing import List

from ..basebutton import BaseUserRestrictedButton

#########################
# BaseDrawPageView class
#########################
class BaseDrawPageView(View):
    def __init__(self, embeds: List[Embed], user: Member, timeout: int = 30):
        super().__init__(timeout = timeout)
        self.embeds = embeds
        self.user = user
        self.current_page = 0
        self.total_pages = len(embeds)
        self.message = None

        self.prev_button = DrawPreviousPageButton(user = user, label = "⬅ 上一頁")
        self.next_button = DrawNextPageButton(user = user, label = "➡ 下一頁")

        self.add_item(self.prev_button)
        self.add_item(self.next_button)

        self.update_button_state()

    def update_button_state(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.total_pages - 1
        
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉抽卡結果。",
                embed = None,
                view = None
            )

##########################
# DrawEmbedPageView class
##########################
class DrawEmbedPageView(BaseDrawPageView):
    def __init__(self, embeds: List[Embed], user: Member):
        super().__init__(embeds = embeds, user = user, timeout = 30)
        self.public_button = PublicDrawEmbedButton(user = user, label = "📢 公開顯示", embeds = embeds)
        self.add_item(self.public_button)
        self.add_item(CancelDrawPageButton(user = user, label = "關閉介面"))

################################
# PublicDrawEmbedPageView class
################################
class PublicDrawEmbedPageView(BaseDrawPageView):
    def __init__(self, embeds: List[Embed], user: Member):
        super().__init__(embeds = embeds, user = user, timeout = 60)

###############################
# DrawPreviousPageButton class
###############################
class DrawPreviousPageButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        view: BaseDrawPageView = self.view
        view.current_page -= 1
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"⚠️ 系統提示：**{self.user.display_name}** 的十連抽結果：第 {view.current_page + 1} / {view.total_pages} 頁",
            embed = view.embeds[view.current_page],
            view = view
        )

###########################
# DrawNextPageButton class
###########################
class DrawNextPageButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        view: BaseDrawPageView = self.view
        view.current_page += 1
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"⚠️ 系統提示：**{self.user.display_name}** 的十連抽結果：第 {view.current_page + 1} / {view.total_pages} 頁",
            embed = view.embeds[view.current_page],
            view = view
        )

#############################
# CancelDrawPageButton class
#############################
class CancelDrawPageButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return

        await interaction.response.edit_message(content = "⚠️ 系統提示：已關閉抽卡結果", 
                                                embed = None,
                                                view = None)

##############################
# PublicDrawEmbedButton class
##############################
class PublicDrawEmbedButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, embeds: List[Embed]):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.embeds = embeds

    async def callback(self, interaction: Interaction):
        view = PublicDrawEmbedPageView(user = self.user, embeds = self.embeds)
        await interaction.response.send_message(
            content = f"⚠️ 系統提示：{interaction.user.display_name} 公開了他的十連抽結果：第 1 / {len(self.embeds)} 頁",
            embed = self.embeds[0],
            view = view  # ✅ 使用公開版本
        )
        view.message = await interaction.original_response()