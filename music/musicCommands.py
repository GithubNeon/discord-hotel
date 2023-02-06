import nextcord

from nextcord import *
from nextcord.ext import commands

import nextwave

class musicCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="join", description="join voice channel")
    async def join(self, interaction : nextcord.Interaction):
        await interaction.user.voice.channel.connect()
        await interaction.response.send_message(f"<#{interaction.user.voice.channel.id}> 에 접속했습니다", delete_after=5)

    @nextcord.slash_command(name="leave", description="leave voice channel")
    async def leave(self, interaction : nextcord.Interaction):
        vc: nextwave.Player = interaction.guild.voice_client
        await vc.stop()
        await vc.disconnect()
        await interaction.response.send_message(f"<#{interaction.user.voice.channel.id}> 에서 나왔습니다", delete_after=5)

def setup(bot):
    bot.add_cog(musicCommand(bot))