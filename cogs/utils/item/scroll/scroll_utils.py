from pathlib import Path
from discord import Embed, Color
from typing import List
from typing import Dict

import yaml

from ...iteminventory.iteminventory import InventoryEntry

###########
# CONSTANT
###########
YAML_PATH = Path("yaml")
with open(YAML_PATH / "item_view.yaml", "r", encoding = "utf-8") as f:
    const = yaml.safe_load(f)

RARITY_EMOJI = const["RARITY_EMOJI"]

def create_scroll_embed(scrolls: List[Dict[str, InventoryEntry]]) -> List[Embed]:
    embeds = []
    
    for page in range(0, len(scrolls), 5):
        embed = Embed(
            title = f"持有的卷軸一覽",
            description = f"顯示第 {page // 5 + 1}頁 / 共 {len(scrolls) // 5} 頁",
            color = Color.blue()
        )
        
        for index, scroll in enumerate(scrolls[page:page+5], start = 1):
            for id, scroll_info in scroll.items():
                display_name = scroll_info.item.get_display_name()
                rarity = scroll_info.item.get_rarity()
                description = scroll_info.item.get_description()
                number = scroll_info.quantity
                
                lines = [
                    f"【稀有度 {RARITY_EMOJI[rarity]} {rarity}",
                    f"【說明】{description}",
                    f"【持有數量】{number}",
                ]
                
                texts = "```\n" + "\n".join(lines) + "\n```"
                
                embed.add_field(
                    name = f"卷軸{index + page}. **{display_name}**",
                    value = texts,
                    inline = False
                )
                
                embeds.append(embed)
    
    return embeds