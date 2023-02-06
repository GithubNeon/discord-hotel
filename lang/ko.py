import asyncio

import nextcord

from nextcord import *
from nextcord.ext import commands

import nextwave

import func
from func import emojis

import time
from time import sleep

import humanfriendly

# class giveaway_modal(nextcord.ui.Modal):
#     def __init__(self):
#         super().__init__("Giveaway")
#         self.duration = nextcord.ui.TextInput(label="기간", placeholder="예시 : 10시간", style=TextInputStyle.short)
#         self.winner = nextcord.ui.TextInput(label="우승자 수", placeholder="1", style=TextInputStyle.short)
#         self.prize = nextcord.ui.TextInput(label="상품", style=TextInputStyle.short)
#         self.description = nextcord.ui.TextInput(label="Description", style=TextInputStyle.paragraph, required=False)

#         self.add_item(self.duration)
#         self.add_item(self.winner)
#         self.add_item(self.prize)
#         self.add_item(self.description)

#     async def callback(self, interaction: nextcord.Interaction):

#         if self.description.value == "":
#             description = "No description"
#         else:
#             description = self.description.value

#         try:
#             int(self.duration.value)
#             시간 = str(self.duration.value)+"초"
#         except:
#             pass
#         기간 = str(self.duration.value).replace("초","s").replace("분","m").replace("시간","h").replace("일","d").replace("년","y")
#         times = humanfriendly.parse_timespan(기간)
#         timer = str(times).replace(".0", "")
#         print(timer)

#         max_time = 2419200.0
#         if times > max_time:
#             times = max_time
#             시간 = "28일"

#         while timer != 0:
#             timer = timer=-1
#             await asyncio.sleep(1)

#         embed = nextcord.Embed(title = f"**{self.prize.value}**", description = f"{description}\n\nEnds : <t:{time.time}:R>\nHost : {interaction.user.mention}\nEntries : **0**\nwinners : {self.winner.value}", color = func.embed)

#         await interaction.response.send_message(embed=embed, view=giveaway_button(title=self.prize.value, description=description, duration=timer))

# class giveaway_button(nextcord.ui.Button):
#     def __init__(self, title, description, duration):
#         super().__init__()
#         self.title = title
#         self.description = description
#         self.duration = duration
#         self.entries = []
#         self.winners = []

#     @nextcord.ui.button(emoji="🎉", style=nextcord.ButtonStyle.blurple)
#     async def giveaways(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
#         if ((interaction.user.id in self.entries) == False):
#             if self.duration != 0:
#                 try:
#                     self.entries.append(interaction.user.id)
#                 except:
#                     pass
#             elif self.duration == 0:
#                 for i in range(self.duration):
#                     result = random.choice(self.entries)
#                     self.winners.append(result)
#                 embed = nextcord.Embed(title = self.title, description = f"{self.description}\n\nEnded : <t:{time.time}:R>\nHost : {self.interaction.user.mention}\nEntries : **{len(self.entries)}**\nwinners : {self.winners}", color = func.embed)
#         else:
#             await interaction.response.send_message("You have already entered this giveaway!", ephemeral=True)


class yes_no_vote_button(nextcord.ui.View):
    def __init__(self, title=None, admin: nextcord.Member = None):
        super().__init__(timeout=None)
        self.title = title
        self.admin = admin
        self.yesALL = []
        self.noALL = []

    @nextcord.ui.button(emoji=f"{emojis.good()}", style=nextcord.ButtonStyle.green)
    async def yes(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if ((interaction.user.id in self.yesALL) == False):
            try:
                self.noALL.remove(interaction.user.id)
            except:
                pass
            try:
                self.yesALL.append(interaction.user.id)
            except:
                pass

            description = f"{emojis.good()} | {len(self.yesALL)}표\n{emojis.bad()} | {len(self.noALL)}표"
            embed = nextcord.Embed(
                title=f"📋 투표주제 : {self.title}", description=description, color=0x2f3136)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(f"이미 {emojis.good()}에 투표를 하였습니다", ephemeral=True)

    @nextcord.ui.button(emoji=f"{emojis.bad()}", style=nextcord.ButtonStyle.red)
    async def no(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if ((interaction.user.id in self.noALL) == False):
            try:
                self.noALL.append(interaction.user.id)
            except:
                pass
            try:
                self.yesALL.remove(interaction.user.id)
            except:
                pass

            description = f"{emojis.good()} | {len(self.yesALL)}표\n{emojis.bad()} | {len(self.noALL)}표"
            embed = nextcord.Embed(
                title=f"📋 투표주제 : {self.title}", description=description, color=0x2f3136)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(f"이미 {emojis.bad()}에 투표를 하였습니다", ephemeral=True)

    @nextcord.ui.button(emoji=f"{emojis.lock()}", style=nextcord.ButtonStyle.gray)
    async def end(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user == self.admin:
            self.clear_items()
            self.add_item(nextcord.ui.Button(
                emoji=f"{emojis.good()} ", style=nextcord.ButtonStyle.green, disabled=True))
            self.add_item(nextcord.ui.Button(
                emoji=f"{emojis.bad()}", style=nextcord.ButtonStyle.red, disabled=True))
            self.add_item(nextcord.ui.Button(
                emoji=f"{emojis.lock()}", style=nextcord.ButtonStyle.gray, disabled=True))

            description = f"**최종 결과**\n{emojis.good()} | {len(self.yesALL)}표\n{emojis.bad()} | {len(self.noALL)}표"
            embed = nextcord.Embed(
                title=f"📋 투표주제 : {self.title}", description=description, color=0x2f3136).set_footer(text="투표가 종료되었습니다")
            await interaction.response.edit_message(embed=embed, view=self)
            del self
        else:
            await interaction.response.send_message("투표를 만든사람만 끝낼수 있습니다", ephemeral=True)

class vote_modal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("투표")

        self.val1 = None
        self.val2 = None
        self.val3 = None
        self.val4 = None
        self.val5 = None

        self.votetitle = nextcord.ui.TextInput(
            label="투표 제목을 적어주세요", style=TextInputStyle.short, placeholder="개발자 네오니는?")
        self.voteinput = nextcord.ui.TextInput(
            label="투표 항목을 적어주세요", style=TextInputStyle.paragraph, placeholder="천재임\n멍청이임")
        self.add_item(self.votetitle)
        self.add_item(self.voteinput)

    async def callback(self, interaction: nextcord.Interaction):
        a = ["", "", "", "", ""]

        self.val = self.children[1].value
        char = self.val.split("\n")

        try:
            a[0] = char[0]
        except IndexError:
            a[0] = None
        try:
            a[1] = char[1]
        except IndexError:
            a[1] = None
        try:
            a[2] = char[2]
        except IndexError:
            a[2] = None
        try:
            a[3] = char[3]
        except IndexError:
            a[3] = None
        try:
            a[4] = char[4]
        except IndexError:
            a[4] = None

        if a[1] is None or a[1] == "" or a[2] == "" or a[3] == "" or a[4] == "":
            await interaction.response.send_message("다시 시도해주세요")
        else:
            embed = nextcord.Embed(
                title=f"📋 투표주제 : {self.votetitle.value}", description=f"{emojis.one()} {a[0]} | 0표\n\n{emojis.two()} {a[1]} | 0표\n\n{emojis.three()} {a[2]} | 0표\n\n{emojis.four()} {a[3]} | 0표\n\n{emojis.five()} {a[4]} | 0표", color=0x2f3136)
            await interaction.response.send_message(embed=embed, view=vote_button(title=self.votetitle.value, admin=interaction.user, vone=a[0], vtwo=a[1], vthree=a[2], vfour=a[3], vfive=a[4]))


class vote_button(nextcord.ui.View):
    def __init__(self, title, admin: nextcord.Member, vone, vtwo, vthree, vfour, vfive):
        super().__init__(timeout=None)
        self.title = title
        self.admin = admin
        self.vone = vone
        self.vtwo = vtwo
        self.vthree = vthree
        self.vfour = vfour
        self.vfive = vfive
        self.voting1 = []
        self.voting2 = []
        self.voting3 = []
        self.voting4 = []
        self.voting5 = []

    @nextcord.ui.button(emoji=f"{emojis.one()}", style=nextcord.ButtonStyle.blurple)
    async def voting1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if ((interaction.user.id in self.voting1) == False):
            try:
                self.voting1.append(interaction.user.id)
            except:
                pass
            try:
                self.voting2.remove(interaction.user.id)
            except:
                pass
            try:
                self.voting3.remove(interaction.user.id)
            except:
                pass
            try:
                self.voting4.remove(interaction.user.id)
            except:
                pass
            try:
                self.voting5.remove(interaction.user.id)
            except:
                pass

            description = f"{emojis.one()} {self.vone} | {len(self.voting1)}표\n\n{emojis.two()} {self.vtwo} | {len(self.voting2)}표\n\n{emojis.three()} {self.vthree} | {len(self.voting3)}표\n\n{emojis.four()} {self.vfour} | {len(self.voting4)}표\n\n{emojis.five()} {self.vfive} | {len(self.voting5)}표"
            embed = nextcord.Embed(
                title=f"📋 투표주제 : {self.title}", description=description, color=0x2f3136)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(f"이미 {emojis.one()}에 투표를 하였습니다", ephemeral=True)

    @nextcord.ui.button(emoji=f"{emojis.two()}", style=nextcord.ButtonStyle.blurple)
    async def voting2(self, button: nextcord.Button, interaction: nextcord.Interaction):
        if ((interaction.user.id in self.voting2) == False):
            try:
                self.voting2.append(interaction.user.id)
            except:
                pass
            try:
                self.voting1.remove(interaction.user.id)
            except:
                pass
            try:
                self.voting3.remove(interaction.user.id)
            except:
                pass
            try:
                self.voting4.remove(interaction.user.id)
            except:
                pass
            try:
                self.voting5.remove(interaction.user.id)
            except:
                pass

            description = f"{emojis.one()} {self.vone} | {len(self.voting1)}표\n\n{emojis.two()} {self.vtwo} | {len(self.voting2)}표\n\n{emojis.three()} {self.vthree} | {len(self.voting3)}표\n\n{emojis.four()} {self.vfour} | {len(self.voting4)}표\n\n{emojis.five()} {self.vfive} | {len(self.voting5)}표"
            embed = nextcord.Embed(
                title=f"📋 투표주제 : {self.title}", description=description, color=0x2f3136)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(f"이미 {emojis.two()}에 투표를 하였습니다", ephemeral=True)

    @nextcord.ui.button(emoji=f"{emojis.three()}", style=nextcord.ButtonStyle.blurple)
    async def voting3(self, button: nextcord.Button, interaction: nextcord.Interaction):
        if self.vthree is None:
            return await interaction.response.send_message("현재 3번은 비활성화 상태입니다\n투표에 영향을 주진 않습니다", ephemeral=True)
        else:
            if ((interaction.user.id in self.voting3) == False):
                try:
                    self.voting3.append(interaction.user.id)
                except:
                    pass
                try:
                    self.voting1.remove(interaction.user.id)
                except:
                    pass
                try:
                    self.voting2.remove(interaction.user.id)
                except:
                    pass
                try:
                    self.voting4.remove(interaction.user.id)
                except:
                    pass
                try:
                    self.voting5.remove(interaction.user.id)
                except:
                    pass

                description = f"{emojis.one()} {self.vone} | {len(self.voting1)}표\n\n{emojis.two()} {self.vtwo} | {len(self.voting2)}표\n\n{emojis.three()} {self.vthree} | {len(self.voting3)}표\n\n{emojis.four()} {self.vfour} | {len(self.voting4)}표\n\n{emojis.five()} {self.vfive} | {len(self.voting5)}표"
                embed = nextcord.Embed(
                    title=f"📋 투표주제 : {self.title}", description=description, color=0x2f3136)
                await interaction.response.edit_message(embed=embed)
            else:
                await interaction.response.send_message(f"이미 {emojis.three()}에 투표를 하였습니다", ephemeral=True)

    @nextcord.ui.button(emoji=f"{emojis.four()}", style=nextcord.ButtonStyle.blurple)
    async def voting4(self, button: nextcord.Button, interaction: nextcord.Interaction):
        if self.vfour is None:
            return await interaction.response.send_message("현재 4번은 비활성화 상태입니다\n투표에 영향을 주진 않습니다", ephemeral=True)
        else:
            if ((interaction.user.id in self.voting4) == False):
                try:
                    self.voting4.append(interaction.user.id)
                except:
                    pass
                try:
                    self.voting1.remove(interaction.user.id)
                except:
                    pass
                try:
                    self.voting2.remove(interaction.user.id)
                except:
                    pass
                try:
                    self.voting3.remove(interaction.user.id)
                except:
                    pass
                try:
                    self.voting5.remove(interaction.user.id)
                except:
                    pass

                description = f"{emojis.one()} {self.vone} | {len(self.voting1)}표\n\n{emojis.two()} {self.vtwo} | {len(self.voting2)}표\n\n{emojis.three()} {self.vthree} | {len(self.voting3)}표\n\n{emojis.four()} {self.vfour} | {len(self.voting4)}표\n\n{emojis.five()} {self.vfive} | {len(self.voting5)}표"
                embed = nextcord.Embed(
                    title=f"📋 투표주제 : {self.title}", description=description, color=0x2f3136)
                await interaction.response.edit_message(embed=embed)
            else:
                await interaction.response.send_message(f"이미 {emojis.four()}에 투표를 하였습니다", ephemeral=True)

    @nextcord.ui.button(emoji=f"{emojis.five()}", style=nextcord.ButtonStyle.blurple)
    async def voting5(self, button: nextcord.Button, interaction: nextcord.Interaction):
        if self.vfive is None:
            return await interaction.response.send_message("현재 5번은 비활성화 상태입니다\n투표에 영향을 주진 않습니다", ephemeral=True)
        else:
            if ((interaction.user.id in self.voting5) == False):
                try:
                    self.voting5.append(interaction.user.id)
                except:
                    pass
                try:
                    self.voting1.remove(interaction.user.id)
                except:
                    pass
                try:
                    self.voting2.remove(interaction.user.id)
                except:
                    pass
                try:
                    self.voting3.remove(interaction.user.id)
                except:
                    pass
                try:
                    self.voting4.remove(interaction.user.id)
                except:
                    pass

                description = f"{emojis.one()} {self.vone} | {len(self.voting1)}표\n\n{emojis.two()} {self.vtwo} | {len(self.voting2)}표\n\n{emojis.three()} {self.vthree} | {len(self.voting3)}표\n\n{emojis.four()} {self.vfour} | {len(self.voting4)}표\n\n{emojis.five()} {self.vfive} | {len(self.voting5)}표"
                embed = nextcord.Embed(
                    title=f"📋 투표주제 : {self.title}", description=description, color=0x2f3136)
                await interaction.response.edit_message(embed=embed)
            else:
                await interaction.response.send_message(f"이미 {emojis.five()}에 투표를 하였습니다", ephemeral=True)

    @nextcord.ui.button(emoji=f"{emojis.lock()}", style=nextcord.ButtonStyle.gray)
    async def end(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if interaction.user == self.admin:
            self.clear_items()
            self.add_item(nextcord.ui.Button(
                emoji=f"{emojis.one()}", style=nextcord.ButtonStyle.blurple, disabled=True))
            self.add_item(nextcord.ui.Button(
                emoji=f"{emojis.two()}", style=nextcord.ButtonStyle.blurple, disabled=True))
            self.add_item(nextcord.ui.Button(
                emoji=f"{emojis.three()}", style=nextcord.ButtonStyle.blurple, disabled=True))
            self.add_item(nextcord.ui.Button(
                emoji=f"{emojis.four()}", style=nextcord.ButtonStyle.blurple, disabled=True))
            self.add_item(nextcord.ui.Button(
                emoji=f"{emojis.five()}", style=nextcord.ButtonStyle.blurple, disabled=True))
            self.add_item(nextcord.ui.Button(
                emoji=f"{emojis.lock()}", style=nextcord.ButtonStyle.gray, disabled=True))

            description = f"**최종 결과**\n\n{emojis.one()} {self.vone} | {len(self.voting1)}표\n\n{emojis.two()} {self.vtwo} | {len(self.voting2)}표\n\n{emojis.three()} {self.vthree} | {len(self.voting3)}표\n\n{emojis.four()} {self.vfour} | {len(self.voting4)}표\n\n{emojis.five()} {self.vfive} | {len(self.voting5)}표"
            embed = nextcord.Embed(
                title=f"📋 투표주제 : {self.title}", description=description, color=0x2f3136).set_footer(text="투표가 종료되었습니다")
            await interaction.response.edit_message(embed=embed, view=self)
            del self
        else:
            await interaction.response.send_message("투표를 만든사람만 끝낼수 있습니다", ephemeral=True)


class help_menu(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="관리 명령어", emoji=emojis.settings()),
            nextcord.SelectOption(label="유틸리티", emoji=emojis.idcard()),
            nextcord.SelectOption(label="음악 명령어", emoji=emojis.music()),
            nextcord.SelectOption(label="개발자 명령어", emoji=emojis.developer()),
            nextcord.SelectOption(label="도움말", emoji=emojis.help())
        ]
        super().__init__(placeholder="명령어 메뉴", options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == "관리 명령어":
            embed = nextcord.Embed(title="서버관리 카테고리", color=func.embed)
            embed.add_field(name="• 서버관리 명령어 목록", value="""
```py
@ 관리명령어는 관리자만 사용할 수 있습니다.
@ 권한이 없을시 보이지 않습니다

" /추방 <멤버 선택> "
# 사용방법 : /추방 네오니

" /차단 <멤버 선택> "
# 사용방법 : /차단 네오니

" /타임아웃 <멤버 선택> <시간> <단위>"
# 사용방법 : /타임아웃 네오니 1 시간

" /청소 <삭제할 메세지 갯수> "
# 사용방법 : /청소 10
```""", inline=False)
            await interaction.message.edit(embed=embed, view=help_menu_view())
        elif self.values[0] == "유틸리티":
            embed = nextcord.Embed(title="유틸리티 카테고리", color=func.embed)
            embed.add_field(name="• 유틸리티 명령어 목록", value="""
```py
" /서버정보 "
# 사용방법 : /서버정보

" /내정보 "
# 사용방법 : /내정보

" /투표 "
# 사용방법 : /투표

" /찬반투표 <투표주제> "
# 사용방법 : /찬반투표 네오니천재
```""", inline=False)
            await interaction.message.edit(embed=embed, view=help_menu_view())
        elif self.values[0] == "음악 명령어":
            embed = nextcord.Embed(title="음악 카테고리", color=func.embed)
            embed.add_field(name="• 음악 명령어 목록", value="""
```py
" /join "
# 사용방법 : /join

" /leave "
# 사용방법 : /leave
```""", inline=False)
            await interaction.message.edit(embed=embed, view=help_menu_view())
        elif self.values[0] == "개발자 명령어":
            embed = nextcord.Embed(title="개발자 카테고리", color=func.embed)
            embed.add_field(name="• 개발자 명령어 목록", value="""
```py
" /개발자 "
# 사용방법 : /개발자

" /핑 "
# 사용방법 : /핑
```""", inline=False)
            await interaction.message.edit(embed=embed, view=help_menu_view())
        elif self.values[0] == "도움말":
            embed = nextcord.Embed(title="도움말 카테고리", color=func.embed)
            embed.add_field(name="• 도움말 명령어 목록", value="""
```py
" /명령어 "
# 사용방법 : /명령어
```""", inline=False)
            await interaction.message.edit(embed=embed, view=help_menu_view())


class help_menu_view(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(help_menu())
