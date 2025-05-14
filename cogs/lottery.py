import discord
from discord.ext import commands
from discord import app_commands
import random
import yaml
import os
from typing import List

POOL_PATH = "yaml/lottery_pool.yaml"

RARITY_WEIGHTS = {
    "UR": 1,
    "SSR": 5,
    "SR": 10,
    "R": 20,
    "N": 64,
    "miss": 0
}

class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = self.load_pool()

    def load_pool(self):
        with open(POOL_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    def draw_item(self):
        # 池中篩選稀有度
        rarities = list(RARITY_WEIGHTS.keys())
        weights = list(RARITY_WEIGHTS.values())
        chosen_rarity = random.choices(rarities, weights=weights, k=1)[0]

        if chosen_rarity == "miss":
            return {"name": "什麼都沒抽到...", "image": None, "rarity": "miss"}

        candidates = self.pool.get(chosen_rarity, [])
        if not candidates:
            return {"name": f"[{chosen_rarity}] 目前尚無獎品", "image": None, "rarity": chosen_rarity}

        return random.choice(candidates)
    
    def create_embed(self, user: discord.User, item: dict):
        embed = discord.Embed(title=f"{user.display_name} 的抽獎結果",
                              description=f"🎁 你抽到了：**{item['name']}**",
                              color=discord.Color.gold())
        embed.set_footer(text=f"稀有度：{item['rare']}")
        return embed
    
    @app_commands.command(name="抽獎", description="抽一次獎")
    async def draw(self, interaction: discord.Interaction):
        results = self.draw_item()
        
        embed = self.create_embed(interaction.user, results)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Lottery(bot))
    