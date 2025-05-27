from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import Button, View
from pathlib import Path
from typing import List

import yaml

from .player import Player

YAML_PATH = Path("yaml")
with open(YAML_PATH / "item_view.yaml", "r", encoding = "utf-8") as f:
    const = yaml.safe_load(f)

SLOT_MAPPING = const["SLOT_MAPPING"]

class EquipSlotView(View):
    def __init__(self, embeds: List[Embed], equip_names: List[str], user: Member, slot_name: str, timeout: int = 30):
        super().__init__(timeout = timeout)
        self.embeds = embeds
        self.equip_names = equip_names
        self.user = user
        self.current_page = 0
        self.total_pages = len(embeds)
        self.slot_name = slot_name
        self.index = 0
        
        self.prev_button = SlotPreviousPageButton(label = "⬅ 上一頁", user = user, slot_name = slot_name)
        self.equip_button1 = SelectEquipmentButton(label = equip_names[self.index], user = user, index = self.index)
        self.add_item(self.prev_button)
        self.add_item(self.equip_button1)
        # 只有在還有第2件裝備時才加按鈕
        if self.index + 1 < len(equip_names):
            self.equip_button2 = SelectEquipmentButton(label = equip_names[self.index + 1], user = user, index = self.index + 1)
            self.add_item(self.equip_button2)
        else:
            self.equip_button2 = None  # 安全保留屬性，但不加入 view
        self.next_button = SlotNextPageButton(label = "➡ 下一頁", user = user, slot_name = slot_name)
        self.add_item(self.next_button)
        
        self.update_button_state()
    
    def update_button_state(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.total_pages - 1
        self.equip_button1.label = self.equip_names[self.index]
        self.equip_button1.index = self.index
        self.equip_button1.disabled = self.equip_button1.index >= len(self.equip_names)
        if self.equip_button2:
            self.equip_button2.label = self.equip_names[self.index + 1]
            self.equip_button2.index = self.index + 1
            self.equip_button2.disabled = self.equip_button2.index >= len(self.equip_names)

class SlotPreviousPageButton(Button):
    def __init__(self, label: str, user: Member, slot_name: str):
        super().__init__(label = label, style = ButtonStyle.primary)
        self.user = user
        self.slot_name = slot_name
        
    async def callback(self, interaction: Interaction):
        view: EquipSlotView = self.view
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的介面喔！",
                                                    ephemeral = True)
            return
        
        view.current_page -= 1
        view.index -= 2
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"**{self.user.display_name}** 的{SLOT_MAPPING[self.slot_name]}裝備一覽：第 {view.current_page + 1} / {view.total_pages} 頁",
            embed = view.embeds[view.current_page],
            view = view
        )
    
class SlotNextPageButton(Button):
    def __init__(self, label: str, user: Member, slot_name: str):
        super().__init__(label = label, style = ButtonStyle.primary)
        self.user = user
        self.slot_name = slot_name
        
    async def callback(self, interaction: Interaction):
        view: EquipSlotView = self.view
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的介面喔！",
                                                    ephemeral = True)
            return
        
        view.current_page += 1
        view.index += 2
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"**{self.user.display_name}** 的{SLOT_MAPPING[self.slot_name]}裝備一覽：第 {view.current_page + 1} / {view.total_pages} 頁",
            embed = view.embeds[view.current_page],
            view = view
        )
        
class SelectEquipmentButton(Button):
    def __init__(self, label: str, user: Member, index: int):
        super().__init__(label = label, style = ButtonStyle.primary)
        self.index = index
        self.user = user
    
    async def callback(self, interaction: Interaction):
        view: EquipSlotView = self.view
        if interaction.user != self.user:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的介面喔！",
                                                    ephemeral = True)
            return
        
        await interaction.response.edit_message(
            ...
        )
        