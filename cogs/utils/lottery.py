import discord
from discord.ext import commands
from discord import app_commands, Embed, Member, Interaction
from discord.ui import View, Button, button
import random
import yaml
from typing import Dict

LOTTERY_POOL_PATH = "yaml/equipment_pool.yaml"
RARITY_WEIGHTS = {
    "UR": 1, 
    "SR": 10,
    "R": 29,
    "N": 60
}
PART_MAPPING = {
    "pre-weapon": "原型武器",
    "head": "頭部",
    "chest": "上身",
    "legs": "腿部",
    "feet": "腳部",
    "earring": "耳環",
    "necklace": "項鍊",
    "bracelet": "手鐲",
    "ring": "戒指"
}

def load_lottery_pool():
    with open(LOTTERY_POOL_PATH, "r", encoding = "utf-8") as f:
        return yaml.safe_load(f)
    
def draw_item(lottery_pool: Dict) -> Dict:
    rarity = list(RARITY_WEIGHTS.keys())
    weights = list(RARITY_WEIGHTS.values())
    
    chosen_rarity = random.choices(rarity, weights=weights, k=1)[0]
    
    candidates = lottery_pool.get(chosen_rarity, [])
    if not candidates:
        return None
    
    loot = random.choice(candidates)
    
    return loot

def get_lottery_embed(loot: Dict, user: Member) -> Embed:
    embed = Embed(
        title = f"{user.display_name} 的抽獎結果",
        description = f"🎁 你抽到了：**{loot['name']}**",
        color = discord.Color.gold()
    )
    
    info_lines = []
    info_lines.append(f"💎 稀有度： {loot["rarity"]}")
    if loot.get("part"):
        info_lines.append(f"👕 裝備分類： {PART_MAPPING[loot["part"]]}")
    if loot.get("maxlevel"):
        info_lines.append(f"🧬 最大等級： {loot["maxlevel"]}")
    if loot.get("sockets"):
        info_lines.append(f"🔘 可鑲嵌孔洞： {loot["sockets"]}")
        
    embed.add_field(
        name="【物品資訊】",
        value="```" + "\n".join(info_lines) + "```",
        inline=False
    )
    
    if loot["image"]:
        embed.set_thumbnail(url = loot["image"])
    
    return embed

class LotteryView(View):
    def __init__(self, embed: Embed, user: Member):
        super().__init__(timeout = 30)
        self.embed = embed
        self.user = user
        
        self.add_item(LotteryPublicButton(embed))

class LotteryPublicButton(Button):
    def __init__(self, embed: Embed):
        super().__init__(label = "📢 公開顯示", 
                         style = discord.ButtonStyle.primary)
        self.embed = embed
    
    async def callback(self, interaction: Interaction):
        view: LotteryView = self.view
        if interaction.user != view.user:
            await interaction.response.send_message("❌ 這不是你的抽獎結果喔！", ephemeral = True)
            return
        
        await interaction.response.defer()
        await interaction.followup.send(embed = self.embed)
        
        self.disabled = True 
        self.view.stop()      