from pathlib import Path
from discord import Embed, Color
from typing import List
from typing import Dict

import yaml

from ..player.player import Player
from .equipinventory import EquipInventory
from ..item.equipment.equipment import Equipment

###########
# CONSTANT
###########
YAML_PATH = Path("yaml")
with open(YAML_PATH / "item_view.yaml", "r", encoding = "utf-8") as f:
    const = yaml.safe_load(f)

SLOT_MAPPING = const["SLOT_MAPPING"]
RARITY_EMOJI = const["RARITY_EMOJI"]


def create_equip_inventory_slot_embed(slot: List[Equipment], label: str) -> Embed:
    embeds = []
    
    for page in range(0, len(slot), 2):
        embed = Embed(
            title = f"{label}的裝備一覽",
            description = f"顯示第 {page // 2 + 1}頁 / 共 {len(slot) // 2} 頁",
            color = Color.blue()
        )
        
        for index, equipment in enumerate(slot[page:page+2], start = 1):
            display_name = equipment.get_display_name()
            rarity = equipment.get_rarity()
            success_level = equipment.success_level
            scroll_number = equipment.scroll_number
            
            attr_lines = [
                f"【稀有度】{rarity}",
                f"VIT： +{equipment.attribute_bonus['VIT']:>3}  WIS： +{equipment.attribute_bonus['WIS']:>3}",
                f"STR： +{equipment.attribute_bonus['STR']:>3}  INT： +{equipment.attribute_bonus['INT']:>3}",
                f"DEX： +{equipment.attribute_bonus['DEX']:>3}  AGI： +{equipment.attribute_bonus['AGI']:>3}",
                f"MND： +{equipment.attribute_bonus['MND']:>3}  LUK： +{equipment.attribute_bonus['LUK']:>3}"
            ]
            for i, socket in enumerate(equipment.sockets, start = 1):
                if isinstance(socket, Dict):
                    attribute, value = next(iter(socket.items()))
                    attr_lines.append(f"潛能{i}: {attribute} +{value:>2}")
                elif isinstance(socket, bool):
                    attr_lines.append(f"潛能{i}: 未開啟")
            attr_lines.append(f"剩餘強化次數：{scroll_number}")
            
            attr_texts = "```\n" + "\n".join(attr_lines) + "\n```"
            
            embed.add_field(
                name = f"裝備{index + page}. **{display_name}(+{success_level})**",
                value = attr_texts,
                inline = True
            )
        
        embeds.append(embed)
    
    return embeds
                    