from discord import Member, Interaction, ButtonStyle, Color, Embed
from discord.ui import View

from ...player.player import Player
from .equipment import Equipment
from ...basebutton import BaseUserRestrictedButton
from .equipment_utils import create_equipment_embed, create_equipment_compare_embed, EQUIP_SLOT_MAPPING

###################
# ConfirmEquipView
###################
class ConfirmEquipView(View):
    def __init__(self, 
                 user: Member, 
                 player: Player, 
                 slot_name: str,
                 target_slot_name: str,
                 index: int,
                 embed: Embed,
                 timeout: int = 60):
        
        super().__init__(timeout = timeout)
        self.user = user
        self.player = player
        self.slot_name = slot_name
        self.target_slot_name = target_slot_name
        self.index = index
        self.embed = embed
        self.message = None
        
        self.add_item(ConfirmEquipButton(user = user, label = "確定裝備"))
        self.add_item(CancelEquipButton(user = user, label = "取消裝備"))
    
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉裝備介面。",
                embed = None,
                view = None
            )
        return

#####################
# ConfirmEquipButton
#####################
class ConfirmEquipButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        view: ConfirmEquipView = self.view
        
        view.player.equipmentslot.equip(slot_name = view.slot_name,
                                        index = view.index,
                                        equipinventory = view.player.equipinventory)
        view.player.save(view.user.id)
        
        await interaction.response.edit_message(
            content = "成功",
            embed = None,
            view = None
        )

####################
# CancelEquipButton
####################
class CancelEquipButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        view: ConfirmEquipView = self.view
        from .equipment_panel import EquipmentView
        new_view = EquipmentView(user = view.user,
                                 player = view.player,
                                 slot_name = view.slot_name,
                                 index = view.index,
                                 embed = view.embed)
        await interaction.response.edit_message(
            content = "測試",
            embed = view.embed,
            view = new_view
        )