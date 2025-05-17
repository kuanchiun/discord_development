import discord
from discord.ext import commands
from discord import app_commands, Embed, Member, Interaction
from discord.ui import View, Button, button
import random
import yaml

POOL_PATH = "yaml/equipment_pool.yaml"

RARITY_WEIGHTS = {
    "UR": 1,
    "SR": 4,
    "R": 15,
    "N": 40,
    "miss": 40,
}

class LotteryView(View):
    def __init__(self, embed: Embed, user: Member):
        super().__init__(timeout=60)
        self.embed = embed
        self.user = user
        
    @button(label="📢 公開顯示", style=discord.ButtonStyle.primary)
    async def reveal_button(self, interaction: Interaction, button: Button):
        if interaction.user != self.user:
            await interaction.response.send_message("❌ 這不是你的抽獎結果喔！", ephemeral=True)
            return
        await interaction.response.defer()
        await interaction.followup.send(embed=self.embed)
        self.stop()
    

class Lottery(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool = self.load_pool()

    def load_pool(self):
        with open(POOL_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    
    def draw_item(self):
        # 池中篩選稀有度
        rarity = list(RARITY_WEIGHTS.keys())
        weights = list(RARITY_WEIGHTS.values())
        chosen_rarity = random.choices(rarity, weights=weights, k=1)[0]

        if chosen_rarity == "miss":
            return {"name": "什麼都沒抽到...", "image": None, "rarity": "miss"}

        candidates = self.pool.get(chosen_rarity, [])
        if not candidates:
            return {"name": f"[{chosen_rarity}] 目前尚無獎品", "image": None, "rarity": chosen_rarity}
        
        loot = random.choice(candidates)

        return loot
    
    def create_embed(self, user: discord.User, item: dict):
        embed = discord.Embed(title = f"{user.display_name} 的抽獎結果",
                              description = f"🎁 你抽到了：**{item['name']}**",
                              color = discord.Color.gold())
        embed.set_footer(text=f"稀有度：{item['rarity']}")
        if item["image"]:
            embed.set_thumbnail(url = item["image"])
        return embed
    
    @app_commands.command(name = "抽獎", description = "抽一次獎")
    async def draw(self, interaction: discord.Interaction):
        loot = self.draw_item()
        
        embed = self.create_embed(interaction.user, loot)
        await interaction.response.send_message(embed=embed, ephemeral=True, view=LotteryView(embed, interaction.user))
    
async def setup(bot):
    await bot.add_cog(Lottery(bot))
    