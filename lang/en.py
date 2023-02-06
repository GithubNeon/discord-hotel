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

            description = f"{emojis.good()} | {len(self.yesALL)} vote\n{emojis.bad()} | {len(self.noALL)} vote"
            embed = nextcord.Embed(
                title=f"📋 topic : {self.title}", description=description, color=0x2f3136)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(f"You already voted for {emojis.good()}", ephemeral=True)

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

            description = f"{emojis.good()} | {len(self.yesALL)} vote\n{emojis.bad()} | {len(self.noALL)} vote"
            embed = nextcord.Embed(
                title=f"📋 topic : {self.title}", description=description, color=0x2f3136)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(f"You already voted for {emojis.bad()}", ephemeral=True)

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

            description = f"**final result**\n{emojis.good()} | {len(self.yesALL)} vote\n{emojis.bad()} | {len(self.noALL)} vote"
            embed = nextcord.Embed(title=f"📋 topic : {self.title}", description=description, color=0x2f3136).set_footer(
                text="The voting has ended")
            await interaction.response.edit_message(embed=embed, view=self)
            del self
        else:
            await interaction.response.send_message("Only the person who created the vote can end it", ephemeral=True)


class vote_modal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__("vote")

        self.val1 = None
        self.val2 = None
        self.val3 = None
        self.val4 = None
        self.val5 = None

        self.votetitle = nextcord.ui.TextInput(
            label="topic", style=TextInputStyle.short, placeholder="Developer Neoni is")
        self.voteinput = nextcord.ui.TextInput(
            label="vote", style=TextInputStyle.paragraph, placeholder="genius!\nstupid!")
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
            await interaction.response.send_message("Please retry again")
        else:
            embed = nextcord.Embed(title=f"📋 topic : {self.votetitle.value}",
                                   description=f"{emojis.one()} {a[0]} | 0 vote\n\n{emojis.two()} {a[1]} | 0 vote\n\n{emojis.three()} {a[2]} | 0 vote\n\n{emojis.four()} {a[3]} | 0 vote\n\n{emojis.five()} {a[4]} | 0 vote", color=0x2f3136)
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

            description = f"{emojis.one()} {self.vone} | {len(self.voting1)} vote\n\n{emojis.two()} {self.vtwo} | {len(self.voting2)} vote\n\n{emojis.three()} {self.vthree} | {len(self.voting3)} vote\n\n{emojis.four()} {self.vfour} | {len(self.voting4)} vote\n\n{emojis.five()} {self.vfive} | {len(self.voting5)} vote"
            embed = nextcord.Embed(
                title=f"📋 topic : {self.title}", description=description, color=0x2f3136)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(f"You already voted for {emojis.one()}", ephemeral=True)

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

            description = f"{emojis.one()} {self.vone} | {len(self.voting1)} vote\n\n{emojis.two()} {self.vtwo} | {len(self.voting2)} vote\n\n{emojis.three()} {self.vthree} | {len(self.voting3)} vote\n\n{emojis.four()} {self.vfour} | {len(self.voting4)} vote\n\n{emojis.five()} {self.vfive} | {len(self.voting5)} vote"
            embed = nextcord.Embed(
                title=f"📋 topic : {self.title}", description=description, color=0x2f3136)
            await interaction.response.edit_message(embed=embed)
        else:
            await interaction.response.send_message(f"You already voted for {emojis.two()}", ephemeral=True)

    @nextcord.ui.button(emoji=f"{emojis.three()}", style=nextcord.ButtonStyle.blurple)
    async def voting3(self, button: nextcord.Button, interaction: nextcord.Interaction):
        if self.vthree is None:
            return await interaction.response.send_message("Number 3 is currently inactive\nDoes not affect voting", ephemeral=True)
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

                description = f"{emojis.one()} {self.vone} | {len(self.voting1)} vote\n\n{emojis.two()} {self.vtwo} | {len(self.voting2)} vote\n\n{emojis.three()} {self.vthree} | {len(self.voting3)} vote\n\n{emojis.four()} {self.vfour} | {len(self.voting4)} vote\n\n{emojis.five()} {self.vfive} | {len(self.voting5)} vote"
                embed = nextcord.Embed(
                    title=f"📋 topic : {self.title}", description=description, color=0x2f3136)
                await interaction.response.edit_message(embed=embed)
            else:
                await interaction.response.send_message(f"You already voted for {emojis.three()}", ephemeral=True)

    @nextcord.ui.button(emoji=f"{emojis.four()}", style=nextcord.ButtonStyle.blurple)
    async def voting4(self, button: nextcord.Button, interaction: nextcord.Interaction):
        if self.vfour is None:
            return await interaction.response.send_message("Number 4 is currently inactive\nDoes not affect voting", ephemeral=True)
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

                description = f"{emojis.one()} {self.vone} | {len(self.voting1)} vote\n\n{emojis.two()} {self.vtwo} | {len(self.voting2)} vote\n\n{emojis.three()} {self.vthree} | {len(self.voting3)} vote\n\n{emojis.four()} {self.vfour} | {len(self.voting4)} vote\n\n{emojis.five()} {self.vfive} | {len(self.voting5)} vote"
                embed = nextcord.Embed(
                    title=f"📋 topic : {self.title}", description=description, color=0x2f3136)
                await interaction.response.edit_message(embed=embed)
            else:
                await interaction.response.send_message(f"You already voted for {emojis.four()}", ephemeral=True)

    @nextcord.ui.button(emoji=f"{emojis.five()}", style=nextcord.ButtonStyle.blurple)
    async def voting5(self, button: nextcord.Button, interaction: nextcord.Interaction):
        if self.vfive is None:
            return await interaction.response.send_message("Number 5 is currently inactive\nDoes not affect voting", ephemeral=True)
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

                description = f"{emojis.one()} {self.vone} | {len(self.voting1)} vote\n\n{emojis.two()} {self.vtwo} | {len(self.voting2)} vote\n\n{emojis.three()} {self.vthree} | {len(self.voting3)} vote\n\n{emojis.four()} {self.vfour} | {len(self.voting4)} vote\n\n{emojis.five()} {self.vfive} | {len(self.voting5)} vote"
                embed = nextcord.Embed(
                    title=f"📋 topic : {self.title}", description=description, color=0x2f3136)
                await interaction.response.edit_message(embed=embed)
            else:
                await interaction.response.send_message(f"You already voted for {emojis.five()}", ephemeral=True)

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

            description = f"**final result**\n\n{emojis.one()} {self.vone} | {len(self.voting1)} vote\n\n{emojis.two()} {self.vtwo} | {len(self.voting2)} vote\n\n{emojis.three()} {self.vthree} | {len(self.voting3)} vote\n\n{emojis.four()} {self.vfour} | {len(self.voting4)} vote\n\n{emojis.five()} {self.vfive} | {len(self.voting5)} vote"
            embed = nextcord.Embed(title=f"📋 topic : {self.title}", description=description, color=0x2f3136).set_footer(
                text="The voting has ended")
            await interaction.response.edit_message(embed=embed, view=self)
            del self
        else:
            await interaction.response.send_message("Only the person who created the vote can end it", ephemeral=True)


class help_menu(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Permissions commands", emoji=emojis.settings()),
            nextcord.SelectOption(label="Utility commands", emoji=emojis.idcard()),
            nextcord.SelectOption(label="Music commands", emoji=emojis.music()),
            nextcord.SelectOption(label="Developer commands", emoji=emojis.developer()),
            nextcord.SelectOption(label="Help commands", emoji=emojis.help())
        ]
        super().__init__(placeholder="Commands", options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == "Permissions commands":
            embed = nextcord.Embed(title="Permissions category", color=func.embed)
            embed.add_field(name="• Permissions commands list", value="""
```py
@ Permissions commands is admins can use it.

" /kick <user> "
# ex) : /kick Neoni

" /ban <user> "
# ex) : /ban Neoni

" /timeout <user> <time> <unit>"
# ex) : /timeout Neoni 1 h

" /clear <count> "
# ex) : /clear 10
```""", inline=False)
            await interaction.message.edit(embed=embed, view=help_menu_view())
        elif self.values[0] == "Utility commands":
            embed = nextcord.Embed(title="Utility category", color=func.embed)
            embed.add_field(name="• Utility commands list", value="""
```py
" /server_info "
# ex) : /server_info

" /user "
# ex) : /user

" /vote "
# ex) : /vote

" /yes_no_vote <topic> "
# ex) : /yes_no_vote Neoni is genius
```""", inline=False)
            await interaction.message.edit(embed=embed, view=help_menu_view())
        elif self.values[0] == "Music commands":
            embed = nextcord.Embed(title="Music category", color=func.embed)
            embed.add_field(name="• Music commands list", value="""
```py
" /join "
# ex) : /join

" /leave "
# ex) : /leave
```""", inline=False)
            await interaction.message.edit(embed=embed, view=help_menu_view())
        elif self.values[0] == "Developer commands":
            embed = nextcord.Embed(title="Dev category", color=func.embed)
            embed.add_field(name="• Dev commands list", value="""
```py
" /developer "
# ex) : /developer

" /ping "
# ex) : /ping
```""", inline=False)
            await interaction.message.edit(embed=embed, view=help_menu_view())
        elif self.values[0] == "Help commands":
            embed = nextcord.Embed(title="Help category", color=func.embed)
            embed.add_field(name="• Help commands list", value="""
```py
" /help "
# ex) : /help
```""", inline=False)
            await interaction.message.edit(embed=embed, view=help_menu_view())


class help_menu_view(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(help_menu())
