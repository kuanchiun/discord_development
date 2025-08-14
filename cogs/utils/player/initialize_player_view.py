import discord
from discord import Interaction, Member
from discord.ui import View

from ..basebutton import BaseUserRestrictedButton
from .player import Player


#########################
# ConfirmResetView class
#########################
class ConfirmResetView(View):
    def __init__(self, user: Member):
        super().__init__(timeout = 30)
        self.user = user
        self.message = None 
        
        self.add_item(ConfirmResetButton(user = user, label = "⚠️ 確認初始化"))
        self.add_item(CancelResetButton(user = user, label = "❌ 取消初始化"))
    
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，初始化取消。",
                view = None
            )
        return
        
###########################
# ConfirmResetButton class
###########################
class ConfirmResetButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = discord.ButtonStyle.danger)
        self.user_id = user.id
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        player = Player()
        player.iteminventory.add_money(10000)
        player.save(self.user_id)
        await interaction.response.edit_message(content = "⚠️ 系統提示：已初始化角色！獲得發財金💎10000！", 
                                                view = None)
        return
 
##########################
# CancelResetButton class
##########################
class CancelResetButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = discord.ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return

        await interaction.response.edit_message(content = "⚠️ 系統提示：已取消初始化角色。", 
                                                view = None)
        return