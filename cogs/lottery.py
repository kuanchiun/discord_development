import discord
import asyncio
import pickle

from discord.ext import commands
from discord import app_commands, Interaction, Embed, Member

from .utils.player.player import Player
from .utils.lottery.lottery import Lottery
from .utils.lottery.lottery_view import DrawLotteryView


class LotteryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lottery = Lottery()
        
    @app_commands.command(name = "抽獎")
    async def draw(self, interaction: Interaction):
        user = interaction.user
        user_id = interaction.user.id
        
        if Player.exists(user_id):
            view = DrawLotteryView(user, self.lottery)
            await interaction.response.send_message(
                content = "系統提示：抽獎！",
                view = view,
                ephemeral = True
            )
        else:
            await interaction.response.send_message(
                content = "⚠️ 系統提示：你尚未創建角色！",
            )
    
async def setup(bot):
    await bot.add_cog(LotteryCog(bot))