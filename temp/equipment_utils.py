from discord import Member, Interaction, ButtonStyle, Embed

import yaml
from pathlib import Path

from ...player.player import Player
from .equipment import Equipment

YAML_PATH = Path("yaml")
with open(YAML_PATH / "item_view.yaml", "r", encoding = "utf-8") as f:
    const = yaml.safe_load(f)
RARITY_EMOJI = const["RARITY_EMOJI"]

def create_equipment_compare_embed(player: Player, slot_name: str, index: int) -> Embed:
    select_equipment = player.equipinventory.get_slot(slot_name = slot_name)[index]
    rarity = select_equipment.get_rarity()
    
    embed = Embed(title = "裝備介面", description = "即將裝備")
    equipment_lines = [
        f"【稀有度】{RARITY_EMOJI[rarity]} {rarity}",
        f"VIT： +{select_equipment.attribute_bonus['VIT']:>3}  WIS： +{select_equipment.attribute_bonus['WIS']:>3}",
        f"STR： +{select_equipment.attribute_bonus['STR']:>3}  INT： +{select_equipment.attribute_bonus['INT']:>3}",
        f"DEX： +{select_equipment.attribute_bonus['DEX']:>3}  AGI： +{select_equipment.attribute_bonus['AGI']:>3}",
        f"MND： +{select_equipment.attribute_bonus['MND']:>3}  LUK： +{select_equipment.attribute_bonus['LUK']:>3}"
    ]
    for i, socket in enumerate(select_equipment.sockets, start=1):
        if isinstance(socket, dict):
            attribute, value = next(iter(socket.items()))
            equipment_lines.append(f"潛能{i}: {attribute} +{value:>2}")
        elif isinstance(socket, bool):
            equipment_lines.append(f"潛能{i}: 未開啟")
    equipment_texts = "\n".join(equipment_lines)
    
    embed.add_field(
        name = select_equipment.get_display_name(),
        value = equipment_texts,
        inline = True
    )
    
    is_already_equipped = player.equipmentslot.is_already_equipped(slot_name = slot_name)
    if is_already_equipped:
        embed.description = "裝備比較"
        
        compare_equipment = player.equipmentslot.get_slot(slot_name = slot_name)
        
        rarity = compare_equipment.get_rarity()
        equipment_lines = [
            f"【稀有度】{RARITY_EMOJI[rarity]} {rarity}",
            f"VIT： +{compare_equipment.attribute_bonus['VIT']:>3}  WIS： +{compare_equipment.attribute_bonus['WIS']:>3}",
            f"STR： +{compare_equipment.attribute_bonus['STR']:>3}  INT： +{compare_equipment.attribute_bonus['INT']:>3}",
            f"DEX： +{compare_equipment.attribute_bonus['DEX']:>3}  AGI： +{compare_equipment.attribute_bonus['AGI']:>3}",
            f"MND： +{compare_equipment.attribute_bonus['MND']:>3}  LUK： +{compare_equipment.attribute_bonus['LUK']:>3}"
        ]
        for i, socket in enumerate(compare_equipment.sockets, start=1):
            if isinstance(socket, dict):
                attribute, value = next(iter(socket.items()))
                equipment_lines.append(f"潛能{i}: {attribute} +{value:>2}")
            elif isinstance(socket, bool):
                equipment_lines.append(f"潛能{i}: 未開啟")
        equipment_texts = "\n".join(equipment_lines)
        
        embed.add_field(
            name = compare_equipment.get_display_name(),
            value = equipment_texts,
            inline = True
        )
    
    return embed