import re

import discord
import requests
from discord.ext import commands


class IwaraEmbed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.url_pattern = re.compile(r"(https?://(?:www\.)?iwara\.tv/video/\w+)")

    """
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        match = self.url_pattern.search(message.content)
        if not match:
            return

        video_url = match.group(1)
        video_id = re.search(r"iwara\.tv/video/([^/?#]+)", video_url).group(1)
        api_url = f"https://api.iwara.tv/video/{video_id}"

        res = requests.get(api_url, timeout=10)
        data = res.json()

        title = data.get("title", "未命名影片")
        file_name = data["file"].get("id", "")
        thumbnail = f"https://i.iwara.tv/image/thumbnail/{file_name}/thumbnail-00.jpg"
        tags = data.get("tags", [])
        tag_list = []
        for tag in tags:
            tag_list.append(tag["id"])
        tags_text = ", ".join(tag_list)
        user = data["user"].get("name", "")

        embed = discord.Embed(
            title=title,
            url=f"https://www.iwara.tv/video/{video_id}",
            description="🔞 Iwara 影片預覽",
            color=discord.Color.red()
        )

        if thumbnail and thumbnail.startswith("https"):
            embed.set_image(url=thumbnail)
        if tags:
            embed.add_field(name="🎯 Tags", value=tags_text, inline=False)
        
        embed.set_author(
            name = user,  # 作者暱稱
        )
        
        await message.channel.send(embed=embed)
        await message.delete()
    """

async def setup(bot: commands.Bot):
    await bot.add_cog(IwaraEmbed(bot))
