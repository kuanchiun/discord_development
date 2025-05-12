import yaml
import discord

from dataclasses import dataclass, asdict, field
from typing import Optional, List, Dict

from discord import Embed, Member, Interaction
from discord.ui import Button, View

FILE_PATH = "yaml/job.yml"

@dataclass
class Job:
    name: str
    description: str
    
    skills: List[str]
    
    next_job: Optional[List[str]] = field(default_factory = list)
    required_level: Optional[int] = None


def get_job_list() -> Dict[str, Job]:
    with open(FILE_PATH, "r", encoding = "utf-8") as f:
        jobs = yaml.safe_load(f)
        
    job_list = {}
    for job_type in jobs["jobs"]:
        for job in jobs["jobs"][job_type]:
            job_list[job["name"]] = Job(**job)
        
    return job_list

def get_job_embed(user: Member) -> Embed:
    from .player import PlayerAttribute
    player = PlayerAttribute.load(user.id)
    job_list = get_job_list()
    
    current_job = job_list[player.job]
    
    if not current_job.next_job:
        return Embed(title = "系統資訊", description = f"❌ `{current_job.name}` 該職業已是最高級職業！", color = 0xFF5555)
    
    job_options = [job_list[next_job] for next_job in current_job.next_job]
    embed = Embed(title="可轉職職業選項", color=0x00BFFF)
    
    for job in job_options:
        skill_text = ", ".join(job.skills)
        embed.add_field(
            name = job.name,
            value = f"{job.description}\n 技能：`{skill_text}`",
            inline = False
        )
    
    return embed

class TransferJobView(View):
    from .player import PlayerAttribute
    def __init__(self, player: PlayerAttribute, user: Member):
        super().__init__(timeout = 120)
        self.player = player
        self.user = user
        self.job_list = get_job_list()
        
        current_job = self.job_list[player.job]
        job_options = [self.job_list[next_job] for next_job in current_job.next_job]
        
        for job in job_options:
            self.add_item(
                TransferButton(label = job.name, user = self.user)
            )
        
        self.add_item(CancelTransferButton(user = self.user, label = "❌ 取消轉職"))

class TransferButton(Button):
    def __init__(self, label: str, user: Member):
        super().__init__(label = f"{label}", style = discord.ButtonStyle.primary)
        self.user = user
        self.job_list = get_job_list()
    
    async def callback(self, interaction: Interaction):
        view: TransferJobView = self.view
        if interaction.user != view.user:
            await interaction.response.send_message("⚠️ 這不是你的介面喔", ephemeral = True)
            return
        next_job = self.job_list[self.label]
        if view.player.level >= next_job.required_level:
            view.player.promote_job(self.label, self.user.id)
            await interaction.response.edit_message(content = f"✅ 已成功轉職為`{self.label}`！", view = None)
        else:
            await interaction.response.edit_message(content = f"❌ 你的等級尚未達到轉職`{self.label}`的條件", view = None)

class CancelTransferButton(Button):
    def __init__(self, label: str, user):
        super().__init__(label = label, style = discord.ButtonStyle.secondary)
        self.user = user
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 這不是你的介面喔", ephemeral = True)
            return

        await interaction.response.edit_message(content = "已取消角色轉職。", view = None)