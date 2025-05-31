from discord.ext import commands
from discord import app_commands, Interaction

from .utils.player.player import Player
from .utils.equipinventory.equipinventory_panel import EquipInventoryView

##########################
# EquipInventoryCog class
##########################
class EquipInventoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name = "裝備背包", description = "打開你的裝備背包")
    async def open_equipinventory(self, interaction: Interaction):
        user = interaction.user
        user_id = interaction.user.id
        
        if Player.exists(user_id):
            view = EquipInventoryView(user = user)
            await interaction.response.send_message(
                content = "系統提示：請選擇裝備欄位",
                view = view,
                ephemeral = True
            )
            view.message = await interaction.original_response()
        else:
            await interaction.response.send_message(
                content = "⚠️ 系統提示：你尚未創建角色！",
            )
        return

async def setup(bot: commands.Bot):
    await bot.add_cog(EquipInventoryCog(bot))