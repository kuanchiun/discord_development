from discord import Member, Interaction, ButtonStyle
from discord.ui import View

from ...player.player import Player
from .equipment import Equipment
from ...basebutton import BaseUserRestrictedButton

#########################
# ConfirmEquipView class
#########################
class ConfirmEquipView(View):
    def __init__(self, user: Member, player: Player, equipment: Equipment, timeout = 60):
        super().__init__(timeout = timeout)
        self.user = user
        self.player = player
        self.equipment = equipment
        
        self.add_item(ConfirmEquipButton())
        self.add_item(CancelEquipButton())
    

###########################
# ConfirmEquipButton class
###########################
class ConfirmEquipButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        ...

##########################
# CancelEquipButton class
##########################
class CancelEquipButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        ...


#########################
# EquipResultView class
#########################
class ConfirmEquipView(View):
    def __init__(self, user: Member, player: Player, equipment: Equipment, timeout = 60):
        super().__init__(timeout = timeout)
        self.user = user
        self.player = player
        self.equipment = equipment
        
        self.add_item(ConfirmEquipButton())
        self.add_item(CancelEquipButton())
    

###########################
# EquipResultBackButton class
###########################
class EquipResultBackButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        ...

##########################
# CloseEquipResultButton class
##########################
class CloseEquipResultButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        ...