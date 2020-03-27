import time
import json
import random
import math
import discord
import os
import sys
import sqlite3
import secrets
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
import asyncio
# Changes the directory
os.chdir('F:/IEE')

# Connects to the database
conn = sqlite3.connect("people.db")
c = conn.cursor()

def printl(string):
	prn = open("F:/IEE/output.txt", 'a')
	prn.write(f'\n{string}')
	prn.close()
	print(string)

# Mod Cog
class Moderator(commands.Cog, name="Moderator Commands"):
	def __init__(self, bot):
		self.bot = bot

	async def mod(ctx):
		# opens the modlist and then stores the data as a list
		modlist = open('F:/IEE/storage/modlist.txt', 'r')
		modlist = modlist.read().split('-')
		# author's id
		authorid = str(ctx.author.id)
		# Check if the person is in the modlist
		if authorid in modlist:
			return True
		else:
			return False

	async def blacklisted(ctx):
		blacklistedpeople = [600798393459146784]
		if int(ctx.author.id) in blacklistedpeople:
			return False
		else:
			return True

	@commands.command()
	@commands.is_owner()
	async def nuke(self, ctx):
		c.execute("DROP TABLE people")
		conn.commit()
		# Create a table if does not exist people
		c.execute("""CREATE TABLE IF NOT EXISTS people (
					id blob,
					coin real,
					bank real,
					bankmax real,
					server blob,
					inventory blob,
					mines blob
					)""")
		# commit
		conn.commit()
		await ctx.send('killed people')

	@commands.command()
	async def update(self, ctx):
		await ctx.send("Added command `smto`, send messages to the bot owner, as I left for a bit")

	@commands.command(aliases=['perms',])
	@commands.check(mod)
	async def permissions(self, ctx, member: discord.Member):
		perms = member.guild_permissions
		embed=discord.Embed(title="Perms")
		embed.set_author(name=str(member)[:-5],icon_url=member.avatar_url)
		for perm, value in perms:
			if value:
				embed.add_field(name=perm, value=True, inline=True)
			else:
				embed.add_field(name=perm, value=False, inline=True)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.check(mod)
	async def roles(self, ctx, person: discord.Member):
		await ctx.send(f"`{person.roles}`")

	# Adds a moderator
	@commands.command()
	@commands.check(mod)
	async def addmod(self, ctx, mod: discord.Member):
		# Silly random color
		color = random.randint(0, 0xFFFFFF)
		# opens the modlist and then stores the data as a list
		modlistr = open('F:/IEE/storage/modlist.txt', 'r')
		modlistlr = modlistr.read()
		modlistlr = modlistlr.split('-')
		# author's id
		authorid = mod.id
		# Check if the person is in the modlist, if so tell them they're in the modlist
		if str(authorid) in modlistlr:
			modlistr.close()
			# embed
			embed=discord.Embed(title="", color=color)
			embed.set_author(name=str(mod)[:-5],icon_url=mod.avatar_url)
			embed.add_field(name="Mod Already", value=f"They're Already a mod", inline=True)
			await ctx.send(embed=embed)
		else:
			modlistr.close()
			# opens modlist in write mode
			modlist = open('F:/IEE/storage/modlist.txt', 'a')
			modlist.write(f'-{mod.id}')
			modlist.close()
			# embed
			embed=discord.Embed(title="", color=color)
			embed.set_author(name=str(mod)[:-5],icon_url=mod.avatar_url)
			embed.add_field(name="Added", value=f"Added {str(mod)[:-5]}.", inline=True)
			await ctx.send(embed=embed)

	@commands.command()
	@commands.check(mod)
	async def revmod(self, ctx, mod: discord.Member):
		# Silly random color
		color = random.randint(0, 0xFFFFFF)
		# opens the modlist and then stores the data as a list
		modlistr = open('F:/IEE/storage/modlist.txt', 'r')
		modlistlr = modlistr.read()
		modlistlr = modlistlr.split('-')
		# author's id
		authorid = mod.id
		# Check if the person is in the modlist, if so tell them they're in the modlist
		if str(authorid) not in modlistlr:
			modlistr.close()
			# embed
			embed=discord.Embed(title="", color=color)
			embed.set_author(name=str(mod)[:-5],icon_url=mod.avatar_url)
			embed.add_field(name="Not a Mod", value=f"They're not a Mod", inline=True)
			await ctx.send(embed=embed)
		else:
			modlistr.close()
			strmodid = str(mod.id)
			modlistlr.remove(strmodid)
			modlistlr = "-".join(modlistlr)
			# opens modlist in write mode
			modlist = open('F:/IEE/storage/modlist.txt', 'w')
			modlist.write(str(modlistlr))
			modlist.close()
			# embed
			embed=discord.Embed(title="", color=color)
			embed.set_author(name=str(mod)[:-5],icon_url=mod.avatar_url)
			embed.add_field(name="Remove", value=f"Removed {str(mod)[:-5]}.", inline=True)
			await ctx.send(embed=embed)

	# Checks Code
	@commands.command()
	@commands.check(mod)
	async def code(self, ctx, start: int, end: int, file):
		#opens the file
		read = open(f"{file}", "r", encoding='utf-8').readlines()[int(start)-1:int(end)]
		# joins the file
		read = ' '.join(read)
		# removes 3x` and replaces it with [codeblock]
		read = Moderator.codeblock(read)
		await ctx.send(f'''>>> ```py\n{read}\n```''')

	def codeblock(text: str):
		# removes ` and replaces it with '
		text = text.replace('```', "[codeblock]")
		return text

	# Reloads the Cog
	@commands.command()
	@commands.check(mod)
	async def reload(self, ctx, cog : str):
		initial_extensions = [f'cogs.{cog}']
		for extension in initial_extensions:
			self.bot.reload_extension(extension)
		await ctx.send(f"Reloaded {cog}.py")

	@commands.command()
	@commands.check(mod)
	async def smute(self, ctx, member: discord.Member, *, reason: str):
		await member.edit(mute=True, reason=reason)
		await member.send("You got servermuted for reason: " + reason)
		await ctx.message.delete()

	@commands.command()
	@commands.check(mod)
	async def unsmute(self, ctx, member: discord.Member):
		await member.edit(mute=False, reason=reason)
		await member.send("You got unservermuted")
		await ctx.message.delete()

	@commands.command()
	@commands.check(mod)
	async def deafen(self, ctx, member: discord.Member, *, reason: str):
		await member.edit(deafen=True, reason=reason)
		await member.send("You got deafend for reason: " + reason)
		await ctx.message.delete()

	@commands.command()
	@commands.check(mod)
	async def undeafen(self, ctx, member: discord.Member, *, reason: str):
		await member.edit(deafen=False, reason=reason)
		await member.send("You got undeafened")
		await ctx.message.delete()

	@commands.command()
	@commands.check(mod)
	async def vckill(self, ctx, member: discord.Member, *, reason: str):
		await member.edit(deafen=True, reason=reason)
		await member.edit(mute=True, reason=reason)
		await member.send("You got deafend and servermuted for reason: " + reason)
		await ctx.message.delete()

	@commands.command()
	@commands.check(mod)
	async def unvckill(self, ctx, member: discord.Member, *, reason: str):
		await member.edit(deafen=False, reason=reason)
		await member.edit(mute=False, reason=reason)
		await member.send("You got unservermute and undeafened")
		await ctx.message.delete()

	@commands.command()
	async def modlist(self, ctx):
		# Silly random color
		color = random.randint(0, 0xFFFFFF)
		# opens the modlist and then stores the data as a list
		modlist = open('F:/IEE/storage/modlist.txt', 'r')
		modlist = modlist.read().split('-')
		mods = ""
		for mod in modlist:
			mods += "{} - {:5}\n".format(self.bot.get_user(int(mod)).mention, self.bot.get_user(int(mod)).name)
		embed=discord.Embed(title="Mods", description=f"{mods}", color=color)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.check(mod)
	async def move(self, ctx, member: discord.Member, channel: discord.VoiceChannel, *, reason: str):
		await member.edit(voice_channel=channel, reason=reason)
		await member.send("You got moved for reason: " + reason)
		await ctx.message.delete()

	@commands.command()
	@commands.check(mod)
	async def disconnect(self, ctx, member: discord.Member, *, reason: str ):
		await member.edit(voice_channel=None, reason=reason)
		await member.send("You got disconnected for reason: " + reason)
		await ctx.message.delete()

	@commands.command()
	@commands.check(mod)
	async def nick(self, ctx, member: discord.Member, nickname: str, *, reason: str):
		if nickname == 'None':
			nickname = None
		await member.edit(nick=nickname, reason=reason)
		await member.send("You nickname got changed for reason: " + reason)
		await ctx.message.delete()

	@commands.command()
	@commands.check(mod)
	async def changeroles(self, ctx, member: discord.Member, role: discord.Role, *, reason: str):
		await member.add_roles(role, reason=reason)
		await member.send(f"You got the {role} for reason: " + reason)
		await ctx.message.delete()

	@commands.command()
	@commands.check(mod)
	async def changestatus(self, ctx, status: str, statustype: str, *, message: str):
		statustype = statustype.lower()

		if status == 'online':
			status = discord.Status.online
		elif status == 'dnd' or status == 'do_not_disturb':
			status = discord.Status.dnd
		elif status == 'idle':
			status = discord.Status.idle
		elif status == 'offline':
			status = discord.Status.offline
		elif status == 'invisible':
			status = discord.Status.invisible
		else:
			await ctx.send("That is not a valid status")

		if statustype == 'playing':
			game = discord.Activity(name=message, type=discord.ActivityType.playing)
			await self.bot.change_presence(status=status, activity=game)
			await ctx.send(f"Changed the status to {statustype} {message}")
			statusofbot = open("F:/IEE/status.txt", 'w')
			statusofbot.write(f"{message}-{statustype}")
			statusofbot.close()
		elif statustype == 'watching':
			game = discord.Activity(name=message, type=discord.ActivityType.watching)
			await self.bot.change_presence(status=status, activity=game)
			await ctx.send(f"Changed the status to {statustype} {message}")
			statusofbot = open("F:/IEE/status.txt", 'w')
			statusofbot.write(f"{message}-{statustype}")
			statusofbot.close()
		elif statustype == 'listening':
			game = discord.Activity(name=message, type=discord.ActivityType.listening)
			await self.bot.change_presence(status=status, activity=game)
			await ctx.send(f"Changed the status to {statustype} {message}")
			statusofbot = open("F:/IEE/status.txt", 'w')
			statusofbot.write(f"{message}-{statustype}")
			statusofbot.close()
		else:
			await ctx.send("That is not a valid game")

	@commands.command()
	@commands.check(mod)
	async def purge(self, ctx, channel: discord.TextChannel, user: discord.Member, limit: int):
		def isuser(message):
			return message.author.id == user.id
		await channel.purge(limit=limit, check=isuser)
		await ctx.send("Should've worked")

	@commands.command()
	@commands.check(mod)
	async def reactto(self, ctx, message: discord.Message, reaction: str):
		await message.add_reaction(reaction)

	@commands.command()
	@commands.check(mod)
	async def moneygive(self, ctx, member: discord.Member, balance: str, amount: int = 0):
		person = str(member.id)
		server = str(ctx.guild.id)
		c.execute("SELECT * FROM people WHERE id=? AND server=?", (person, server))
		# commit
		conn.commit()
		# defines a var
		fetchall = c.fetchall()
		fetch = fetchall[0]
		pocket = round(fetch[1], 2)
		bank = round(fetch[2], 2)
		bankmax = round(fetch[3], 2)
		mines = float(fetch[5])
		if balance == 'coin':
			newbal = float(amount) + pocket
		elif balance == 'bank':
			newbal = float(amount) + bank
		elif balance == 'bankmax':
			newbal = float(amount) + bankmax
		else:
			await ctx.send('not a valid bal')
			return
		c.execute("UPDATE people SET {}=? WHERE id=? AND server=?".format(balance), (newbal, person, server))
		# commit
		conn.commit()

	@commands.command()
	@commands.check(mod)
	async def moneyset(self, ctx, member: discord.Member, balance: str, amount: int = 0):
		person = str(member.id)
		server = str(ctx.guild.id)
		c.execute("SELECT * FROM people WHERE id=? AND server=?", (person, server))
		# commit
		conn.commit()
		# defines a var
		fetchall = c.fetchall()
		fetch = fetchall[0]
		pocket = round(fetch[1], 2)
		bank = round(fetch[2], 2)
		bankmax = round(fetch[3], 2)
		mines = float(fetch[5])
		amount = float(amount)
		c.execute("UPDATE people SET {}=? WHERE id=? AND server=?".format(balance), (amount, person, server))
		# commit
		conn.commit()


# setup the Cog
def setup(bot):
	print("Mod Commands Loaded...")
	bot.add_cog(Moderator(bot))
def teardown(bot):
	print("Mod Commands Unloaded...")