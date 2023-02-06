import nextcord
from nextcord import *
from nextcord.ext import commands
from nextcord.utils import get

import datetime
from datetime import *

import func
from func import color


class utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="user", name_localizations=func.locale("내정보", "user"), description="Show Discord user information", description_localizations=func.locale("디스코드 유저 정보를 보여줍니다", "Show Discord user information"))
    async def user(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        date = datetime.utcfromtimestamp(
            ((int(interaction.user.id) >> 22) + 1420070400000) / 1000)
        if func.isKo(interaction):
            embed = nextcord.Embed(title="유저정보", color=func.embed)
            embed.add_field(name="디스코드 닉네임", value=f"{interaction.user}", inline=False)
            embed.add_field(name="디스코드 별명", value=f"{interaction.user.display_name}", inline=False)
            embed.add_field(name="디스코드 가입일", value=f"{date.year}년 {date.month}월 {date.day}일 {date.hour}시 {date.minute}분", inline=False)
            embed.add_field(name="디스코드 고유 ID", value=f"{interaction.user.id}", inline=False)
            embed.add_field(name="디스코드 상태", value=(interaction.user.status.name).replace("online", '```py\n" 온라인 "\n```').replace("idle", "```fix\n자리 비움\n```").replace("dnd", "```diff\n- 다른 용무 중\n```").replace("offline", "```py\n# 오프라인\n```"))
            embed.set_thumbnail(url=f"{interaction.user.avatar}")
        else:
            embed = nextcord.Embed(title="user info", color=func.embed)
            embed.add_field(name="name", value=f"{interaction.user}", inline=False)
            embed.add_field(name="nick", value=f"{interaction.user.display_name}", inline=False)
            embed.add_field(name="id", value=f"{interaction.user.id}", inline=False)
            embed.add_field(name="member since", value=f"{date.year}y {date.month}m {date.day}d {date.hour}h {date.minute}m", inline=False)
            embed.add_field(name="status", value=(interaction.user.status.name).replace("online", '```py\n"online"\n```').replace("idle", "```fix\nidle 비움\n```").replace("dnd", "```diff\n- dnd\n```").replace("offline", "```py\n# offline\n```"))
            embed.set_thumbnail(url=f"{interaction.user.avatar}")
        await interaction.followup.send(embed=embed)

    @nextcord.slash_command(name="server_info", name_localizations=func.locale("서버정보", "server_info"), description="Show server information", description_localizations=func.locale("서버에 대한 정보를 보여줍니다", "Show server information"))
    async def server_info(self, interaction: nextcord.Interaction):
        await interaction.response.defer()
        bot = 0
        for i in range(interaction.guild.member_count):
            if interaction.guild.members[i].bot:
                bot += 1
        if func.isKo(interaction):
            embed = nextcord.Embed(title=f'"{interaction.guild.name}" 서버 정보입니다', color=func.embed)
            embed.add_field(name="서버장", value=f"{interaction.guild.owner.mention}", inline=True)
            embed.add_field(name="서버 생성일", value="" + interaction.guild.created_at.strftime(f"20%y년 %m월 %d일"), inline=True)
            embed.add_field(name="서버 인증 단계", value=(str(interaction.guild.verification_level)+" ").replace("none", "없음").replace("low", "낮음").replace("medium", "중간").replace("high", "높음".replace("highest", "매우 높음")), inline=True)
            embed.add_field(name="서버 인원수", value=f"유저 : {interaction.guild.member_count}명\n봇 : {bot}명\n유저 : {interaction.guild.member_count-bot}명", inline=True)
            embed.add_field(name="채널 갯수", value=f"채팅채널 : {len(interaction.guild.text_channels)}개\n음성채널 : {len(interaction.guild.voice_channels)}개\n카테고리 : {len(interaction.guild.categories)}개")
            embed.set_thumbnail(url=f"{interaction.guild.icon}")
        else:
            embed = nextcord.Embed(title=f'"{interaction.guild.name}" server information', color=func.embed)
            embed.add_field(name="owner", value=f"{interaction.guild.owner.mention}", inline=True)
            embed.add_field(name="server since", value="" + interaction.guild.created_at.strftime(f"20%yy %mm %dd"), inline=True)
            embed.add_field(name="server verifycation level", value=(str(interaction.guild.verification_level)), inline=True)
            embed.add_field(name="member count", value=f"all member : {interaction.guild.member_count}\nbot : {bot}\nuser : {interaction.guild.member_count-bot}", inline=True)
            embed.add_field(name="channel count", value=f"chat : {len(interaction.guild.text_channels)}\nvoice : {len(interaction.guild.voice_channels)}\ncategory : {len(interaction.guild.categories)}")
            embed.set_thumbnail(url=f"{interaction.guild.icon}")
        await interaction.followup.send(embed=embed)


def setup(bot):
    bot.add_cog(utils(bot))
