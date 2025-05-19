from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from dataclasses import dataclass

BASIC_HEALTH = 100
BASIC_PHYSICAL_ATTACK = (3, 15)
BASIC_MAGIC_ATTACK = (3, 15)
BASIC_DEFENSE = 5
BASIC_CRITICAL_RATE = 0.10
BASIC_HIT = 10
BASIC_SIDESTEP = 10
BASIC_SPEED = 100

@dataclass
class JobAttribute(ABC):
    hp_per_level: int
    
    physical_attack_min_per_level: int
    physical_attack_max_per_level: int
    magic_attack_min_per_level: int
    magic_attack_max_per_level: int
    
    defense_per_level: int
    
    hit_per_level: int = 5
    sidestep_per_level: int = 5

    @abstractmethod
    def calculate_hp(self, level: int, VIT: int) -> int:
        pass
    
    @abstractmethod
    def calculate_physical_attack(self, level: int, STR: int) -> int:
        pass
    
    @abstractmethod
    def calculate_magic_attack(self, level: int, INT: int) -> int:
        pass
    
    @abstractmethod
    def calculate_defense(self, level: int, VIT: int) -> int:
        pass
    
    def calculate_critical_rate(self, LUK: int) -> float:
        return round(BASIC_CRITICAL_RATE * (1 + LUK * 0.025), 2)
    
    def calculate_hit(self, level: int, MND: int) -> int:
        return round((BASIC_HIT + (level - 1) * self.hit_per_level) * (1 + MND * 0.005))
    
    def calculate_sidestep(self, level: int, DEX: int) -> int:
        return round((BASIC_SIDESTEP + (level - 1) * self.sidestep_per_level) * (1 + DEX * 0.005))
    
    def calculate_speed(self, DEX: int) -> int:
        return round(BASIC_SPEED * (1 + min(DEX, 150) * 0.01 + max(0, DEX - 150) * 0.002))
        
class StarterJobAttribute(JobAttribute):
    def __init__(self):
        super().__init__(hp_per_level = 15,
                         physical_attack_min_per_level = 2, 
                         physical_attack_max_per_level = 3,
                         magic_attack_min_per_level = 2, 
                         magic_attack_max_per_level = 3,
                         defense_per_level = 2)
        
    def calculate_hp(self, level: int, VIT: int) -> int:
        return round((BASIC_HEALTH + (level - 1) * self.hp_per_level) * (1 + VIT * 0.005))
    
    def calculate_defense(self, level: int, VIT: int) -> int:
        return round((BASIC_DEFENSE + (level - 1) * self.defense_per_level) * (1 + VIT * 0.005))
    
    def calculate_physical_attack(self, level: int, STR: int, LUK: int) -> int:
        min_physical_attack, max_physical_attack = BASIC_PHYSICAL_ATTACK
        
        level_min_add = (level - 1) * self.physical_attack_min_per_level
        level_max_add = (level - 1) * self.physical_attack_max_per_level
        
        # max
        max_physical_attack += level_max_add
        max_physical_attack = round(max_physical_attack * (1 + STR * 0.005))
        # min
        min_physical_attack += level_min_add
        min_physical_attack = min_physical_attack * (1 + STR * 0.0025)
        min_physical_attack = round(min(min_physical_attack * (1 + 0.005 * LUK), max_physical_attack))
        

        return min_physical_attack, max_physical_attack
    
    def calculate_magic_attack(self, level, INT, LUK):
        min_magic_attack, max_magic_attack = BASIC_MAGIC_ATTACK
        
        level_min_add = (level - 1) * self.magic_attack_min_per_level
        level_max_add = (level - 1) * self.magic_attack_max_per_level
        
        # max
        max_magic_attack += level_max_add
        max_magic_attack = round(max_magic_attack * (1 + INT * 0.005))
        # min
        min_magic_attack += level_min_add
        min_magic_attack = min_magic_attack * (1 + INT * 0.0025)
        min_magic_attack = round(min(min_magic_attack * (1 + 0.005 * LUK), max_magic_attack))
        
        
        return min_magic_attack, max_magic_attack
    

class SwordJobAttribute(JobAttribute):
    def __init__(self):
        super().__init__(hp_per_level = 45,
                         physical_attack_min_per_level = 2, 
                         physical_attack_max_per_level = 3,
                         magic_attack_min_per_level = 2, 
                         magic_attack_max_per_level = 3,
                         defense_per_level = 5)
    
    def calculate_hp(self, level: int, VIT: int) -> int:
        return round((BASIC_HEALTH + (level - 1) * self.hp_per_level) * (1 + VIT * 0.01))
    
    def calculate_defense(self, level: int, VIT: int) -> int:
        return round((BASIC_DEFENSE + (level - 1) * self.defense_per_level) * (1 + VIT * 0.005))
    
    def calculate_physical_attack(self, level: int, STR: int, LUK: int) -> int:
        min_physical_attack, max_physical_attack = BASIC_PHYSICAL_ATTACK
        
        level_min_add = (level - 1) * self.physical_attack_min_per_level
        level_max_add = (level - 1) * self.physical_attack_max_per_level
        
        # max
        max_physical_attack += level_max_add
        max_physical_attack = round(max_physical_attack * (1 + STR * 0.005))
        # min
        min_physical_attack += level_min_add
        min_physical_attack = min_physical_attack * (1 + STR * 0.0025)
        min_physical_attack = round(min(min_physical_attack * (1 + 0.005 * LUK), max_physical_attack))
        

        return min_physical_attack, max_physical_attack
    
    def calculate_magic_attack(self, level, INT, LUK):
        min_magic_attack, max_magic_attack = BASIC_MAGIC_ATTACK
        
        level_min_add = (level - 1) * self.magic_attack_min_per_level
        level_max_add = (level - 1) * self.magic_attack_max_per_level
        
        # max
        max_magic_attack += level_max_add
        max_magic_attack = round(max_magic_attack * (1 + INT * 0.005))
        # min
        min_magic_attack += level_min_add
        min_magic_attack = min_magic_attack * (1 + INT * 0.0025)
        min_magic_attack = round(min(min_magic_attack * (1 + 0.005 * LUK), max_magic_attack))
        
        
        return min_magic_attack, max_magic_attack
    
    

class ShooterJobAttribute(JobAttribute):
    def __init__(self):
        super().__init__(hp_per_level = 35,
                         physical_attack_min_per_level = 3, 
                         physical_attack_max_per_level = 5,
                         magic_attack_min_per_level = 1, 
                         magic_attack_max_per_level = 2,
                         defense_per_level = 4)
        
    def calculate_hp(self, level: int, VIT: int) -> int:
        return round((BASIC_HEALTH + (level - 1) * self.hp_per_level) * (1 + VIT * 0.005))
    
    def calculate_defense(self, level: int, VIT: int) -> int:
        return round((BASIC_DEFENSE + (level - 1) * self.defense_per_level) * (1 + VIT * 0.003))
    
    def calculate_physical_attack(self, level: int, STR: int, LUK: int) -> int:
        min_physical_attack, max_physical_attack = BASIC_PHYSICAL_ATTACK
        
        level_min_add = (level - 1) * self.physical_attack_min_per_level
        level_max_add = (level - 1) * self.physical_attack_max_per_level
        
        # max
        max_physical_attack += level_max_add
        max_physical_attack = round(max_physical_attack * (1 + STR * 0.005))
        # min
        min_physical_attack += level_min_add
        min_physical_attack = min_physical_attack * (1 + STR * 0.0025)
        min_physical_attack = round(min(min_physical_attack * (1 + 0.005 * LUK), max_physical_attack))
        

        return min_physical_attack, max_physical_attack
    
    def calculate_magic_attack(self, level, INT, LUK):
        min_magic_attack, max_magic_attack = BASIC_MAGIC_ATTACK
        
        level_min_add = (level - 1) * self.magic_attack_min_per_level
        level_max_add = (level - 1) * self.magic_attack_max_per_level
        
        # max
        max_magic_attack += level_max_add
        max_magic_attack = round(max_magic_attack * (1 + INT * 0.005))
        # min
        min_magic_attack += level_min_add
        min_magic_attack = min_magic_attack * (1 + INT * 0.0025)
        min_magic_attack = round(min(min_magic_attack * (1 + 0.005 * LUK), max_magic_attack))
        
        
        return min_magic_attack, max_magic_attack
    
class MageJobAttribute(JobAttribute):
    def __init__(self):
        super().__init__(hp_per_level = 30,
                         physical_attack_min_per_level = 1, 
                         physical_attack_max_per_level = 2,
                         magic_attack_min_per_level = 4, 
                         magic_attack_max_per_level = 6,
                         defense_per_level = 3)
        
    def calculate_hp(self, level: int, VIT: int) -> int:
        return round((BASIC_HEALTH + (level - 1) * self.hp_per_level) * (1 + VIT * 0.005))
    
    def calculate_defense(self, level: int, VIT: int) -> int:
        return round((BASIC_DEFENSE + (level - 1) * self.defense_per_level) * (1 + VIT * 0.003))
    
    def calculate_physical_attack(self, level: int, STR: int, LUK: int) -> int:
        min_physical_attack, max_physical_attack = BASIC_PHYSICAL_ATTACK
        
        level_min_add = (level - 1) * self.physical_attack_min_per_level
        level_max_add = (level - 1) * self.physical_attack_max_per_level
        
        # max
        max_physical_attack += level_max_add
        max_physical_attack = round(max_physical_attack * (1 + STR * 0.005))
        # min
        min_physical_attack += level_min_add
        min_physical_attack = min_physical_attack * (1 + STR * 0.0025)
        min_physical_attack = round(min(min_physical_attack * (1 + 0.005 * LUK), max_physical_attack))
        

        return min_physical_attack, max_physical_attack
    
    def calculate_magic_attack(self, level, INT, LUK):
        min_magic_attack, max_magic_attack = BASIC_MAGIC_ATTACK
        
        level_min_add = (level - 1) * self.magic_attack_min_per_level
        level_max_add = (level - 1) * self.magic_attack_max_per_level
        
        # max
        max_magic_attack += level_max_add
        max_magic_attack = round(max_magic_attack * (1 + INT * 0.005))
        # min
        min_magic_attack += level_min_add
        min_magic_attack = min_magic_attack * (1 + INT * 0.0025)
        min_magic_attack = round(min(min_magic_attack * (1 + 0.005 * LUK), max_magic_attack))
        
        
        return min_magic_attack, max_magic_attack

class ThiefJobAttribute(JobAttribute):
    def __init__(self):
        super().__init__(hp_per_level = 30,
                         physical_attack_min_per_level = 4, 
                         physical_attack_max_per_level = 6,
                         magic_attack_min_per_level = 1, 
                         magic_attack_max_per_level = 2,
                         defense_per_level = 3)
        
    def calculate_hp(self, level: int, VIT: int) -> int:
        return round((BASIC_HEALTH + (level - 1) * self.hp_per_level) * (1 + VIT * 0.005))
    
    def calculate_defense(self, level: int, VIT: int) -> int:
        return round((BASIC_DEFENSE + (level - 1) * self.defense_per_level) * (1 + VIT * 0.005))
    
    def calculate_physical_attack(self, level: int, STR: int, LUK: int) -> int:
        min_physical_attack, max_physical_attack = BASIC_PHYSICAL_ATTACK
        
        level_min_add = (level - 1) * self.physical_attack_min_per_level
        level_max_add = (level - 1) * self.physical_attack_max_per_level
        
        # max
        max_physical_attack += level_max_add
        max_physical_attack = round(max_physical_attack * (1 + STR * 0.005))
        # min
        min_physical_attack += level_min_add
        min_physical_attack = min_physical_attack * (1 + STR * 0.0025)
        min_physical_attack = round(min(min_physical_attack * (1 + 0.005 * LUK), max_physical_attack))
        

        return min_physical_attack, max_physical_attack
    
    def calculate_magic_attack(self, level, INT, LUK):
        min_magic_attack, max_magic_attack = BASIC_MAGIC_ATTACK
        
        level_min_add = (level - 1) * self.magic_attack_min_per_level
        level_max_add = (level - 1) * self.magic_attack_max_per_level
        
        # max
        max_magic_attack += level_max_add
        max_magic_attack = round(max_magic_attack * (1 + INT * 0.005))
        # min
        min_magic_attack += level_min_add
        min_magic_attack = min_magic_attack * (1 + INT * 0.0025)
        min_magic_attack = round(min(min_magic_attack * (1 + 0.005 * LUK), max_magic_attack))
        
        
        return min_magic_attack, max_magic_attack


JOB_MAP = {
    "starter": StarterJobAttribute(),
    "sword": SwordJobAttribute(),
    "shooter": ShooterJobAttribute(),
    "mage": MageJobAttribute(),
    "thief": ThiefJobAttribute()
}