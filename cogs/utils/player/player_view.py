import yaml
import math
import discord

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional, List, Union
from random import choice

from discord import Embed, Member, Interaction
from discord.ui import Button, View

from .player import Player

#########################
# ConfirmResetView class
#########################
class ConfirmResetView(View):
    def __init__(self, user: Member):
        super().__init__(timeout = 30)
        self.user = user
        self.user_id = user.id
        
        self.add_item(ConfirmResetButton("⚠️ 確認初始化", self.user, self.user_id))
        self.add_item(CancelResetButton("❌ 取消初始化", self.user))
        
###########################
# ConfirmResetButton class
###########################
class ConfirmResetButton(Button):
    def __init__(self, label: str, user: Member, user_id: int):
        super().__init__(label = label, style = discord.ButtonStyle.danger)
        self.user = user
        self.user_id = user_id
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：你不能初始化別人的角色！",
                                                    ephemeral = True)
            return
        
        player = Player()
        player.iteminventory.add_money(10000)
        player.save(self.user_id)
        await interaction.response.edit_message(content = "⚠️ 系統提示：已初始化角色！獲得發財金💎10000！", 
                                                view = None)
 
##########################
# CancelResetButton class
##########################
class CancelResetButton(Button):
    def __init__(self, label: str, user: Member):
        super().__init__(label = label, style = discord.ButtonStyle.secondary)
        self.user = user
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的介面喔", 
                                                    ephemeral = True)
            return

        await interaction.response.edit_message(content = "⚠️ 系統提示：已取消初始化角色。", 
                                                view = None)