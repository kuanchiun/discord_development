from discord import Member, Interaction, ButtonStyle, Color, Embed
from discord.ui import View
from typing import List

import math

from ...player.player import Player
from ...basebutton import BaseUserRestrictedButton
from ..equipment.equipment_utils import create_equipment_embed

#################
# ScrollListView
#################
class ScrollListView(View):
    def __init__(self, 
                 user: Member, 
                 player: Player,
                 slot_name: str,
                 index: int,
                 scroll_ids: List[str],
                 embeds: List[Embed],
                 timeout: int = 60,
                 scroll_per_page: int = 5):
        
        super().__init__(timeout = timeout)
        self.user = user
        self.player = player
        self.slot_name = slot_name
        self.index = index
        self.scroll_ids = scroll_ids
        self.embeds = embeds
        self.scroll_per_page = scroll_per_page
        
        self.current_page = 0
        self.total_pages = math.ceil(len(scroll_ids) / scroll_per_page)
        self.scroll_index = 0
        self.message = None
        
        # 基礎按鈕
        self.prev_button = ScrollPreviousPageButton(user = user, label = "⬅ 上一頁")
        self.next_button = ScrollNextPageButton(user = user, label = "➡ 下一頁")
        self.back_button = ScrollViewBackButton(user = user, label = "返回裝備介面")
        #self.add_item(self.prev_button)    
        
        # 卷軸按鈕 (動態)
        self.scroll_buttons: List[ScrollSelectButton] = []
        self._build_scroll_buttons()
        
        self.add_item(self.prev_button)
        self.add_item(self.next_button)
        self.add_item(self.back_button)
        self.update_button_state()
    
    def _build_scroll_buttons(self):
        """根據當前的 index 動態產生按鈕
        """
        for i in range(self.scroll_per_page):
            idx = self.scroll_index + i
            if idx < len(self.scroll_ids):
                button = ScrollSelectButton(user = self.user,
                                            label = self.scroll_ids[idx],
                                            index = idx)
                self.scroll_buttons.append(button)
                self.add_item(button)
        return
    
    def update_button_state(self):
        self.prev_button.disabled = self.current_page == 0
        self.next_button.disabled = self.current_page >= self.total_pages - 1

        for i, button in enumerate(self.scroll_buttons):
            idx = self.scroll_index + i
            if idx < len(self.scroll_ids):
                button.label = self.scroll_ids[idx]
                button.index = idx
                button.disabled = False
            else:
                button.label = "-"
                button.disabled = True
        return
    
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉介面",
                embed = None,
                view = None
            )
        return

###########################
# ScrollPreviousPageButton
###########################
class ScrollPreviousPageButton(BaseUserRestrictedButton):
    def __init__(self, 
                 user: Member, 
                 label: str):
        
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        view: ScrollListView = self.view
        if not await self.check_user(interaction):
            return
        
        view.current_page -= 1
        view.scroll_index -= 2
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"系統提示：請選擇卷軸",
            embed = view.embeds[view.current_page],
            view = view
        )
        return


#######################
# ScrollNextPageButton
#######################
class ScrollNextPageButton(BaseUserRestrictedButton):
    def __init__(self, 
                 user: Member, 
                 label: str):
        
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        view: ScrollListView = self.view
        if not await self.check_user(interaction):
            return
        
        view.current_page += 1
        view.scroll_index += 2
        view.update_button_state()
        await interaction.response.edit_message(
            content = f"系統提示：請選擇卷軸",
            embed = view.embeds[view.current_page],
            view = view
        )
        return

#####################
# ScrollSelectButton
#####################
class ScrollSelectButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, index: int):
        super().__init__(user = user, label = label, style = ButtonStyle.success)
        self.index = index
    
    async def callback(self, interaction: Interaction):
        view: ScrollListView = self.view
        if not await self.check_user(interaction):
            return


#######################
# ScrollViewBackButton
#######################
class ScrollViewBackButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.secondary)
    
    async def callback(self, interaction: Interaction):
        from ..equipment.equipment_panel import EquipmentFromInventoryView
        
        if not await self.check_user(interaction):
            return
        view: ScrollListView = self.view
        
        equipment = view.player.equipinventory.get_equipment(slot_name = view.slot_name,
                                                             index = view.index)
        embed = create_equipment_embed(equipment = equipment)
        new_view = EquipmentFromInventoryView(
            user = view.user,
            player = view.player,
            slot_name = view.slot_name,
            index = view.index,
            embed = embed
        )
        
        await interaction.response.edit_message(content = None,
                                                embed = embed,
                                                view = new_view)
