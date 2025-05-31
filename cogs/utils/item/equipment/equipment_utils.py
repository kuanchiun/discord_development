from discord import Member, Interaction, ButtonStyle, Embed

from ...player.player import Player
from .equipment import Equipment

def create_equipment_compare_embed(player: Player, slot_name: str, index: int) -> Embed:
    select_equipment = player.equipinventory.get_slot(slot_name = slot_name)[index]
    compare_equipment = player.equipmentslot.is_already_equipped(slot_name = slot_name)
    
    embed = Embed()
    
    if compare_equipment:
        ...
    
    
    ...