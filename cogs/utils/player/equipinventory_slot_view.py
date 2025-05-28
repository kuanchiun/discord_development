from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import Button, View
from pathlib import Path
from typing import List

import math
import yaml

from .player import Player
from ..basebutton import BaseUserRestrictedButton

YAML_PATH = Path("yaml")
with open(YAML_PATH / "item_view.yaml", "r", encoding = "utf-8") as f:
    const = yaml.safe_load(f)

SLOT_MAPPING = const["SLOT_MAPPING"]

######################
# EquipSlotView class
######################
class EquipSlotView(View):
    def __init__(self, embeds: List[Embed], equip_names: List[str], user: Member, slot_name: str, timeout: int = 30, items_per_page: int = 2):
        super().__init__(timeout=timeout)
        self.embeds = embeds
        self.equip_names = equip_names
        self.user = user
        self.slot_name = slot_name
        self.items_per_page = items_per_page

        self.current_page = 0
        self.total_pages = math.ceil(len(equip_names) / items_per_page)
        self.index = 0  # 第一頁的起始 index

        # 分頁按鈕
        self.prev_button = SlotPreviousPageButton(user = user, label = "⬅ 上一頁", slot_name = slot_name)
        self.next_button = SlotNextPageButton(user = user, label = "➡ 下一頁", slot_name = slot_name)
        self.cancel_button = EquipSlotViewCancelButton(user = user, label = "關閉介面")
        self.add_item(self.prev_button)

        # 動態裝備按鈕們（初始化）
        self.equip_buttons: List[SelectEquipmentButton] = []
        self._build_equipment_buttons()

        self.add_item(self.next_button)
        self.add_item(self.cancel_button)
        self.update_button_state()

    def _build_equipment_buttons(self):
        """根據當前 index 動態產生裝備按鈕"""
        for i in range(self.items_per_page):
            idx = self.index + i
            if idx < len(self.equip_names):
                button = SelectEquipmentButton(label = self.equip_names[idx], user = self.user, index = idx)
                self.equip_buttons.append(button)
                self.add_item(button)

    def update_button_state(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.total_pages - 1

        for i, btn in enumerate(self.equip_buttons):
            idx = self.index + i
            if idx < len(self.equip_names):
                btn.label = self.equip_names[idx]
                btn.index = idx
                btn.disabled = False
            else:
                btn.label = "-"
                btn.disabled = True

###############################
# SlotPreviousPageButton class
###############################
class SlotPreviousPageButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, slot_name: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.slot_display_name = SLOT_MAPPING[slot_name]
        
    async def callback(self, interaction: Interaction):
        view: EquipSlotView = self.view
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
    
###########################
# SlotNextPageButton class
###########################
class SlotNextPageButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, slot_name: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.slot_display_name = SLOT_MAPPING[slot_name]
        
    async def callback(self, interaction: Interaction):
        view: EquipSlotView = self.view
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

##############################
# SelectEquipmentButton class
##############################
class SelectEquipmentButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, index: int):
        super().__init__(user = user, label = label, style = ButtonStyle.success)
        self.index = index
    
    async def callback(self, interaction: Interaction):
        view: EquipSlotView = self.view
        if not await self.check_user(interaction):
            return
        
        await interaction.response.edit_message(
            ...
        )

##################################
# EquipSlotViewCancelButton class
################################## 
class EquipSlotViewCancelButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        await interaction.response.edit_message(content = "系統提示：已關閉", embed = None, view = None)