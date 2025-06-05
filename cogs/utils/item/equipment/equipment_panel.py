from discord import Member, Interaction, ButtonStyle, Color, Embed
from discord.ui import View

from ...player.player import Player
from .equipment import Equipment
from ...basebutton import BaseUserRestrictedButton
from .equipment_utils import create_equipment_embed, create_equipment_compare_embed, EQUIP_SLOT_MAPPING
from .confirm_equip_view import ConfirmEquipView

################
# EquipmentView
################
class EquipmentView(View):
    def __init__(self, user: Member, player: Player, slot_name: str, index: int, embed: Embed, timeout: int = 60):
        super().__init__(timeout = timeout)
        self.user = user
        self.player = player
        self.slot_name = slot_name
        self.index = index
        self.embed = embed
        self.message = None
        
        self.add_item(EquipButton(user = user, label = f"裝備到{EQUIP_SLOT_MAPPING[slot_name]}", target_slot_name = slot_name))
        if slot_name == "ring":
            target_slot_name = f"{slot_name}2"
            self.add_item(EquipButton(user = user, label = f"裝備到{EQUIP_SLOT_MAPPING[target_slot_name]}", target_slot_name = target_slot_name))
        #self.add_item(EnhanceButton())
        #self.add_item(PotentialButton())
        #self.add_item(DisMantleButton())
        #self.add_item(SellButton)
        #self.add_item(EquipmentBackButton())
        #self.add_item(CloseEquipmentButton())
    
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
        
        view: EquipmentView = self.view
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

###############