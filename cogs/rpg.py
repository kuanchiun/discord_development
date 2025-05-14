import discord
import asyncio
import pickle
import os

from discord.ext import commands
from discord import app_commands, Interaction, Embed, Member

from .utils.job import Job, get_job_list, TransferJobView, get_job_embed
from .utils.player import *
from .utils.playerviews import *

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.job_list = get_job_list()
    
    @app_commands.command(name = "角色初始化", description = "初始化你的角色")
    async def initialize_character(self, interaction = Interaction):
        user_id = interaction.user.id
        
        if PlayerAttribute.exists(user_id):
            view = ConfirmResetView(user_id, interaction.user)
            await interaction.response.send_message(
            content = "⚠️ 你已經有角色了。是否確認要**初始化角色**？\n這將會刪除現有資料。",
            view = view,
            ephemeral  =True)
        else:
            player = PlayerAttribute()
            player.save(user_id)
            await interaction.response.send_message("✅ 已成功建立角色！", ephemeral = True)
    
    @app_commands.command(name = "配點", description = "配置角色點數")
    async def modify_character(self, interaction: Interaction):
        user_id = interaction.user.id
        user = interaction.user
        
        if PlayerAttribute.exists(user_id):
            player = PlayerAttribute.load(user_id)
            view = AssignAttributeView(player, user)
            await interaction.response.send_message(embed = get_player_embed_for_point(user), view = view, ephemeral = True)
        else:
            await interaction.response.send_message("⚠️ 你尚未創建角色喔！", ephemeral = True)
    
    @app_commands.command(name = "轉職職業查詢")
    async def check_transfer_job(self, interaction: Interaction):
        user_id = interaction.user.id
        user = interaction.user
        
        if PlayerAttribute.exists(user_id):
            embed = get_job_embed(user)
            await interaction.response.send_message(embed = embed, ephemeral = True)
        else:
            await interaction.response.send_message("⚠️ 你尚未創建角色喔！", ephemeral = True)
    
    @app_commands.command(name = "轉職")
    async def transfer_job(self, interaction: Interaction):
        user_id = interaction.user.id
        user = interaction.user
        
        if PlayerAttribute.exists(user_id):
            embed = get_job_embed(user)
            player = PlayerAttribute.load(user_id)
            current_job = self.job_list[player.job]
            if not current_job.next_job:
                await interaction.response.send_message(embed = embed, ephemeral = True)
                return
            view = TransferJobView(player, user)
            await interaction.response.send_message(embed = embed, view = view, ephemeral = True)
        else:
            await interaction.response.send_message("⚠️ 你尚未創建角色喔！", ephemeral = True)
    
    @commands.command(name = "角色資訊")
    async def show_character(self, ctx, user: discord.Member | str = ""):
        if user:
            user = user
        else:
            user = ctx.author
        
        if PlayerAttribute.exists(user.id):
            embed = get_player_embed(user)
            await ctx.send(embed = embed)
        else:
            await ctx.send("⚠️ 該用戶還沒有創建角色")
    
    @commands.command(name = "升級測試")
    async def level_up_test(self, ctx, experience: str | int):
        try:
            experience = int(experience)
        except:
            await ctx.send(f"經驗值必須為整數")
            return
        
        user = ctx.author
        
        if PlayerAttribute.exists(user.id):
            player = PlayerAttribute.load(user.id)
            player.add_experience(experience)
            text = player.level_up()
            player.save(user.id)
            if text:
                await ctx.send(f"你獲得了{experience}點經驗")
                await ctx.send(text)
            else:
                await ctx.send(f"你獲得了{experience}點經驗")
        else:
            await ctx.send("⚠️ 該用戶還沒有創建角色")

async def setup(bot):
    await bot.add_cog(Game(bot))