from typing import Dict, List, Union
from collections import defaultdict
from random import choice, choices
from pathlib import Path
from discord import Member
from dataclasses import dataclass, field

import yaml

"""
┌───────────┬──────────────────────────────────────┐
│ Attribute │           Effect on Player           │
├───────────┼──────────────────────────────────────┤
│    VIT    │         HP, Physical Defense         │
├───────────┼──────────────────────────────────────┤
│    WIS    │         MP, Magical Defense          │
├───────────┼──────────────────────────────────────┤
│    STR    │  Physical Attack, Physical Hit Rate  │
├───────────┼──────────────────────────────────────┤
│    INT    │   Magical Attack, Magical Hit Rate   │
├───────────┼──────────────────────────────────────┤
│    DEX    │     Action Speed, Turn Priority      │
├───────────┼──────────────────────────────────────┤
│    AGI    │  Evasion Rate, High-tier Skill Bias  │
├───────────┼──────────────────────────────────────┤
│    MND    │    DOT Damage, Control Resistance    │
├───────────┼──────────────────────────────────────┤
│    LUK    │ Critical Rate, Critical Damage Bonus │
└───────────┴──────────────────────────────────────┘
"""

######################
# BaseAttribute class
######################
@dataclass
class BaseAttribute:
    VIT: int = 0
    WIS: int = 0
    STR: int = 0
    INT: int = 0
    DEX: int = 0
    AGI: int = 0
    MND: int = 0
    LUK: int = 0
    remind_point: int = 50
    
    def to_dict(self) -> Dict:
        """轉換成字典

        Returns
        -------
        Dict:
           基礎屬性字典
        """
        
        return {
            "VIT": self.VIT,
            "WIS": self.WIS,
            "STR": self.STR,
            "INT": self.INT,
            "DEX": self.DEX,
            "AGI": self.AGI,
            "MND": self.MND,
            "LUK": self.LUK,
            "remind_point": self.remind_point
        }
    
    @classmethod
    def from_dict(cls, data) -> "BaseAttribute":
        """將字典轉換為基礎屬性物件

        Parameters
        ----------
        data : dict
            基礎屬性字典

        Returns
        -------
        Equipment
            基礎屬性物件
        """
        
        return cls(
            VIT = data.get("VIT", 0),
            WIS = data.get("WIS", 0),
            STR = data.get("STR", 0),
            INT = data.get("INT", 0),
            DEX = data.get("DEX", 0),
            AGI = data.get("AGI", 0),
            MND = data.get("MND", 0),
            LUK = data.get("LUK", 0),
            remind_point = data.get("remind_point", 0)
        )