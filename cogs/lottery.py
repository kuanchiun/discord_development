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
    
    @commands.command(name = "獎池裝備一覽")
    async def show_all_equipments_in_pool(self, ctx):
        embed = Embed(
            title = f"📦 所有裝備一覽",
            color = discord.Color.gold()
        )
        embed.set_image(url = "https://raw.githubusercontent.com/kuanchiun/discord_development/main/figures/all_equipments.png")
        embed.set_footer(text=f"總計：36 件裝備\n最後更新：2025-05-18")
        await ctx.send(embed = embed)
    
    @commands.command(name = "武器一覽")
    async def show_all_equipments_in_pool(self, ctx, career: str):
        career_map = {
            "劍術師": "sword",
            "弓箭手": "bow",
            "法師": "mage",
            "盜賊": "thief"
        }
        if career not in ["劍術師", "弓箭手", "法師", "盜賊"]:
            await ctx.send("沒有這個職業喔！")
            return
        
        embed = Embed(
            title = f"📦 {career}武器一覽",
            color = discord.Color.gold()
        )
        embed.set_image(url = f"https://raw.githubusercontent.com/kuanchiun/discord_development/main/figures/{career_map[career]}_weapons.png")
        embed.set_footer(text=f"最後更新：2025-05-18")
        await ctx.send(embed = embed)

async def setup(bot):
    await bot.add_cog(Lottery(bot))