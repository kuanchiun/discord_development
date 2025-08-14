from discord import Interaction, app_commands
from discord.ext import commands

from .utils.lottery import DrawLotteryView, Lottery
from .utils.player.player import Player


###################
# LotteryCog class
###################
class LotteryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lottery = Lottery()
        
    @app_commands.command(name = "抽獎", description = "來試試手氣吧！")
    async def draw(self, interaction: Interaction):
        user = interaction.user
        user_id = interaction.user.id
        
        if Player.exists(user_id):
            player = Player.load(user_id)
            view = DrawLotteryView(user, player, self.lottery)
            await interaction.response.send_message(
                content = f"系統提示：抽獎！ 你的💎水晶持有數：{player.iteminventory.money}",
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
    await bot.add_cog(LotteryCog(bot))