from discord import Member, Interaction, ButtonStyle
from discord.ui import Button, View
from pathlib import Path

import yaml

from .player import Player
from .equipinventory_utils import create_slot_embed
from .equipinventory_slot_view import EquipSlotView
from ..basebutton import BaseUserRestrictedButton

YAML_PATH = Path("yaml")
with open(YAML_PATH / "item_view.yaml", "r", encoding = "utf-8") as f:
    const = yaml.safe_load(f)

SLOT_MAPPING = const["SLOT_MAPPING"]

###########################
# EquipInventoryView class
###########################
class EquipInventoryView(View):
    def __init__(self, user: Member, timeout:int = 30):
        super().__init__(timeout = timeout)
        self.user = user
        self.user_id = user.id
        
        self.add_item(EquipSlotButton(user = self.user, slot_name = "weapon"))
        self.add_item(EquipSlotButton(user = self.user, slot_name = "head"))
        self.add_item(EquipSlotButton(user = self.user, slot_name = "chest"))
        self.add_item(EquipSlotButton(user = self.user, slot_name = "leggings"))
        self.add_item(EquipSlotButton(user = self.user, slot_name = "feet"))
        self.add_item(EquipSlotButton(user = self.user, slot_name = "earring"))
        self.add_item(EquipSlotButton(user = self.user, slot_name = "necklace"))
        self.add_item(EquipSlotButton(user = self.user, slot_name = "bracelet"))
        self.add_item(EquipSlotButton(user = self.user, slot_name = "ring"))
        self.add_item(EquipSlotCancelButton(user = self.user, label = "關閉介面"))

########################
# EquipSlotButton class
########################
class EquipSlotButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, slot_name: str):
        super().__init__(user = user, label = SLOT_MAPPING[slot_name], style = ButtonStyle.primary)
        self.user_id = user.id
        self.slot_name = slot_name
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的介面喔！",
                                                    ephemeral = True)
            return
        
        player = Player.load(self.user_id)
        slot = player.equipinventory.get_slot(self.slot_name)
        embeds, equip_names = create_slot_embed(slot, self.slot_name)
        
        await interaction.response.edit_message(
            content = "系統提示：請選擇裝備",
            embed = embeds[0],
            view = EquipSlotView(embeds = embeds, 
                                 equip_names = equip_names, 
                                 user = self.user,
                                 slot_name = self.slot_name)
        )

##############################
# EquipSlotCancelButton class
##############################
class EquipSlotCancelButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 這不是你的介面喔", ephemeral = True)
            return
        
        await interaction.response.edit_message(content = "系統提示：已關閉", view = None)
    