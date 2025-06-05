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
        
        self.add_item(ConfirmEquipButton(user = user, label = "確定"))
        self.add_item(CancelEquipButton(user = user, label = "取消"))
    
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉介面",
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
        equipment = view.player.equipinventory.get_equipment(slot_name = view.slot_name, 
                                                             index = view.index)
        equipment_display_name = equipment.get_display_name()
        
        view.player.equipmentslot.equip(slot_name = view.slot_name,
                                        index = view.index,
                                        equipinventory = view.player.equipinventory)
        view.player.save(view.user.id)
        
        new_view = EquipResultView(user = self.user,
                                   player = view.player,
                                   slot_name = view.slot_name)
        
        await interaction.response.edit_message(
            content = f"你已經成功裝備{equipment_display_name}",
            embed = view.embed,
            view = new_view
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
            content = None,
            embed = view.embed,
            view = new_view
        )
        return

##################
# EquipResultView
##################
class EquipResultView(View):
    def __init__(self, 
                 user: Member, 
                 player: Player, 
                 slot_name: str,
                 timeout: int = 60):
        
        super().__init__(timeout = timeout)
        self.user = user
        self.player = player
        self.slot_name = slot_name
        self.message = None
        
        self.add_item(EquipResultBackButton(user = user, label = "返回裝備背包介面"))
        self.add_item(CloseEquipResultButton(user = user, label = "關閉介面"))
    
    async def on_timeout(self):
        if self.message:
            await self.message.edit(
                content = "⏰ 操作逾時，關閉介面",
                embed = None,
                view = None
            )
        return

########################
# EquipResultBackButton
########################
class EquipResultBackButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        from ...equipinventory.equipinventory_panel import EquipInventoryView
        
        view: EquipResultView = self.view
        new_view = EquipInventoryView(user = view.user)
        await interaction.response.send_message(
            content = "系統提示：請選擇裝備欄位",
            view = new_view,
            ephemeral = True
        )
        view.message = await interaction.original_response()
        
        return

#########################
# CloseEquipResultButton
#########################
class CloseEquipResultButton(BaseUserRestrictedButton):
    def __init__(self, user: Member, label: str):
        super().__init__(user = user, label = label, style = ButtonStyle.primary)
    
    async def callback(self, interaction: Interaction):
        if not await self.check_user(interaction):
            return
        
        await interaction.response.edit_message(
            content = "系統提示：已關閉介面",
            embed = None,
            view = None
        )
        
        return