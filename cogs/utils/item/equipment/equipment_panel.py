from discord import Member, Interaction, ButtonStyle, Color
from discord.ui import View

from ...player.player import Player
from .equipment import Equipment
from ...basebutton import BaseUserRestrictedButton

#####################
# EquipmentViewClass
#####################
class EquipmentView(View):
    def __init__(self, user: Member, player: Player, equipment: Equipment):
        super().__init__(timeout = 60)
        self.user = user
        self.player = player
        self.equipment = equipment
        
        self.add_item(EquipButton())
        self.add_item(EnhanceButton())
        self.add_item(PotentialButton())
        self.add_item(DisMantleButton())
        self.add_item(SellButton)
        self.add_item(EquipmentBackButton())
        self.add_item(CloseEquipmentButton())
    

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
        
        
        
        
    