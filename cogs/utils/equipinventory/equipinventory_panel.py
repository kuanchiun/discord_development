from discord import Member, Interaction, ButtonStyle
from discord.ui import View
from pathlib import Path

import yaml

from ..player.player import Player
from ..basebutton import BaseUserRestrictedButton
from .equipinventory_utils import create_equip_inventory_slot_embed


###########
# CONSTANT
###########
YAML_PATH = Path("yaml")
with open(YAML_PATH / "item_view.yaml", "r", encoding = "utf-8") as f:
    const = yaml.safe_load(f)

SLOT_MAPPING = const["SLOT_MAPPING"]

###########################
# EquipInventoryView class
###########################
class EquipInventoryView(View):
    def __init__(self, user: Member, timeout: int = 30):
        super().__init__(timeout = timeout)
        self.user = user
        self.user_id = user
        self.player = Player.load(user.id)
        self.message = None
        
        self.add_item(EquipInventorySlotButton(user = user, slot_name = "weapon"))
        self.add_item(EquipInventorySlotButton(user = user, slot_name = "head"))
        self.add_item(EquipInventorySlotButton(user = user, slot_name = "chest"))
        self.add_item(EquipInventorySlotButton(user = user, slot_name = "leggings"))
        self.add_item(EquipInventorySlotButton(user = user, slot_name = "feet"))
        self.add_item(EquipInventorySlotButton(user = user, slot_name = "earring"))
        self.add_item(EquipInventorySlotButton(user = user, slot_name = "necklace"))
        self.add_item(EquipInventorySlotButton(user = user, slot_name = "bracelet"))
        self.add_item(EquipInventorySlotButton(user = user, slot_name = "ring"))
        
        self.add_item(CloseEquipInventoryButton(user = user, label = "關閉介面"))
    
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉裝備背包介面",
                embed = None,
                view = None
            )
        return

########################
# EquipSlotButton class
########################
class EquipInventorySlotButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, slot_name: str):
        super().__init__(user = user, label = SLOT_MAPPING[slot_name], style = ButtonStyle.primary)
        self.slot_name = slot_name
        
    async def callback(self, interaction: Interaction):
        view: EquipInventoryView = self.view
        if not await self.check_user(interaction):
            return
        
        slot = view.player.equipinventory.get_slot(self.slot_name)
        
        if len(slot) == 0:
            await interaction.response.edit_message(
                content = f"系統提示：你的**{self.label}**欄位沒有裝備，請重新選擇欄位",
                view = view,
                embed = None
            )
            return
        
        embeds = create_equip_inventory_slot_embed(slot, self.label)
        
        await interaction.response.edit_message(
            content = "系統提示：請選擇裝備",
            embed = embeds[0]
        )
        return
        
##################################
# CloseEquipInventoryButton class
##################################
class CloseEquipInventoryButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        await interaction.response.edit_message(
            content = "系統提示：已關閉裝備背包介面",
            view = None
        )
        
        return