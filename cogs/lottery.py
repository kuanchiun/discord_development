import discord
import asyncio
import pickle
import os

from discord.ext import commands
from discord import app_commands, Interaction, Embed, Member

from .utils.job import Job, get_job_list, TransferJobView, get_job_embed
from .utils.player import *
from .utils.playerviews import *
from .utils.lottery import *

class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lottery_pool = load_lottery_pool()

    @app_commands.command(name = "抽獎")
    async def draw(self, interaction: discord.Interaction):
        user_id = interaction.user.id
        user = interaction.user
        
        loot = draw_item(self.lottery_pool)
        
        if PlayerAttribute.exists(user_id):
            embed = get_lottery_embed(loot, user)
            view = LotteryView(embed, user)
            await interaction.response.send_message(embed = embed, view = view, ephemeral = True)
        else:
            await interaction.response.send_message("⚠️ 你尚未創建角色喔！", ephemeral = True)
    
    @commands.command(name = "圖片測試")
    async def show_all_equipments(self, ctx):
        embed = Embed(
            title = f"📦 所有裝備一覽",
            color = discord.Color.gold()
        )
        embed.set_image(url = "https://raw.githubusercontent.com/kuanchiun/discord_development/main/figures/all_equipments.png")
        await ctx.send(embed = embed)

async def setup(bot):
    await bot.add_cog(Lottery(bot))