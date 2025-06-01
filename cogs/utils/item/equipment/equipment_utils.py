from pathlib import Path
from discord import Embed, Color
from typing import List
from typing import Dict

import yaml

from ...player.player import Player
from ...equipinventory.equipinventory import EquipInventory
from .equipment import Equipment

###########
# CONSTANT
###########
YAML_PATH = Path("yaml")
with open(YAML_PATH / "item_view.yaml", "r", encoding = "utf-8") as f:
    const = yaml.safe_load(f)

RARITY_EMOJI = const["RARITY_EMOJI"]
FIGURE_PATH = "https://raw.githubusercontent.com/kuanchiun/discord_development/main/figures/{rarity}/{figure_id}.png"



def create_equipment_embed(equipment: Equipment) -> Embed:
    display_name = equipment.get_display_name()
    rarity = equipment.get_rarity()
    sell_money = equipment.get_sell_money()
    figure_id = equipment.get_figure_id()
    success_level = equipment.success_level
    scroll_number = equipment.scroll_number
    
    embed = Embed(
        title = f"**{display_name} (+{success_level})**",
        description = f"【稀有度】{rarity}",
    )
    
    attr_lines = [
        f"VIT： +{equipment.attribute_bonus['VIT']:>3}  WIS： +{equipment.attribute_bonus['WIS']:>3}",
        f"STR： +{equipment.attribute_bonus['STR']:>3}  INT： +{equipment.attribute_bonus['INT']:>3}",
        f"DEX： +{equipment.attribute_bonus['DEX']:>3}  AGI： +{equipment.attribute_bonus['AGI']:>3}",
        f"MND： +{equipment.attribute_bonus['MND']:>3}  LUK： +{equipment.attribute_bonus['LUK']:>3}"
    ]
    potential_lines = []
    for i, socket in enumerate(equipment.sockets, start = 1):
        if isinstance(socket, Dict):
            attribute, value = next(iter(socket.items()))
            potential_lines.append(f"潛能{i}: {attribute} +{value:>2}")
        elif isinstance(socket, bool):
            potential_lines.append(f"潛能{i}: 未開啟")

    attr_texts = "```\n" + "\n".join(attr_lines) + "\n```"
    embed.add_field(
        name = "【裝備屬性】",
        value = attr_texts,
        inline = False
    )
    
    if len(potential_lines) > 0:
        potential_texts = "```\n" + "\n".join(potential_lines) + "\n```"
        embed.add_field(
            name = "【潛能屬性】",
            value = potential_texts,
            inline = False
        )
    
    embed.add_field(
        name = "【剩餘強化次數】",
        value = f"```\n{scroll_number}次\n```",
        inline = False
    )
    
    embed.set_thumbnail(url = FIGURE_PATH.format(rarity = rarity, figure_id = figure_id))
    embed.set_footer(text = f"出售金額：💎{sell_money}")
    
    return embed
    
    