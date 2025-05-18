import yaml
import math
import discord

from abc import ABC, abstractmethod
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

PLAYER_SAVEPATH = Path("yaml/players_attribute")
EQUIPMENT_SAVEPATH = Path("yaml/player_equipment")
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
    job_type: str = "starter"
    skills: List = field(default_factory = lambda: ["直拳", 
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
            self.job_type = next_job.job_type
            self.save(user_id)
            return True
        else:
            return False
