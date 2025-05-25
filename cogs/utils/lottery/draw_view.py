from discord import Embed, Member, Interaction, ButtonStyle
from discord.ui import Button, View

class BaseDrawView(View):
    def __init__(self, embed: Embed, user: Member, timeout: int = 30):
        super().__init__(timeout = timeout)
        self.embed = embed
        self.user = user
        
class DrawView(BaseDrawView):
    def __init__(self, embed: Embed, user: Member, timeout: int = 30):
        super().__init__(embed = embed, user = user, timeout = timeout)
        
        self.add_item(PublicDrawButton(self.embed, self.user))

class PublicDrawView(BaseDrawView):
    def __init__(self, embed: Embed, user: Member, timeout: int = 60):
        super().__init__(embed = embed, user = user, timeout = timeout)

class PublicDrawButton(Button):
    def __init__(self, embed: Embed, user: Member):
        super().__init__(label = "📢 公開顯示", style = ButtonStyle.primary)
        self.embed = embed
        self.user = user
    
    async def callback(self, interaction: Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message("⚠️ 系統提示：這不是你的抽獎結果喔！", ephemeral=True)
            return
        
        view = PublicDrawView(self.embed, self.user)
        await interaction.response.send_message(
            content = f"⚠️ 系統提示：🎁 {interaction.user.display_name} 公開了他的單抽結果",
            embed = self.embed,
            view = view  # ✅ 使用公開版本
        )