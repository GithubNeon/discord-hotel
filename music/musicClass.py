import nextcord
from nextcord import *

from nextcord.ext import commands

import nextwave

import json

import func
from func import emojis

import math
import time

import datetime
from datetime import timedelta

import config
from config import module, musicType

class MusicPlayer(nextcord.ui.View):
    def __init__(self, vc: nextwave.Player, musicArray: list, q, admin: Member = None):
        super().__init__(timeout=math.inf)

        self.vc = vc
        self.musicArray = musicArray
        self.q = q
        self.admin = admin

    @nextcord.ui.button(label="정지", style=nextcord.ButtonStyle.gray, emoji=emojis.musicStop())
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.admin == interaction.user or self.admin == None:
            vc: nextwave.Player = interaction.guild.voice_client

            try:
                await interaction.user.voice.channel.connect(cls=nextwave.Player)
            except:
                pass

            for item in self.children:
                item.disabled = True

            vc.loop = False
            song_number = 1
            musicType.music_loop_type = 1
            musicType.playlist = []
            musicType.music_shuffle = False
            await self.vc.stop()
            await self.vc.disconnect()

            embed = nextcord.Embed(title=f"음악재생을 마칩니다.", color=func.embed)

            await interaction.message.edit(embed=embed, view=self, delete_after=3)
        else:
            await interaction.response.send_message(embed=Embed(title="자신의것을 사용해주세요!", color=func.embed), ephemeral=True)

    @nextcord.ui.button(label="일시정지", style=nextcord.ButtonStyle.gray, emoji=emojis.musicPause())
    async def pause(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.admin == interaction.user or self.admin == None:
            if self.vc.is_paused():
                await self.vc.resume()
                button.emoji = emojis.musicPause()
                button.label = "일시정지"
                await interaction.message.edit(view = self)
                return await interaction.response.send_message("일시정지중인 곡을 다시재생 했습니다", delete_after=3)
            await self.vc.pause()
            button.emoji = emojis.musicPlay()
            button.label = "다시재생"
            await interaction.message.edit(view = self)
            await interaction.response.send_message("재생중인 곡을 일시정지 했습니다", delete_after=3)
        else:
            await interaction.response.send_message(embed=Embed(title="자신의것을 사용해주세요!", color=func.embed), ephemeral=True)

    @nextcord.ui.button(label="스킵", style=nextcord.ButtonStyle.gray, emoji=emojis.musicDisabled())
    async def skip(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.admin == interaction.user or self.admin == None:
            vc: nextwave.Player = interaction.guild.voice_client
            try:
                if vc.is_playing():
                    next_song = vc.queue.get()
                    await vc.play(next_song)
                    MUSIC : nextwave.Track = self.musicArray[0]
                    embed = nextcord.Embed(title=f"{next_song}", color=func.embed)
                    embed.add_field(name="노래 길이", value=f"`{str(datetime.timedelta(seconds=next_song.length))}`", inline=True)
                    embed.add_field(name="볼륨", value=f"`100%`", inline=True)
                    embed.add_field(name="호스트", value=self.admin.mention, inline=True)
                    embed.add_field(name=interaction.message.embeds[0].fields[3].name, value=interaction.message.embeds[0].fields[3].value, inline=True)
                    embed.add_field(name=interaction.message.embeds[0].fields[4].name, value=interaction.message.embeds[0].fields[4].value, inline=True)
                    embed.add_field(name=interaction.message.embeds[0].fields[5].name, value=interaction.message.embeds[0].fields[5].value, inline=True)
                    img = f"https://img.youtube.com/vi/{next_song.identifier}/mqdefault.jpg"
                    embed.set_image(url=img)
                    print(next_song)
                    print(next_song.uri)
                    hoster = interaction.user
                    print(f"Host : {hoster} ({hoster.id})")
                    print("================================================")
                    await interaction.message.edit(embed=embed)
                    return await interaction.response.send_message(f"노래가 스킵되었어요! 새로 재생중인 음악 : `{next_song}`", delete_after=3)
            except:
                return await interaction.response.send_message(f"재생 목록이 비었어요!", delete_after=3)
        else:
            await interaction.response.send_message(embed=Embed(title="자신의것을 사용해주세요!", color=func.embed), ephemeral=True)

    @nextcord.ui.button(label="반복", style=nextcord.ButtonStyle.red, emoji=emojis.musicRepeat())
    async def repeat(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.admin == interaction.user or self.admin == None:
            vc: nextwave.Player = interaction.guild.voice_client
            if musicType.music_loop_type == 1:
                vc.loop ^= True
                musicType.music_loop_type = 2
                button.style = nextcord.ButtonStyle.green
                embed = nextcord.Embed(title=interaction.message.embeds[0].title, color=interaction.message.embeds[0].color)
                embed.add_field(name=interaction.message.embeds[0].fields[0].name, value=interaction.message.embeds[0].fields[0].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[1].name, value=interaction.message.embeds[0].fields[1].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[2].name, value=interaction.message.embeds[0].fields[2].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[3].name, value="`전체반복`", inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[4].name, value=interaction.message.embeds[0].fields[4].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[5].name, value=interaction.message.embeds[0].fields[5].value, inline=True)
                embed.set_image(url=interaction.message.embeds[0].image.url)
                await interaction.message.edit(embed=embed, view=self)
                return await interaction.response.send_message("현재 플레이리스트를 반복재생합니다", delete_after=3)
            elif musicType.music_loop_type == 2:
                vc.loop ^= True
                musicType.music_loop_type = 3
                button.style = nextcord.ButtonStyle.blurple
                embed = nextcord.Embed(title=interaction.message.embeds[0].title, color=interaction.message.embeds[0].color)
                embed.add_field(name=interaction.message.embeds[0].fields[0].name, value=interaction.message.embeds[0].fields[0].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[1].name, value=interaction.message.embeds[0].fields[1].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[2].name, value=interaction.message.embeds[0].fields[2].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[3].name, value="`한곡반복`", inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[4].name, value=interaction.message.embeds[0].fields[4].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[5].name, value=interaction.message.embeds[0].fields[5].value, inline=True)
                embed.set_image(url=interaction.message.embeds[0].image.url)
                await interaction.message.edit(embed=embed, view=self)
                return await interaction.response.send_message("현재 곡을 반복재생합니다", delete_after=3)
            else:
                vc.loop ^= False
                musicType.music_loop_type = 1
                button.style = nextcord.ButtonStyle.red
                embed = nextcord.Embed(title=interaction.message.embeds[0].title, color=interaction.message.embeds[0].color)
                embed.add_field(name=interaction.message.embeds[0].fields[0].name, value=interaction.message.embeds[0].fields[0].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[1].name, value=interaction.message.embeds[0].fields[1].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[2].name, value=interaction.message.embeds[0].fields[2].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[3].name, value="`꺼짐`", inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[4].name, value=interaction.message.embeds[0].fields[4].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[5].name, value=interaction.message.embeds[0].fields[5].value, inline=True)
                embed.set_image(url=interaction.message.embeds[0].image.url)
                await interaction.message.edit(embed=embed, view=self)
                return await interaction.response.send_message("반복재생을 비활성화 하였습니다", delete_after=3)
        else:
            await interaction.response.send_message(embed=Embed(title="자신의것을 사용해주세요!", color=func.embed), ephemeral=True)

    @nextcord.ui.button(label="셔플", style=nextcord.ButtonStyle.red, emoji=emojis.musicShuffle())
    async def shuffle(self, button: nextcord.ui.Button, interaction : nextcord.Interaction):
        if self.admin == interaction.user or self.admin == None:
            if musicType.music_shuffle is False:
                musicType.music_shuffle = True
                button.style = nextcord.ButtonStyle.green
                embed = nextcord.Embed(title=interaction.message.embeds[0].title, color=interaction.message.embeds[0].color)
                embed.add_field(name=interaction.message.embeds[0].fields[0].name, value=interaction.message.embeds[0].fields[0].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[1].name, value=interaction.message.embeds[0].fields[1].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[2].name, value=interaction.message.embeds[0].fields[2].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[3].name, value=interaction.message.embeds[0].fields[3].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[4].name, value="`켜짐`", inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[5].name, value=interaction.message.embeds[0].fields[5].value, inline=True)
                embed.set_image(url=interaction.message.embeds[0].image.url)
                await interaction.message.edit(embed=embed, view = self)
                return await interaction.response.send_message("셔플 재생을 활성화 하였습니다", delete_after=3)
            elif musicType.music_shuffle is True:
                musicType.music_shuffle = False
                button.style = nextcord.ButtonStyle.red
                embed = nextcord.Embed(title=interaction.message.embeds[0].title, color=interaction.message.embeds[0].color)
                embed.add_field(name=interaction.message.embeds[0].fields[0].name, value=interaction.message.embeds[0].fields[0].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[1].name, value=interaction.message.embeds[0].fields[1].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[2].name, value=interaction.message.embeds[0].fields[2].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[3].name, value=interaction.message.embeds[0].fields[3].value, inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[4].name, value="`꺼짐`", inline=True)
                embed.add_field(name=interaction.message.embeds[0].fields[5].name, value=interaction.message.embeds[0].fields[5].value, inline=True)
                embed.set_image(url=interaction.message.embeds[0].image.url)
                await interaction.message.edit(embed=embed, view = self)
                return await interaction.response.send_message("셔플 재생을 비활성화 하였습니다", delete_after=3)
        else:
            await interaction.response.send_message(embed=Embed(title="자신의것을 사용해주세요!", color=func.embed), ephemeral=True)

    @nextcord.ui.button(label="플레이리스트", style=nextcord.ButtonStyle.gray, emoji=emojis.musicPlaylist())
    async def playlist(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.admin == interaction.user or self.admin == None:
            vc: nextwave.Player = interaction.guild.voice_client
            playlist = vc.queue.copy()
            return await interaction.response.send_message(f"{playlist}", ephemeral=True)
        else:   
            await interaction.response.send_message(embed=Embed(title="자신의것을 사용해주세요!", color=func.embed), ephemeral=True)