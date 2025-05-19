import discord

from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional
from discord.ui import View, Button
from discord import Embed, Member, Interaction

from .player import PlayerAttribute

'''
Effect 分為正面與負面
正面:
    # 提升傷害
    暴走 => target = "self", 根據職業轉數而定
    # 提升防禦
    減傷 => target = "self", 根據職業轉數而定
    # 回合補血
    自我回復 => target = "self", 根據職業轉數而定
    # 提升命中
    會心一擊 => target = "self", 根據職業轉數而定
    # 提升迴避
    提高迴避機率 => target = "self", 根據職業轉數而定
    # 提升暴擊
    精準攻擊 => target = "self", 根據職業轉數而定
    # 反擊
    反擊 => target = "self", 根據職業轉數而定
    # 護盾扛傷
    護盾 => target = "self", 根據職業轉數而定
負面:
    # 降低傷害
    虛弱 => target = "enemy"
    自我虛弱 => target = "self"
    # 減少防禦
    破甲 => target = "enemy", 根據職業轉數而定
    # 減少命中
    致盲 => target = "enemy", 根據職業轉數而定
    # 降低迴避
    緩速 => target = "enemy", 根據職業轉數而定
    # 無法行動
    麻痺、凍結、暈眩 => target = "enemy"
    # 回合傷害
    dot傷害 (凍傷、燒傷、出血、風蝕) => target = "enemy", 最大5層, 通過反覆命中提升等級, 隨著等級增加傷害倍率
    中毒 => target = "enemy", 最大3層, 通過反覆命中提升等級, 隨著等級增加固定比例扣血
    # 延遲爆發
    延遲爆發 => target = "enemy"
'''
# ==================
# DotEffect 抽象類別
# ==================

@dataclass
class DotEffect(ABC):
    name: str # 凍傷, 燒傷, 出血, 風蝕, 中毒
    effect_type: str # frostbite, burn, bleed, corrosion, poison
    basic_damage: float
    duration: int # 持續時間
    max_level: int
    
    @abstractmethod
    def calculate_damage(self, attacker, defender, level):
        pass

# ==================
# DotEffect 實作類別
# ==================

class FrostbiteEffect(DotEffect):
    def __init__(self, duration):
        super().__init__(name = "凍傷", 
                         effect_type = "forstbite", 
                         basic_damage = 0.1,
                         max_level = 5, 
                         duration = duration)
    
    def calculate_damage(self, player: PlayerAttribute, level) -> int:
        return self.basic_damage * (1 + player.MND * 0.2)




@dataclass
class Effect(ABC):
    name: str
    duration: int # 持續時間
    level: int # Buff等級


@dataclass
class JobAttribute(ABC):
    hp: int
    attack: int
    defense: int
    