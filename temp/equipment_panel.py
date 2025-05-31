from discord import Member, Interaction, ButtonStyle, Color
from discord.ui import View

from ...player.player import Player
from .equipment import Equipment
from ...basebutton import BaseUserRestrictedButton
from .confirm_equip_view import ConfirmEquipView
from .equipment_utils import create_equipment_compare_embed

#####################
# EquipmentViewClass
#####################
class EquipmentView(View):
    def __init__(self, user: Member, player: Player, slot_name: str, index: int):
        super().__init__(timeout = 60)
        self.user = user
        self.player = player
        self.slot_name = slot_name
        self.index = index
        
        self.add_item(EquipButton())
        #self.add_item(EnhanceButton())
        #self.add_item(PotentialButton())
        #self.add_item(DisMantleButton())
        #self.add_item(SellButton)
        #self.add_item(EquipmentBackButton())
        #self.add_item(CloseEquipmentButton())
    

##############
# EquipButton
##############
class EquipButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
        
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        view: EquipmentView = self.view
        embed = create_equipment_compare_embed(player = view.player,
                                               slot_name = view.slot_name,
                                               index = view.index)
        
        await interaction.response.edit_message(
            content = "替換裝備",
            embed = embed
        )
        
        
        
        
        
        
    