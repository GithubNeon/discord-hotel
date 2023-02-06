import nextcord
from nextcord import *
from nextcord.ext import commands
from nextcord.utils import get

import func
from func import color, emojis, locale

import lang
from lang import ko, en

class vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="yes_no_vote", name_localizations=func.locale("찬반투표", "yes_no_vote"), description="yes_no_vote", description_localizations=func.locale("찬반투표 기능입니다", "yes_no_vote"))
    async def 찬반투표(self, interaction: nextcord.Interaction, 투표주제: str = SlashOption(name="topic", name_localizations=func.locale("투표주제", "topic"), description="topic", description_localizations=func.locale("투표 주제를 적어주세요", "topic"))):
        if func.isKo(interaction):
            embed = nextcord.Embed(title=f"📋 투표주제 : {투표주제}", description=f"{emojis.good()} | 0표\n{emojis.bad()} | 0표", color=func.embed)
            await interaction.response.send_message(embed=embed, view=lang.ko.yes_no_vote_button(title=투표주제, admin=interaction.user))
        else:
            embed = nextcord.Embed(title=f"📋 topic : {투표주제}", description=f"{emojis.good()} | 0 vote\n{emojis.bad()} | 0 vote", color=func.embed)
            await interaction.response.send_message(embed=embed, view=lang.en.yes_no_vote_button(title=투표주제, admin=interaction.user))

    @nextcord.slash_command(name="vote", name_localizations=func.locale("투표", "vote"), description="vote", description_localizations=func.locale("투표", "vote"))
    async def 투표(self, interaction: nextcord.Interaction):
        if func.isKo(interaction):
            await interaction.response.send_modal(lang.ko.vote_modal())
        else:
            await interaction.response.send_modal(lang.en.vote_modal())

def setup(bot):
    bot.add_cog(vote(bot))
