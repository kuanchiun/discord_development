import math
from dataclasses import asdict, dataclass, field
from pathlib import Path
from random import choice
from typing import List, Optional, Union

import discord
from discord import Embed, Interaction, Member
from discord.ui import Button, View

import yaml

from .job_attribute import *
#from .job import Job, get_job_list
from .player import ATTRIBUTE, PlayerAttribute


def get_player_embed(user: Member) -> Embed:
    player = PlayerAttribute.load(user.id)
    job = JOB_MAP[player.job_type]
    
    hp = job.calculate_hp(player.level, player.VIT)
    defense = job.calculate_defense(player.level, player.VIT)
    min_physical_attack, max_physical_attack = job.calculate_physical_attack(player.level, player.STR, player.LUK)
    min_magic_attack, max_magic_attack = job.calculate_magic_attack(player.level, player.INT, player.LUK)
    critical_rate = job.calculate_critical_rate(player.LUK) * 100
    hit = job.calculate_hit(player.level, player.MND)
    sidestep = job.calculate_sidestep(player.level, player.DEX)
    speed = job.calculate_speed(player.DEX)
    
    embed = Embed(
        title = f"{user.display_name} 的角色資訊",
        description = f"🎖️ 職業：`{player.job}`\n"
                      f"📈 等級：`Lv.{player.level}`\n"
                      f"🧪 經驗值：`{player.experience} / {player.exp_total(player.level + 1) if player.level < 50 else "最大等級"}`",
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

    embed.add_field(
        name = "【角色能力值】",
        value = (
            "```" +
            f"💖血量: {hp:>4}  ⚔️物攻: {min_physical_attack} - {max_physical_attack}\n" + 
            f"🛡️防禦: {defense:>4}  🔮魔攻: {min_magic_attack} - {max_magic_attack}\n" + 
            f"🎯命中: {hit:>4}  🎲爆擊機率: {critical_rate:>3}%\n" +
            f"🌀迴避: {sidestep:>4}  💨行動速度: {speed:>3}" +
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