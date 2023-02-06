import nextcord
from nextcord import *
from nextcord.ext import commands

import func
from func import color

import config
from config import module

class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="developer", name_localizations=func.locale("개발자", "developer"), description="Show discord-hotel bot developer information", description_localizations=func.locale("디코호텔 개발자 정보를 보여줍니다", "Show discord-hotel bot developer information"))
    async def developer(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if func.isKo(interaction):
            embed = nextcord.Embed(title="개발자 정보", color=func.embed)
            embed.add_field(name="이름", value="ㅂㅇㅊ#2978", inline=True)
            embed.add_field(name="ID", value="912950179055935489", inline=True)
            embed.add_field(name="링크", value="[Github](https://github.com/GithubNeon)", inline=True)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/987530663475421224/1047073799604011018/profile.png")
        else:
            embed = nextcord.Embed(title="Developer Information", color=func.embed)
            embed.add_field(name="name", value="ㅂㅇㅊ#2978", inline=True)
            embed.add_field(name="id", value="912950179055935489", inline=True)
            embed.add_field(name="link", value="[Github](https://github.com/GithubNeon)", inline=True)
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/987530663475421224/1047073799604011018/profile.png")
        await interaction.followup.send(embed=embed)

    @nextcord.slash_command(name="ping", name_localizations=func.locale("핑", "ping"), description="show ping", description_localizations=func.locale("핑을 보여줍니다", "show ping"))
    async def ping(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        pings = round(self.bot.latency * 1000)
        embed = nextcord.Embed(title=":ping_pong: Pong!", description=f"{pings}ms", color=func.embed)
        await interaction.followup.send(embed=embed)

    @nextcord.slash_command(name="genius", description="IM GENIUS")
    async def genius(self, interaction: nextcord.Interaction):
        if interaction.user.id == module.developer_id:
            await interaction.response.send_message("IM GENIUS!")
        else:
            await interaction.response.send_message("YOU NOT GENIUS!")

def setup(bot):
    bot.add_cog(dev(bot))
