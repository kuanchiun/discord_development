from discord import Member, Interaction, ButtonStyle, Color
from discord.ui import View

from ...player.player import Player
from .equipment import Equipment
from ...basebutton import BaseUserRestrictedButton

######################
# EquipmentView Class
######################
class EquipmentView(View):
    def __init__(self, user: Member, player: Player):
        ...