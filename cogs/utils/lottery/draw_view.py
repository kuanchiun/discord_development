from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import View

from ..basebutton import BaseUserRestrictedButton

#####################
# BaseDrawView class
#####################
class BaseDrawView(View):
    def __init__(self, embed: Embed, user: Member, timeout: int = 30):
        super().__init__(timeout = timeout)
        self.embed = embed
        self.user = user
        
#################
# DrawView class
#################
class DrawView(BaseDrawView):
    def __init__(self, embed: Embed, user: Member, timeout: int = 60):
        super().__init__(embed = embed, user = user, timeout = timeout)
        self.message = None
        
        self.add_item(PublicDrawButton(user = user, label = "📢 公開顯示", embed = embed))
        self.add_item(CloseDrawButton(user = user, label = "關閉抽卡介面"))
    
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉介面",
                embed = None,
                view = None
            )
        return

#######################
# PublicDrawView class
#######################
class PublicDrawView(BaseDrawView):
    def __init__(self, embed: Embed, user: Member, timeout: int = 60):
        super().__init__(embed = embed, user = user, timeout = timeout)
        self.message = None

#########################
# PublicDrawButton class
#########################
class PublicDrawButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, embed: Embed):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.embed = embed
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        view = PublicDrawView(self.embed, self.user)
        await interaction.response.send_message(
            content = f"⚠️ 系統提示：🎁 {interaction.user.display_name} 公開了他的單抽結果",
            embed = self.embed,
            view = view)
        view.message = await interaction.original_response()
        return

########################
# CloseDrawButton class
########################
class CloseDrawButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return

        await interaction.response.edit_message(content = "⚠️ 系統提示：已關閉抽卡結果", 
                                                embed = None,
                                                view = None)
        return