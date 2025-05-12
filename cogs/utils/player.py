import yaml
import math
import discord

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional, List, Union
from random import choice

from discord import Embed, Member, Interaction
from discord.ui import Button, View

from .job import Job, get_job_list

A = 15
ALPHA = 1.5
B = 1

MAX_LEVEL = 50
POINT_PER_LEVEL = 5
INITIAL_POINT = 25

PLAYER_SAVEPATH = Path("players_attribute")
EQUIPMENT_SAVEPATH = Path("player_equipment")
ATTRIBUTE = [
    "VIT",
    "STR",
    "INT",
    "DEX",
    "MND",
    "LUK"
]

@dataclass
class PlayerAttribute:
    job: str = "見習生"
    skills: list = field(default_factory = lambda: ["直拳", 
                                                    "掃腿", 
                                                    "肩撞",
                                                    "基礎治療"])
    
    level: int = 1
    experience: int = 0
    
    VIT: int = 0
    STR: int = 0
    INT: int = 0
    DEX: int = 0
    MND: int = 0
    LUK: int = 0
    
    remind_point: int = INITIAL_POINT
    
    @classmethod
    def exists(cls, user_id: int) -> bool:
        file_path = PLAYER_SAVEPATH / f"{user_id}.yml"
        return file_path.exists()
    
    @classmethod
    def load(cls, user_id: int) -> "PlayerAttribute":
        PLAYER_SAVEPATH.mkdir(exist_ok = True)
        file_path = PLAYER_SAVEPATH / f"{user_id}.yml"
        
        if file_path.exists():
            with open(file_path, "r", encoding = "utf-8") as f:
                data = yaml.safe_load(f)
            return cls(**data)
        else:
            return cls()
    
    def save(self, user_id: int) -> None:
        PLAYER_SAVEPATH.mkdir(exist_ok = True)
        file_path = PLAYER_SAVEPATH / f"{user_id}.yml"
        
        with open(file_path, "w", encoding = "utf-8") as f:
            yaml.safe_dump(asdict(self), f, allow_unicode = True)
    
    def add_attribute_point(self, attribute, point = 1):
        if self.remind_point < point or attribute not in ATTRIBUTE:
            return False
        setattr(self, attribute, getattr(self, attribute) + point)
        self.remind_point -= point
        return True
            
    def add_experience(self, experience):
        self.experience += experience
    
    def exp_total(self, level: int) -> int:
        return round(A * (level ** ALPHA) * math.log(level + B))
            
    def get_level_by_exp(self) -> int:
        for level in range(1, MAX_LEVEL + 1):
            if self.exp_total(level) > self.experience:
                return level - 1
        return MAX_LEVEL
    
    def level_up(self) -> Union[str, None]:
        level = self.get_level_by_exp()
        if level <= self.level:
            return None
        else:
            self.remind_point += POINT_PER_LEVEL * (level - self.level)
            self.level = level
            return f"升級！ 您的等級目前為 {self.level}"
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    def promote_job(self, job_name, user_id) -> str:
        job_list = get_job_list()
        next_job = job_list[job_name]
        
        if self.level >= next_job.required_level:
            self.job = job_name
            self.save(user_id)
            return True
        else:
            return False

def get_player_embed(user: Member) -> Embed:
    player = PlayerAttribute.load(user.id)
    
    embed = Embed(
        title = f"{user.display_name} 的角色資訊",
        description = f"🎖️ 職業：`{player.job}`\n"
                      f"📈 等級：`Lv.{player.level}`\n"
                      f"🧪 經驗值：`{player.experience} / {player.exp_total(player.level + 1)}`",
        color = 0x00BFFF
    )
    
    embed.add_field(
        name = "【玩家屬性】",
        value = (
            "```" +
            f"VIT: {player.VIT:>4}  STR: {player.STR:>4}\n" + 
            f"INT: {player.INT:>4}  DEX: {player.DEX:>4}\n" + 
            f"MND: {player.MND:>4}  LUK: {player.LUK:>4}" + 
            "```"
        ),
        inline = False
    )
    
    embed.set_thumbnail(url = user.display_avatar.url)
    
    return embed

def get_player_embed_for_point(user: Member) -> Embed:
    player = PlayerAttribute.load(user.id)
    
    embed = Embed(
        title = f"{user.display_name} 的角色配點資訊",
        description = f"VIT: 血量與防禦\n"
                      f"STR: 基礎物理攻擊\n"
                      f"INT: 基礎魔法攻擊\n"
                      f"DEX: 迴避機率與行動速度\n"
                      f"MND: 命中機率與持續性傷害\n"
                      f"LUK: 爆擊機率\n",
        color = 0x00BFFF
    )
    
    embed.add_field(name = "VIT", value = f"`{player.VIT}`", inline = True)
    embed.add_field(name = "STR", value = f"`{player.STR}`", inline = True)
    
    embed.add_field(name = "INT", value = f"`{player.INT}`", inline = True)
    embed.add_field(name = "DEX", value = f"`{player.DEX}`", inline = True)
    
    embed.add_field(name = "MND", value = f"`{player.MND}`", inline = True)
    embed.add_field(name = "LUK", value = f"`{player.LUK}`", inline = True)
    
    embed.add_field(name = "尚餘可用點數", value = f"`{player.remind_point}`", inline = True)
    
    return embed

class AssignAttributeView(View):
    def __init__(self, player: PlayerAttribute, user: Member):
        super().__init__(timeout = 120)
        self.player = player
        self.user = user
        
        for i, attribute in enumerate(ATTRIBUTE):
            self.add_item(AssignButton(label = attribute, 
                                       attribute = attribute, 
                                       row = i // 2)
                          )
            self.add_item(AssignButtonFiveX(label = attribute, 
                                       attribute = attribute, 
                                       row = i // 2)
                          )
        
        self.add_item(RandomAssignButton(row = 4))
        self.add_item(ConfirmAssignButton(row = 4))
    
    async def update_embed(self, interaction: Interaction):
        embed = get_player_embed_for_point(self.user)
        await interaction.response.edit_message(embed = embed, view = self)

class AssignButton(Button):
    def __init__(self, label: str, attribute: str, row: int):
        super().__init__(label = f"{label} +1", style = discord.ButtonStyle.primary, row = row)
        self.attribute = attribute
    
    async def callback(self, interaction: Interaction):
        view: AssignAttributeView = self.view
        if interaction.user != view.user:
            await interaction.response.send_message("⚠️ 這不是你的介面喔", ephemeral = True)
            return
        success = view.player.add_attribute_point(self.attribute, 1)
        if success:
            view.player.save(view.user.id)
            await view.update_embed(interaction)
        else:
            await interaction.response.send_message("⚠️ 沒有剩餘點數或屬性無效", ephemeral = True)

class AssignButtonFiveX(Button):
    def __init__(self, label: str, attribute: str, row: int):
        super().__init__(label = f"{label} +5", style = discord.ButtonStyle.primary, row = row)
        self.attribute = attribute
    
    async def callback(self, interaction: Interaction):
        view: AssignAttributeView = self.view
        if interaction.user != view.user:
            await interaction.response.send_message("⚠️ 這不是你的介面喔", ephemeral = True)
            return
        success = view.player.add_attribute_point(self.attribute, 5)
        if success:
            view.player.save(view.user.id)
            await view.update_embed(interaction)
        else:
            await interaction.response.send_message("⚠️ 沒有剩餘點數或屬性無效", ephemeral = True)

class RandomAssignButton(Button):
    def __init__(self, row: int):
        super().__init__(label = "🎲隨機分配", style = discord.ButtonStyle.primary, row = row)
    
    async def callback(self, interaction: Interaction):
        view: AssignAttributeView = self.view
        if interaction.user != view.user:
            await interaction.response.send_message("⚠️ 這不是你的介面喔", ephemeral = True)
            return
        try:
            for i in range(0, view.player.remind_point):
                random_attribute = choice(ATTRIBUTE)
                view.player.add_attribute_point(random_attribute, 1)
            view.player.save(view.user.id)
            await view.update_embed(interaction)
        except:
            await interaction.response.send_message("⚠️ 出現異常錯誤，請重試", ephemeral = True)
            
class ConfirmAssignButton(Button):
    def __init__(self, row: int):
        super().__init__(label = "✅ 結束分配", style = discord.ButtonStyle.primary, row = row)
    
    async def callback(self, interaction: Interaction):
        view: AssignAttributeView = self.view
        if interaction.user != view.user:
            await interaction.response.send_message("⚠️ 這不是你的介面喔", ephemeral = True)
            return
        
        await interaction.response.edit_message(content = "配點完成，關閉介面", view = None)

class ConfirmResetView(View):
    def __init__(self, user_id: int, user):
        super().__init__(timeout = 60)
        self.user_id = user_id
        self.user = user
        
        self.add_item(ConfirmResetButton("⚠️ 確認初始化", user_id, user))
        self.add_item(CancelResetButton("❌ 取消初始化", user))
        
class ConfirmResetButton(Button):
    def __init__(self, label: str, user_id: int, user):
        super().__init__(label = label, style = discord.ButtonStyle.danger)
        self.user_id = user_id
        self.user = user

    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("❌ 你不能初始化別人的角色。", ephemeral=True)
            return

        player = PlayerAttribute()
        player.save(self.user_id)
        await interaction.response.edit_message(content = "✅ 已初始化角色。", view = None)

class CancelResetButton(Button):
    def __init__(self, label: str, user):
        super().__init__(label = label, style = discord.ButtonStyle.secondary)
        self.user = user

    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 這不是你的介面喔", ephemeral = True)
            return

        await interaction.response.edit_message(content = "已取消初始化角色。", view = None)