from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import View
from pathlib import Path
from typing import List

import math
import yaml

from ..player.player import Player
from ..basebutton import BaseUserRestrictedButton
from ..item.equipment.equipment_utils import create_equipment_embed
from ..item.equipment.equipment_panel import EquipmentView

YAML_PATH = Path("yaml")
with open(YAML_PATH / "item_view.yaml", "r", encoding = "utf-8") as f:
    const = yaml.safe_load(f)

SLOT_MAPPING = const["SLOT_MAPPING"]

#########################
# EquipInventorySlotView
#########################
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
        self.slot_name = slot_name
        self.equip_names = player.equipinventory.get_slot_equipment_name_list(slot_name = slot_name)
        self.embeds = embeds
        self.equipment_per_page = equipment_per_page
        
        self.current_page = 0
        self.total_pages = math.ceil(len(self.equip_names) / equipment_per_page)
        self.index = 0
        self.message = None
        
        # 基礎按鈕
        self.prev_button = EquipInventorySlotPreviousPageButton(user = user, label = "⬅ 上一頁", slot_name = slot_name)
        self.next_button = EquipInventorySlotNextPageButton(user = user, label = "➡ 下一頁", slot_name = slot_name)
        self.cancel_button = CloseEquipInventorySlotViewButton(user = user, label = "關閉裝備背包欄位介面")
        self.back_button = EquipInventorySlotViewBackButton(user = user, label = "返回裝備背包介面")
        self.add_item(self.prev_button)    
        
        # 裝備按鈕 (動態)
        self.equip_buttons: List[EquipInventorySelectEquipmentButton] = []
        self._build_equipment_buttons()
        
        self.add_item(self.next_button)
        self.add_item(self.back_button)
        self.add_item(self.cancel_button)
        self.update_button_state()
        
    def _build_equipment_buttons(self):
        """根據當前的 index 動態產生按鈕
        """
        for i in range(self.equipment_per_page):
            idx = self.index + i
            if idx < len(self.equip_names):
                button = EquipInventorySelectEquipmentButton(user = self.user,
                                                             label = self.equip_names[idx],
                                                             index = idx)
                self.equip_buttons.append(button)
                self.add_item(button)
        #return
    
    def update_button_state(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.total_pages - 1

        for i, button in enumerate(self.equip_buttons):
            idx = self.index + i
            if idx < len(self.equip_names):
                button.label = self.equip_names[idx]
                button.index = idx
                button.disabled = False
            else:
                button.label = "-"
                button.disabled = True
        return
        
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉裝備背包欄位介面。",
                embed = None,
                view = None
            )
        return
        

#######################################
# EquipInventorySlotPreviousPageButton
#######################################
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

###################################
# EquipInventorySlotNextPageButton
###################################
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

######################################
# EquipInventorySelectEquipmentButton
######################################
class EquipInventorySelectEquipmentButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, index: int):
        super().__init__(user = user, label = label, style = ButtonStyle.success)
        self.index = index
    
    async def callback(self, interaction: Interaction):
        view: EquipInventorySlotView = self.view
        if not await self.check_user(interaction):
            return
        
        select_equipment = view.player.equipinventory.get_equipment(slot_name = view.slot_name,
                                                                    index = self.index)
        
        embed = create_equipment_embed(select_equipment)
        
        new_view = EquipmentView(user = view.user,
                                 player = view.player,
                                 slot_name = view.slot_name,
                                 index = self.index,
                                 embed = embed)
        await interaction.response.edit_message(
            content = "測試",
            embed = embed,
            view = new_view
        )
        view.message = await interaction.original_response()
        return

####################################
# CloseEquipInventorySlotViewButton
####################################
class CloseEquipInventorySlotViewButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        await interaction.response.edit_message(content = "系統提示：已關閉介面", 
                                                embed = None, 
                                                view = None)

###################################
# EquipInventorySlotViewBackButton
###################################
class EquipInventorySlotViewBackButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        from .equipinventory_panel import EquipInventoryView
        
        if not await self.check_user(interaction):
            return
        
        view = EquipInventoryView(user = self.user)
        await interaction.response.edit_message(content = "系統提示：請選擇裝備欄位",
                                                embed = None,
                                                view = view)
