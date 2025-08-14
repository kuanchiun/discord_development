import asyncio
import os
import pickle

import discord
from discord import Embed, Interaction, Member, app_commands
from discord.ext import commands

from .utils.player.initialize_player_view import ConfirmResetView
from .utils.player.player import Player


##################
# PlayerCog class
##################
class PlayerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name = "角色初始化", description = "初始化你的角色")
    async def initialize_character(self, interaction: Interaction):
        user = interaction.user
        user_id = interaction.user.id
        
        if Player.exists(user_id):
            view = ConfirmResetView(user)
            await interaction.response.send_message(
                content = "⚠️ 系統提示：\n你已經有角色了。是否確認要**初始化角色**？\n注意！這將會刪除現有資料。",
                view = view,
                ephemeral = True
            )
            message = await interaction.original_response()
            view.message = message
        else:
            player = Player()
            player.iteminventory.add_money(10000)
            player.save(user_id)
            await interaction.response.send_message("✅ 已成功建立角色！獲得發財金💎10000！", ephemeral = True)
        return
    
    
    @app_commands.command(name = "點數配置", description = "配置角色屬性")
    async def add_attribute(self, interaction: Interaction):
        ...
        
async def setup(bot: commands.Bot):
    await bot.add_cog(PlayerCog(bot))