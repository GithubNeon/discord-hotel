import nextcord
from nextcord import *
from nextcord.ext import commands
from nextcord.utils import get

import datetime
from datetime import timedelta

import time
from time import *

import func
from func import color

from config import module


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="kick", name_localizations=func.locale("추방", "kick"), description="Kick the user from the server", description_localizations=func.locale("유저를 서버에서 추방합니다", "Kick the user from the server"), default_member_permissions=nextcord.Permissions(kick_members=True))
    async def kick(self, interaction: nextcord.Interaction, user: nextcord.Member = SlashOption(name="user", name_localizations=func.locale("유저", "user"), description="select user", description_localizations=func.locale("유저를 선택하세요", "select user")), reason: str = SlashOption(name="reason", name_localizations=func.locale("사유", "reason"), description="reason for deportation", description_localizations=func.locale("추방 사유", "reason for deportation"))):
        await interaction.response.defer()
        if func.isKo(interaction):
            await user.kick(reason=reason)
            embed = nextcord.Embed(title=f"{user}님을 {interaction.guild.name} 서버에서 추방했습니다.", color=func.embed)
            embed.add_field(name="추방 사유", value=reason, inline=True)
            embed.add_field(name="디스코드 닉네임", value=user, inline=True)
            embed.add_field(name="디스코드 ID", value=user.id, inline=True)
            embed.set_author(name=user, icon_url=user.avatar)
        else:
            await user.kick(reason=reason)
            embed = nextcord.Embed(title=f"{user} has been kicked out of the {interaction.guild.name} server.", color=func.embed)
            embed.add_field(name="reason", value=reason, inline=True)
            embed.add_field(name="user", value=user, inline=True)
            embed.add_field(name="id", value=user.id, inline=True)
            embed.set_author(name=user, icon_url=user.avatar)
        await interaction.followup.send(embed=embed)

    @nextcord.slash_command(name="ban", name_localizations=func.locale("차단", "ban"), description="Ban the user from the server", description_localizations=func.locale("유저를 서버에서 차단합니다", "Ban the user from the server"), default_member_permissions=nextcord.Permissions(ban_members=True))
    async def ban(self, interaction: nextcord.Interaction, user: nextcord.Member = SlashOption(name="user", name_localizations=func.locale("유저", "user"), description="select user", description_localizations=func.locale("유저를 선택하세요", "select user")), reason: str = SlashOption(name="reason", name_localizations=func.locale("사유", "reason"), description="ban reason", description_localizations=func.locale("차단 사유", "ban reason"))):
        await interaction.response.defer()
        if func.isKo(interaction):
            await user.ban(reason=reason)
            embed = nextcord.Embed(title=f"{user}님을 {interaction.guild.name} 서버에서 차단했습니다.", color=func.embed)
            embed.add_field(name="차단 사유", value=reason, inline=True)
            embed.add_field(name="디스코드 닉네임", value=user, inline=True)
            embed.add_field(name="디스코드 ID", value=user.id, inline=True)
            embed.set_author(name=user, icon_url=user.avatar)
        else:
            await user.ban(reason=reason)
            embed = nextcord.Embed(title=f"{user} has been blocked out of the {interaction.guild.name} server.", color=func.embed)
            embed.add_field(name="reason", value=reason, inline=True)
            embed.add_field(name="user", value=user, inline=True)
            embed.add_field(name="id", value=user.id, inline=True)
            embed.set_author(name=user, icon_url=user.avatar)
        await interaction.followup.send(embed=embed)

    @nextcord.slash_command(name="clear", name_localizations=func.locale("청소", "clear"), description="delete message", description_localizations=func.locale("메세지를 삭제합니다", "delete message"), default_member_permissions=nextcord.Permissions(manage_messages=True))
    async def clear(self, interaction: nextcord.Interaction, count: int = SlashOption(name="count", name_localizations=func.locale("숫자", "count"), description="number of messages to delete", description_localizations=func.locale("삭제할 메세지 개수", "number of messages to delete"))):
        await interaction.channel.purge(limit=count)
        if func.isKo(interaction):
            await interaction.response.defer()
            await interaction.followup.send(embed=nextcord.Embed(description=f"{count}개의 메시지를 삭제했습니다.", color=func.embed), delete_after=5)
        else:
            await interaction.response.defer()
            await interaction.followup.send(embed=nextcord.Embed(description=f"Deleted {count} messages", color=func.embed), delete_after=5)

    @nextcord.slash_command(name="timeout", name_localizations=func.locale("타임아웃", "timeout"), description="timeout the user from the server", description_localizations=func.locale("유저를 서버에서 타임아웃 합니다", "timeout the user from the server"), default_member_permissions=nextcord.Permissions(moderate_members=True))
    async def timeout(self, interaction: nextcord.Interaction, user: nextcord.Member = SlashOption(name="user", name_localizations=func.locale("유저", "user"), description="select user", description_localizations=func.locale("유저를 선택하세요", "select user")), time: int = SlashOption(name="time", name_localizations=func.locale("시간", "time"), description="timeout time", description_localizations=func.locale("타임아웃 시간", "timeout time")), unit: str = SlashOption(name="unit", name_localizations=func.locale("단위", "unit"), description="unit", description_localizations=func.locale("단위", "unit"), choices=module.en_timeList, choice_localizations=func.locale(module.ko_timeList, module.en_timeList)), reason: str = SlashOption(name="reason", name_localizations=func.locale("사유", "reason"), description="reason for deportation", description_localizations=func.locale("타임아웃 사유", "reason from timeout"))):
        choice: int = {"s": 1, "m": 60, "h": 3600}[unit]
        await interaction.response.defer()
        await user.edit(timeout=utils.utcnow() + datetime.timedelta(seconds=time*choice))
        if func.isKo(interaction):
            await interaction.followup.send(embed=nextcord.Embed(title=f"{user.name}님을 {time}{unit}동안 타임아웃 했습니다", description=f"**사유 : {reason}**", color=func.embed))
        else:
            await interaction.followup.send(embed=nextcord.Embed(title=f"{user.name} timed out for {time}{unit}", description=f"**reason : {reason}**", color=func.embed))


def setup(bot):
    bot.add_cog(admin(bot))
