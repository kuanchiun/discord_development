from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import View
from typing import List

from ..basebutton import BaseUserRestrictedButton

###########################
# BaseDrawSingleView class
###########################
class BaseDrawSingleView(View):
    def __init__(self, 
                 user: Member,
                 embeds: List[Embed], 
                 single_embeds: List[Embed],
                 timeout = 30):
        
        super().__init__(timeout = timeout)
        self.user = user
        self.embeds = embeds
        self.single_embeds = single_embeds
        self.message = None
        
        self.current_page = 0
        self.total_pages = len(single_embeds)
        
        self.previous_button = DrawSinglePreviousPageButton(user = user, label = "⬅ 上一頁")
        self.next_button = DrawSingleNextPageButton(user = user, label = "➡ 下一頁")
        
        self.add_item(self.previous_button)
        self.add_item(self.next_button)
        
        self.update_button_state()
        
    def update_button_state(self):
        self.next_button.disabled = self.current_page >= self.total_pages - 1
    
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉抽卡結果。",
                embed = None,
                view = None
            )

#######################
# DrawSingleView class
#######################
class DrawSingleView(BaseDrawSingleView):
    def __init__(self, 
                 user: Member,
                 embeds: List[Embed], 
                 single_embeds: List[Embed],
                 timeout = 30):
        super().__init__(user = user,
                         embeds = embeds,
                         single_embeds = single_embeds,
                         timeout = timeout)

        self.public_button = PublicDrawSingleButton(user = user, 
                                                    label = "📢 公開顯示",
                                                    embeds = embeds, 
                                                    single_embeds = single_embeds)
        self.add_item(self.public_button)
        
        self.close_button = CloseDrawSingleButton(user = user, label = "關閉介面")
        self.add_item(self.close_button)

#######################
# DrawSingleView class
#######################
class PublicDrawSingleView(BaseDrawSingleView):
    def __init__(self, 
                 user: Member,
                 embeds: List[Embed], 
                 single_embeds: List[Embed],
                 timeout = 60):
        super().__init__(user = user,
                         embeds = embeds,
                         single_embeds = single_embeds,
                         timeout = timeout)
    
#####################################
# DrawSinglePreviousPageButton class
#####################################
class DrawSinglePreviousPageButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        view: BaseDrawSingleView = self.view
        view.current_page -= 1
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"**{self.user.display_name}** 的十連抽結果：第 {view.current_page + 1} / {view.total_pages}",
            embed = view.single_embeds[view.current_page],
            view = view
        )    

#################################
# DrawSingleNextPageButton class
#################################
class DrawSingleNextPageButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        view: BaseDrawSingleView = self.view
        view.current_page += 1
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"**{self.user.display_name}** 的十連抽結果：第 {view.current_page + 1} / {view.total_pages}",
            embed = view.single_embeds[view.current_page],
            view = view
        )
        
##############################
# PublicDrawSingleButton class
##############################
class PublicDrawSingleButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, embeds: List[Embed], single_embeds: List[Embed]):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.embeds = embeds
        self.single_embeds = single_embeds

    async def callback(self, interaction: Interaction):
        view = PublicDrawSingleView(user = self.user, 
                                    embeds = self.embeds, 
                                    single_embeds = self.single_embeds)
        await interaction.response.send_message(
            content = f"⚠️ 系統提示：{interaction.user.display_name} 公開了他的十連抽結果：第 1 / {len(self.single_embeds)} 頁",
            embed = self.single_embeds[0],
            view = view  # ✅ 使用公開版本
        )
        view.message = await interaction.original_response()

##############################
# CloseDrawSingleButton class
##############################
class CloseDrawSingleButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的介面喔", 
                                                    ephemeral = True)
            return

        await interaction.response.edit_message(content = "⚠️ 系統提示：已關閉抽卡結果", 
                                                embed = None,
                                                view = None)