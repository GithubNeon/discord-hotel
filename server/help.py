import nextcord
from nextcord import *
from nextcord.ext import commands

import func
from func import locale

import lang
from lang import ko, en


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="help", name_localizations=func.locale("명령어", "help"), description="Show discord-hotel bot commands", description_localizations=func.locale("디코호텔 봇 명령어를 보여줍니다", "Show discord-hotel bot commands"))
    async def help(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        if func.isKo(interaction):
            await interaction.followup.send(view=lang.ko.help_menu_view())
        else:
            await interaction.followup.send(view=lang.en.help_menu_view())


def setup(bot):
    bot.add_cog(help(bot))
