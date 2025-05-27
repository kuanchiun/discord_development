from collections import Counter
from typing import List, Dict, Tuple
from discord import Embed, Color
from pathlib import Path

import yaml

from ..item.base_item import BaseItem
from ..item.equipment import Equipment
from ..item.scroll import Scroll
from ..item.prototype import Prototype

YAML_PATH = Path("yaml")
with open(YAML_PATH / "item_view.yaml", "r", encoding = "utf-8") as f:
    const = yaml.safe_load(f)

SLOT_MAPPING = const["SLOT_MAPPING"]
ITEM_TYPE_MAPPING = const["ITEM_TYPE_MAPPING"]
RARITY_EMOJI = const["RARITY_EMOJI"]
FIGURE_PATH = "https://raw.githubusercontent.com/kuanchiun/discord_development/main/figures/{rarity}/{figure_id}.png"
GIF_PATH = "https://raw.githubusercontent.com/kuanchiun/discord_development/main/figures/{rarity}.gif"

def create_single_draw_effect_embed(rarity):
    gif_path = GIF_PATH.format(rarity = rarity)
    embed = Embed(title = None)
    embed.set_image(url=gif_path)

    return embed
    
def create_multi_draw_effect_embed(rarity_count):
    for rarity in ["UR", "SR", "R", "N"]:
        if rarity_count[rarity] > 0:
            gif_path = GIF_PATH.format(rarity = rarity)
            embed = Embed(title = None)
            embed.set_image(url=gif_path)

            return embed
    
def summarize_rarity(loots: List[BaseItem]) -> str:
    counter = Counter(loot.get_rarity() for loot in loots)
    texts = "📊 稀有度統計： "
    for rarity in ["UR", "SR", "R", "N"]:
        texts += f"{RARITY_EMOJI[rarity]}  {rarity}: {counter[rarity]}"
        if rarity != "N":
            texts += " | "
    
    return texts

def create_single_draw_embed(loot: BaseItem) -> Embed:
    rarity = loot.get_rarity()
    item_type = loot.get_item_type()
    figure_id = loot.get_figure_id()
    
    embed = Embed(
        title = f"{RARITY_EMOJI[rarity]} {loot.get_display_name()}",
        description = loot.get_description(),
        color = Color.gold()
    )
    
    embed.add_field(name = "【稀有度】", value = rarity, inline = True)
    embed.add_field(name = "【物品類型】", value = ITEM_TYPE_MAPPING[item_type], inline = True)
    
    if isinstance(loot, Equipment):
        attr_lines = [
            f"【裝備部位】：{SLOT_MAPPING[loot.slot]}",
            f"VIT： +{loot.attribute_bonus['VIT']:>3}  WIS： +{loot.attribute_bonus['WIS']:>3}",
            f"STR： +{loot.attribute_bonus['STR']:>3}  INT： +{loot.attribute_bonus['INT']:>3}",
            f"DEX： +{loot.attribute_bonus['DEX']:>3}  AGI： +{loot.attribute_bonus['AGI']:>3}",
            f"MND： +{loot.attribute_bonus['MND']:>3}  LUK： +{loot.attribute_bonus['LUK']:>3}",
        ]
        for i, socket in enumerate(loot.sockets, start=1):
            if socket is None:
                attr_lines.append(f"潛能{i}: 未開啟")
        
        attr_texts = "```\n" + "\n".join(attr_lines) + "\n```"
        
        embed.add_field(
            name = "【裝備屬性】",
            value = attr_texts,
            inline = False
        )
    
    embed.set_thumbnail(url = FIGURE_PATH.format(rarity = rarity, figure_id = figure_id))
    
    return embed

def create_multi_draw_embeds(loots: List[BaseItem]) -> Tuple[Dict[str, int], List[Embed], List[Embed]]:
    embeds = []
    single_embeds = []
    rarity_count = summarize_rarity(loots)
    
    for page in range(0, len(loots), 5):
        embed = Embed(
            title = "十連抽結果",
            description = f"顯示第 {page // 5 + 1}頁 / 共 {len(loots) // 5} 頁",
            color = Color.gold()
        )
        
        for index, loot in enumerate(loots[page:page + 5], start = 1):
            display_name = loot.get_display_name()
            rarity = loot.get_rarity()
            item_type = loot.get_item_type()
            description = loot.get_description()
            
            if isinstance(loot, Equipment):
                slot = loot.slot
                embed.add_field(
                    name = f"{RARITY_EMOJI[rarity]}  {page + index}. {display_name}",
                    value = (
                        f"> **稀有度：** {rarity}\n" + 
                        f"> **類型：** {ITEM_TYPE_MAPPING[item_type]}\n" + 
                        f"> **裝備部位：** {SLOT_MAPPING[slot]}"
                    ),
                    inline = False
                )
            else:
                embed.add_field(
                    name = f"{RARITY_EMOJI[rarity]}  {page + index}. {display_name}",
                    value = (
                        f"> **稀有度：** {rarity}\n" + 
                        f"> **類型：** {ITEM_TYPE_MAPPING[item_type]}\n" + 
                        f"> **說明：** {description}"
                    ),
                    inline = False
                )
        
        embed.set_footer(text = rarity_count)
        
        embeds.append(embed)
    
    for loot in loots:
        single_embeds.append(create_single_draw_embed(loot))
    
    return rarity_count, embeds, single_embeds
