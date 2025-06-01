from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import View
from pathlib import Path
from typing import List

import math
import yaml

from ..player.player import Player
from ..basebutton import BaseUserRestrictedButton

YAML_PATH = Path("yaml")
with open(YAML_PATH / "item_view.yaml", "r", encoding = "utf-8") as f:
    const = yaml.safe_load(f)

SLOT_MAPPING = const["SLOT_MAPPING"]

###############################
# EquipInventorySlotView class
###############################
class EquipInventorySlotView(View):
    def __init__(self, 
                 user: Member, 
                 player: Player,
                 slot_name: str,
                 embeds: List[Embed],
                 timeout: int = 60,
                 equipment_per_page: int = 2):
        
        super().__init__(timeout = timeout)
        self.user = user
        self.player = player
        self.equip_name = player.equipinventory.get_slot_equipment_name_list()
        self.embeds = embeds
        self.equipment_per_page = equipment_per_page
        
        self.current_page = 0
        self.total_page = math.ceil(len(self.equip_name) / equipment_per_page)
        self.index = 0
        
        # 基礎按鈕
        
        
        
        # 裝備按鈕
        
    def _build_equipment_buttons(self):
        ...
        
    
    def update_button_state(self):
        ...
        
    async def on_timeout(self):
        ...
        

#############################################
# EquipInventorySlotPreviousPageButton class
#############################################
class EquipInventorySlotPreviousPageButton(BaseUserRestrictedButton):
    def __init__(self, 
                 user: Member, 
                 label: str, 
                 slot_name: str):
        
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.slot_display_name = SLOT_MAPPING[slot_name]
    
    async def callback(self, interaction: Interaction):
        view: EquipInventorySlotView = self.view
        if not await self.check_user(interaction):
            return
        
        view.current_page -= 1
        view.index -= 2
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"系統提示：請選擇裝備",
            embed = view.embeds[view.current_page],
            view = view
        )
        return

#########################################
# EquipInventorySlotNextPageButton class
#########################################
class EquipInventorySlotNextPageButton(BaseUserRestrictedButton):
    def __init__(self, 
                 user: Member, 
                 label: str, 
                 slot_name: str):
        
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.slot_display_name = SLOT_MAPPING[slot_name]
    
    async def callback(self, interaction: Interaction):
        view: EquipInventorySlotView = self.view
        if not await self.check_user(interaction):
            return
        
        view.current_page += 1
        view.index += 2
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"系統提示：請選擇裝備",
            embed = view.embeds[view.current_page],
            view = view
        )
        return

############################################
# EquipInventorySelectEquipmentButton class
############################################
class EquipInventorySelectEquipmentButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, index: int):
        super().__init__(user = user, label = label, style = ButtonStyle.success)