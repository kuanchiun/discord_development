from discord import Member, Interaction, ButtonStyle, Color
from discord.ui import View

from ...player.player import Player
from .equipment import Equipment
from ...basebutton import BaseUserRestrictedButton
from .equipment_utils import create_equipment_embed, create_equipment_compare_embed, EQUIP_SLOT_MAPPING

################
# EquipmentView
################
class EquipmentView(View):
    def __init__(self, user: Member, player: Player, slot_name: str, index: int, timeout: int = 60):
        super().__init__(timeout = timeout)
        self.user = user
        self.player = player
        self.slot_name = slot_name
        self.index = index
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
    
    #async def on_timeout(self):
    #    return await super().on_timeout()


##############
# EquipButton
##############
class EquipButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str, target_slot_name: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        view: EquipmentView = self.view
        select_equipment = view.player.equipinventory.get_equipment(slot_name = view.slot_name,
                                                                    index = view.index)
        
        if view.player.equipmentslot.is_already_equipped(view.slot_name):
            embed = create_equipment_compare_embed(player = view.player,
                                                   slot_name = view.slot_name,
                                                   index = view.index)
        else:
            embed = create_equipment_embed(select_equipment)
        
        await interaction.response.edit_message(
            content = "測試",
            embed = embed,
            view = None
        )