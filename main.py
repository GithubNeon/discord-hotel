import os
from dotenv import load_dotenv

import nextcord

from nextcord import *
from nextcord.ext import commands, tasks

from itertools import cycle

import nextwave

import json

import func
from func import musicSearch, emojis

import math
import time

import datetime
from datetime import timedelta

import config
from config import module, musicType

import music
from music import musicClass

# music loop type 1 none

# music loop type 2 all repeat

# music loop type 3 single repeat

intents = nextcord.Intents.all()

bot = commands.Bot(intents=intents)

load_dotenv()
token = os.getenv("TOKEN")

for filename in os.listdir("./server"):
    if filename.endswith(".py"):
        bot.load_extension(f"server.{filename[:-3]}")
for filename in os.listdir("./util"):
    if filename.endswith(".py"):
        bot.load_extension(f"util.{filename[:-3]}")

@bot.event
async def on_ready():
    status = cycle(["서버 관리하는", f"{len(bot.users)}명과 함께", "Dev. 네오니"])
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    change_status.start(status)
    bot.loop.create_task(node_connect())

@tasks.loop(seconds=5)
async def change_status(status):
    await bot.change_presence(activity=nextcord.Streaming(name=next(status), url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

async def node_connect():
    await bot.wait_until_ready()
    await nextwave.NodePool.create_node(bot=bot, host="localhost", port=2333, password="youshallnotpass", region="ko", identifier="default-node")

async def check_voice(user : nextcord.Member, vc: int):
    try: user.voice.channel
    except: return False
    ch = bot.get_channel(vc)
    for i in ch.members:
        if i.id == user.id:
            return True
        else:
            pass
    return False

@bot.event
async def on_nextwave_node_ready(node : nextwave.Node):
    print(f"{node.identifier} 실행됨")
    print("================================================")

@bot.event
async def on_voice_state_update(member, before=None, after=None):
    voice_state = member.guild.voice_client

    vc : nextwave.Player = voice_state

    if voice_state is None:
        return 

    if len(voice_state.channel.members) == 1:
        await vc.pause()
    
    elif len(voice_state.channel.members) > 1:
        await vc.resume()

@bot.event
async def on_nextwave_track_end(interaction : nextcord.Interaction, track : nextwave.Track, reason):
    vc: nextwave.Player = interaction.guild.voice_client
    try:
        if musicType.music_loop_type == 3:
            return await vc.play(track)
        elif musicType.music_loop_type == 2:
            if musicType.song_number == (len(musicType.playlist)):
                musicType.song_number = 1
                await vc.play(musicType.playlist[musicType.song_number - 1])
                embed = nextcord.Embed(title=f"{musicType.playlist[musicType.song_number - 1]}", color=func.embed)
                embed.add_field(name="노래 길이", value=f"`{str(datetime.timedelta(seconds=musicType.playlist[musicType.song_number - 1].length))}`", inline=True)
                embed.add_field(name="볼륨", value=f"`100%`", inline=True)
                embed.add_field(name="호스트", value=interaction.user.mention, inline=True)
                embed.add_field(name="반복", value="`전체반복`", inline=True)
                embed.add_field(name="셔플", value="`꺼짐`", inline=True)
                embed.add_field(name="재생 채널", value=f"<#{interaction.user.voice.channel.id}>", inline=True)
                img = f"https://img.youtube.com/vi/{musicType.playlist[musicType.song_number - 1].identifier}/mqdefault.jpg"
                embed.set_image(url=img)
                print(musicType.playlist[musicType.song_number - 1])
                print(musicType.playlist[musicType.song_number - 1].uri)
                hoster = interaction.user
                print(f"Host : {hoster} ({hoster.id})")
                print("================================================")
                await interaction.message.edit(embed=embed, view=musicClass.MusicPlayer(vc=vc, musicArray=musicType.playlist[musicType.song_number - 1], q=musicType.playlist[musicType.song_number - 1], admin=interaction.user.mention))
            else:
                musicType.song_number =+ 1
                await vc.play(musicType.playlist[musicType.song_number - 1])
                embed = nextcord.Embed(title=f"{musicType.playlist[musicType.song_number - 1]}", color=func.embed)
                embed.add_field(name="노래 길이", value=f"`{str(datetime.timedelta(seconds=musicType.playlist[musicType.song_number - 1].length))}`", inline=True)
                embed.add_field(name="볼륨", value=f"`100%`", inline=True)
                embed.add_field(name="호스트", value=interaction.user.mention, inline=True)
                embed.add_field(name="반복", value="`전체반복`", inline=True)
                embed.add_field(name="셔플", value="`꺼짐`", inline=True)
                embed.add_field(name="재생 채널", value=f"<#{interaction.user.voice.channel.id}>", inline=True)
                img = f"https://img.youtube.com/vi/{musicType.playlist[musicType.song_number - 1].identifier}/mqdefault.jpg"
                embed.set_image(url=img)
                print(musicType.playlist[musicType.song_number - 1])
                print(musicType.playlist[musicType.song_number - 1].uri)
                hoster = interaction.user
                print(f"Host : {hoster} ({hoster.id})")
                print("================================================")
                await interaction.message.edit(embed=embed, view=musicClass.MusicPlayer(vc=vc, musicArray=musicType.playlist[musicType.song_number - 1], q=musicType.playlist[musicType.song_number - 1], admin=interaction.user.mention))
        elif musicType.music_shuffle == True:
            shuffle_next_song = random.choice(musicType.playlist)
            await vc.play(shuffle_next_song)
            embed = nextcord.Embed(title=f"{shuffle_next_song}", color=func.embed)
            embed.add_field(name="노래 길이", value=f"`{str(datetime.timedelta(seconds=shuffle_next_song.length))}`", inline=True)
            embed.add_field(name="볼륨", value=f"`100%`", inline=True)
            embed.add_field(name="호스트", value=interaction.user.mention, inline=True)
            embed.add_field(name="반복", value="`꺼짐`", inline=True)
            embed.add_field(name="셔플", value="`켜짐`", inline=True)
            embed.add_field(name="재생 채널", value=f"<#{interaction.user.voice.channel.id}>", inline=True)
            img = f"https://img.youtube.com/vi/{shuffle_next_song.identifier}/mqdefault.jpg"
            embed.set_image(url=img)
            print(shuffle_next_song)
            print(shuffle_next_song.uri)
            hoster = interaction.user
            print(f"Host : {hoster} ({hoster.id})")
            print("================================================")
            await interaction.message.edit(embed=embed, view=musicClass.MusicPlayer(vc=vc, musicArray=shuffle_next_song, q=shuffle_next_song, admin=interaction.user.mention))
        else:
            del musicType.playlist[0]
            next_song = vc.queue.get()
            await vc.play(next_song)
            embed = nextcord.Embed(title=f"{next_song}", color=func.embed)
            embed.add_field(name="노래 길이", value=f"`{str(datetime.timedelta(seconds=next_song.length))}`", inline=True)
            embed.add_field(name="볼륨", value=f"`100%`", inline=True)
            embed.add_field(name="호스트", value=interaction.user.mention, inline=True)
            embed.add_field(name="반복", value="`꺼짐`", inline=True)
            embed.add_field(name="셔플", value="`꺼짐`", inline=True)
            embed.add_field(name="재생 채널", value=f"<#{interaction.user.voice.channel.id}>", inline=True)
            img = f"https://img.youtube.com/vi/{next_song.identifier}/mqdefault.jpg"
            embed.set_image(url=img)
            print(next_song)
            print(next_song.uri)
            hoster = interaction.user
            print(f"Host : {hoster} ({hoster.id})")
            print("================================================")
            await interaction.message.edit(embed=embed, view=musicClass.MusicPlayer(vc=vc, musicArray=next_song, q=next_song, admin=interaction.user.mention))
    except:
        embed = nextcord.Embed(title=f"음악재생을 마칩니다.", color=func.embed)
        await interaction.message.edit(embed=embed, delete_after=3)
        await vc.disconnect()
        vc.loop = False
        musicType.music_loop_type = 1
        musicType.playlist = []

@bot.event
async def on_message(message):
    if message.author.bot: return None
    message_content = message.content
    topic = message.channel.topic
    if topic is not None and "#discord-hotel music channel" in topic:
        await bot.process_commands(message)
        if message.content.startswith("!MUSIC SHUTDOWN"):
            vc: nextwave.Player = message.guild.voice_client
            try:
                await vc.stop()
                await vc.disconnect()
            except:
                return
            await message.channel.purge(limit=2)
            song_number = 1
            musicType.music_loop_type = 1
            musicType.playlist = []
            musicType.music_shuffle = False
            await message.channel.send("음악을 강제 종료하였습니다", delete_after=3)
        elif message.content.startswith("!MUSIC SETUP"):
            await message.delete()
            await message.channel.purge()
            await message.channel.send(embed=Embed(title="🎶 재생하고 싶은 노래 제목이나 링크를 입력해주세요 🎶", color=func.embed))
        elif message.content == message_content:
            func.musicSearch(user=message.author, text=message_content).read()

            try:
                message.author.voice.channel
            except:
                await message.delete()
                await message.channel.send(embed=Embed(title="엥...?", description="음성채널에 먼저 들어가주세요!", color=func.embed), delete_after=3)
                return

            t = 0
            try:
                vc: nextwave.Player = await message.author.voice.channel.connect(cls=nextwave.Player)
            except:
                    for voiceChannel in message.guild.voice_channels:
                        if (message.author in voiceChannel.members):
                            t = 1
                            if (len(voiceChannel.members) <= 2):
                                vc: nextwave.Player = message.guild.voice_client
                                break
                    if (t == 0):
                        vc: nextwave.Player = message.guild.voice_client

            vc.loop = False

            if await check_voice(user=message.author, vc=message.author.voice.channel.id) is False:
                return await message.channel.send("같은 음성채널에 있어야 봇을 컨트롤 할 수 있어요!", ephemeral=True)

            array = await nextwave.YouTubeTrack.search(query=message_content, return_first=False)
            try:
                MUSIC : nextwave.Track = array[0]
            except IndexError:
                await message.delete()
                await message.channel.send("해당 노래를 찾지 못했습니다")
            if vc.volume == 100:
                await vc.set_volume(50)
            if vc.queue.is_empty and not vc.is_playing():
                await message.delete()
                await vc.play(MUSIC)
                embed = nextcord.Embed(title=f"{MUSIC}", color=func.embed)
                embed.add_field(name="노래 길이", value=f"`{str(datetime.timedelta(seconds=MUSIC.length))}`", inline=True)
                embed.add_field(name="볼륨", value=f"`100%`", inline=True)
                embed.add_field(name="호스트", value=message.author.mention, inline=True)
                embed.add_field(name="반복", value="`꺼짐`", inline=True)
                embed.add_field(name="셔플", value="`꺼짐`", inline=True)
                embed.add_field(name="재생 채널", value=f"<#{message.author.voice.channel.id}>", inline=True)
                img = f"https://img.youtube.com/vi/{MUSIC.identifier}/mqdefault.jpg"
                embed.set_image(url=img)
                print(MUSIC)
                print(MUSIC.uri)
                hoster = message.author
                print(f"Host : {hoster} ({hoster.id})")
                print("================================================")
                musicType.playlist.append(array[0])
                await message.channel.send(embed=embed, view=musicClass.MusicPlayer(vc=vc, musicArray=array, q=message_content, admin=message.author))
            elif vc.is_playing():
                await message.delete()
                await vc.queue.put_wait(array[0])
                musicType.playlist.append(array[0])
                await message.channel.send(f"`{array[0]}`을(를) 찾았습니다", delete_after=3)
            else:
                await message.delete()
                return await message.channel.send(embed=Embed(title=f"당신은 호스트가 아닙니다.", color=func.embed), delete_after=3)
    else:
        return

bot.run(token)