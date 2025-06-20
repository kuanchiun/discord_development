from discord import Member, Interaction, ButtonStyle, Color, Embed
from discord.ui import View
from typing import Optional

from ...player.player import Player
from .equipment import Equipment
from ...basebutton import BaseUserRestrictedButton
from .equipment_utils import create_equipment_embed, create_equipment_compare_embed, EQUIP_SLOT_MAPPING
from ..scroll.scroll_utils import create_scroll_embed
from ..scroll.scroll_list_view import ScrollListView
from .confirm_equip_view import ConfirmEquipView

####################
# BaseEquipmentView
####################
class BaseEquipmentView(View):
    def __init__(self,
                 user: Member,
                 player: Player,
                 slot_name: str,
                 index: Optional[int],
                 embed: Embed,
                 timeout: int = 60):
        
        super().__init__(timeout = timeout)
        self.user = user
        self.player = player
        self.slot_name = slot_name
        self.index = index
        self.embed = embed
        self.message = None
        
        self.enhance_button = EnhanceButton(user = user, label = "衝卷！")
        #self.potential_button = PotentialButton()
        #self.dismantle_button = DisMantleButton()
        #self.sell_button = SellButton()
        #self.equipment_back_button = EquipmentBackButton()
        #self.close_equipment_button = CloseEquipmentButton()

################
# EquipmentView
################
class EquipmentFromInventoryView(BaseEquipmentView):
    def __init__(self, user: Member, player: Player, slot_name: str, index: int, embed: Embed, timeout: int = 60):
        super().__init__(user = user,
                         player = player,
                         slot_name = slot_name,
                         index = index,
                         embed = embed,
                         timeout = timeout)
        
        self.add_item(EquipButton(user = user, label = f"裝備到{EQUIP_SLOT_MAPPING[slot_name]}", target_slot_name = slot_name))
        if slot_name == "ring":
            target_slot_name = f"{slot_name}2"
            self.add_item(EquipButton(user = user, label = f"裝備到{EQUIP_SLOT_MAPPING[target_slot_name]}", target_slot_name = target_slot_name))
    
        self.add_item(self.enhance_button)
        
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉介面",
                embed = None,
                view = None
            )
        return

##############
# EquipButton
##############
class EquipButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, target_slot_name: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        self.target_slot_name = target_slot_name
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        view: EquipmentFromInventoryView = self.view
        select_equipment = view.player.equipinventory.get_equipment(slot_name = view.slot_name,
                                                                    index = view.index)
        
        if view.player.equipmentslot.is_already_equipped(view.slot_name):
            compare_equipment = view.player.equipmentslot.get_slot(view.slot_name)
            embed = create_equipment_compare_embed(select_equipment = select_equipment,
                                                   compare_equipment = compare_equipment)
        else:
            embed = create_equipment_embed(equipment = select_equipment)
        
        new_view = ConfirmEquipView(user = view.user,
                                    player = view.player,
                                    slot_name = view.slot_name,
                                    target_slot_name = self.target_slot_name,
                                    index = view.index,
                                    embed = view.embed)
        
        if view.player.equipmentslot.is_already_equipped(view.slot_name):
            await interaction.response.edit_message(
                content = f"你即將使用**{select_equipment.get_display_name()}**替換**{compare_equipment.get_display_name()}**，是否替換？",
                embed = embed,
                view = new_view
            )
        else:
            await interaction.response.edit_message(
                content = f"你確定要將**{select_equipment.get_display_name()}**裝備到**{EQUIP_SLOT_MAPPING[self.target_slot_name]}**嗎？",
                embed = embed,
                view = new_view
            )
            
        new_view.message = await interaction.original_response()
        return

################
# EnhanceButton
################
class EnhanceButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)

    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        view: EquipmentFromInventoryView = self.view
        scrolls = view.player.iteminventory.filter_by_type("scroll")
        
        scroll_ids = [key for scroll in scrolls for key, value in scroll.items()]
        embeds = create_scroll_embed(scrolls)
        
        new_view = ScrollListView(user = view.user,
                                  player = view.player,
                                  slot_name = view.slot_name,
                                  index = view.index,
                                  scroll_ids = scroll_ids,
                                  embeds = embeds)
        
        await interaction.response.edit_message(
            content = f"測試",
            embed = embeds[0],
            view = new_view
        )