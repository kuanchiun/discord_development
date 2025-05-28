from typing import List

from discord import Member, Interaction, ButtonStyle, Embed
from discord.ui import Button

#################################
# BaseUserRestrictedButton class
#################################
class BaseUserRestrictedButton(Button):
    def __init__(self, user: Member, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    async def check_user(self, interaction: Interaction) -> bool:
        if interaction.user != self.user:
            await interaction.response.send_message("❌ 這不是你的介面喔！", ephemeral=True)
            return False
        return True
    
