from discord.ext import commands
from discord import app_commands, Interaction

from .utils.player.player import Player
from .utils.player.equipinventory import EquipInventory
from .utils.player.equipinventory_panel import EquipInventoryView
from .utils.player.equipinventory_slot_view import EquipSlotView
from .utils.player.equipinventory_utils import create_slot_embed

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
        else:
            await interaction.response.send_message(
                content = "⚠️ 系統提示：你尚未創建角色！",
            )

async def setup(bot):
    await bot.add_cog(EquipInventoryCog(bot))