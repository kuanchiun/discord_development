from discord import Member, Interaction, ButtonStyle, Color, Embed
from discord.ui import View

from ...player.player import Player

#################
# ScrollListView
#################
class ScrollListView(View):
    def __init__(self, 
                 user: Member, 
                 player: Player,
                 slot_name: str,
                 index: int,
                 timeout: int = 60):
        
        super().__init__(timeout = timeout)
        self.user = user
        self.player = player
        self.slot_name = slot_name
        self.index = index
        self.message = None