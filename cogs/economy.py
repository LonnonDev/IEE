import time
import json
import random
import math
import discord
import os
import sys
import sqlite3
import secrets
import tex2pix
import datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from sympy import preview
from sympy.solvers import solve
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

# Eco Cog
class Economy(commands.Cog, name="Economy Commands"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['ping', 'uptime'])
	async def info(self, ctx):
		ping = '{0}ms'.format(round(float(self.bot.latency) * 1000), 0)
		randomimg = random.randint(1, 2)
		datetimeformat = "%d Day(s), %H Hour(s), %M Minute(s), %S Second(s)"
		x = datetime.datetime.now()
		x = str(x.strftime("%d Day(s), %H Hour(s), %M Minute(s), %S Second(s)"))
		f = open("F:/IEE/storage/started.txt", 'r')
		time = f.read()
		f.close()
		diff = datetime.datetime.strptime(x, datetimeformat) - datetime.datetime.strptime(time, datetimeformat)
		# Silly random color
		color = random.randint(0, 0xFFFFFF)
		embed=discord.Embed(title=f"Info...", color=color)
		embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
		if randomimg == 1:
			embed.set_image(url="https://media.giphy.com/media/3og0IGzJmvAoY5ijmw/giphy.gif")
		elif randomimg == 2:
			embed.set_image(url="https://media.giphy.com/media/3og0IUEEbY9wRwrBL2/giphy.gif")
		embed.set_thumbnail(url="attachment://test.png")
		embed.add_field(name="Uptime", value=f"Uptime of {diff} ", inline=True)
		embed.add_field(name="Ping", value=f"Ping of the bot is {ping} ", inline=True)
		await ctx.send(embed=embed)

	# Balance Command
	@commands.command(aliases=['bal',])
	async def balance(self, ctx, person: discord.Member = None):
		"""
		Checks you bal
		"""
		# Silly random color
		color = random.randint(0, 0xFFFFFF)
		# Checks if person is none, and if it is sets it to author
		if person == None:
			personog = ctx.author
			person = str(ctx.author.id)
			server = str(ctx.guild.id)
			member = str(ctx)
			membername = str(ctx.author)
		else:
			personog = person
			member = str(person)
			membername = str(person)
			person = str(person.id)
			server = str(ctx.guild.id)
		# handels person
		personhandler(person, server)
		# checks there bal
		c.execute("SELECT * FROM people WHERE id=? AND server=?", (person, server))
		# commit
		conn.commit()
		# defines a var
		fetchall = c.fetchall()
		fetch = fetchall[0]
		pocket = round(fetch[1], 2)
		bank = round(fetch[2], 2)
		bankmax = round(fetch[3], 2)
		mines = fetch[6]
		c.execute("UPDATE people SET coin=?, bank=?, bankmax=? WHERE id=? AND server=?", (pocket, bank, bankmax, person, server))
		# commit
		conn.commit()
		if bankmax == '∞':
			bankmax = float('inf')
		else:
			bankmax = float('{:0.2f}'.format(fetch[3]))
		pocket = float('{:0.2f}'.format(fetch[1]))
		bank = float('{:0.2f}'.format(fetch[2]))
		# embeds
		embed=discord.Embed(title=f"Balance", color=color)
		embed.set_author(name=membername[:-5],icon_url=personog.avatar_url)
		embed.add_field(name="Pocket", value="{:,.2f} Ʀ".format(pocket), inline=True)
		if bankmax != '∞':
			embed.add_field(name="Bank", value="{:,.2f}/{} Ʀ".format(bank, bankmax), inline=True)
		else:
			embed.add_field(name="Bank", value="{:,.2f}/{:,.2f} Ʀ".format(bank, bankmax), inline=True)
		embed.add_field(name="Total", value="{:,.2f} Ʀ".format(pocket + bank), inline=True)
		embed.add_field(name="Bank Left", value="{:,.2f} Ʀ".format(bankmax - bank), inline=True)
		embed.add_field(name="Mines", value="You have {:,.2f} mines".format(float(mines)), inline=True)
		await ctx.send(embed=embed)

	# Print some money
	@commands.cooldown(1, 120, commands.BucketType.user)
	@commands.command(aliases=["print",])
	async def printmoney(self, ctx, money: int = 100):
		"""
		Print Some Money
		Alias = Print
		"""
		# persons id
		person = str(ctx.author.id)
		server = str(ctx.guild.id)
		personhandler(person, server)
		# handle them
		personhandler(person, server)
		# get there money
		c.execute("SELECT * FROM people WHERE id=? AND server=?", (person, server))
		conn.commit()
		coinbal = c.fetchone()
		# die chance
		die = random.randint(1,250)
		if die == 1:
			ded(person)
			# Silly random color
			color = random.randint(0, 0xFFFFFF)
			embed=discord.Embed(title=f"Death...", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name="-", value=f"You died and lost everything", inline=True)
			await ctx.send(embed=embed)
			return
		# if money to print is under 100 or over 1000, give them an error
		if money < 100 or money > 250:
			# Silly random color
			color = random.randint(0, 0xFFFFFF)
			errortype = 'Print Error'
			error = f"{money} is not a valid amount of money to print, Min: 100, Max: 250"
			embed=discord.Embed(title=f"Error {errortype}", color=color)
			embed.add_field(name="-", value=f"```\n{error}\n```", inline=False)
			await ctx.send(embed=embed, delete_after=30)
			await asyncio.sleep(30)
			try:
				await ctx.message.delete()
			except:
				pass
			return
		# Silly random color
		color = random.randint(0, 0xFFFFFF)
		# break printer chance
		breakchance = random.randint(1,money)
		#breakchance = 1
		if math.floor(money/2) == 0:
			# Silly random color
			color = random.randint(0, 0xFFFFFF)
			errortype = 'Print Error'
			error = f"{money} is not a valid amount of money to print"
			embed=discord.Embed(title=f"Error {errortype}", color=color)
			embed.add_field(name="-", value=f"```\n{error}\n```", inline=False)
			await ctx.send(embed=embed, delete_after=30)
			await asyncio.sleep(30)
			try:
				await ctx.message.delete()
			except:
				pass
			return
		if int(breakchance) in range(int(math.floor(money/6))):
			embed=discord.Embed(title=f"Printing...", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name="-", value=f"Printing **{money}** Ʀ", inline=True)
			await ctx.send(embed=embed)
			await asyncio.sleep(90)
			coinbal = int(coinbal[1])+money
			c.execute("UPDATE people SET coin=? WHERE id=? AND server=?", (coinbal, person, server))
			conn.commit()
			embed=discord.Embed(title=f"Done...", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name="-", value=f"Done Printing **{money}** Ʀ", inline=True)
			await ctx.send(embed=embed)
		else:
			embed=discord.Embed(title=f"Broke...", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name="-", value=f"Your printer broke...", inline=True)
			await ctx.send(embed=embed)

	# Leaderboard Command
	@commands.command(aliases=['lb',])
	@commands.is_owner()
	async def leaderboard(self, ctx, typeoflb: str = 'p'):
		"""
		Checks the leaderboard top 5
		Alias = LB
		"""
		typeoflb = typeoflb.lower()
		if typeoflb != 'bank' and typeoflb != 'pocket' and typeoflb != 'b' and typeoflb != 'p':
			# Silly random color
			color = random.randint(0, 0xFFFFFF)
			errortype = 'Leaderboard Error'
			error = f"{typeoflb} is not a valid type of Balance, Valid types are, bank, pocket, b, p"
			embed=discord.Embed(title=f"Error {errortype}", color=color)
			embed.add_field(name="-", value=f"```\n{error}\n```", inline=False)
			await ctx.send(embed=embed, delete_after=30)
			await asyncio.sleep(30)
			try:
				await ctx.message.delete()
			except:
				pass
			return
		person = str(ctx.author.id)
		server = str(ctx.guild.id)
		personhandler(person, server)
		# Silly random color
		color = random.randint(0, 0xFFFFFF)
		# get the people
		c.execute("SELECT * FROM people")
		# commit
		conn.commit()
		# fetchall
		fetch = c.fetchall()
		# sort
		fetchpocket = fetch.sort(key = lambda x: x[1], reverse=True) 
		fetchbank = fetch.sort(key = lambda x: x[2], reverse=True) 
		# range
		i = 0
		i2 = 0
		# list length
		fetchlength = len(fetch)
		# embed
		embed=discord.Embed(title=f"Balance Leaderboard", color=color)
		# get first 10 results
		if typeoflb == 'pocket' or typeoflb == 'p':
			for i in range(5):
				fetchi = fetchpocket[i]
				name = str(self.bot.get_user(int(fetchi[0])))[:-5]
				pocket = fetchi[1]
				embed.add_field(name=f"#{i + 1} {name}", value="Pocket: {:,.2f}".format(pocket), inline=False)
				i += 1 
		elif typeoflb == 'bank' or typeoflb == 'b':
			for i in range(5):
				fetchi = fetchbank[i]
				name = str(self.bot.get_user(int(fetchi[0])))[:-5]
				bank = fetchi[2]
				embed.add_field(name=f"#{i + 1} {name}", value="Bank: {:,.2f}".format(bank), inline=False)
				i += 1 
		# gets the user
		for i2 in range(fetchlength):
			fetchi = fetch[i2]
			try:
				fetchi.index(str(ctx.author.id))
				pocket = fetchi[1]
				bank = fetchi[2]
				total = int(pocket) + int(bank)
				embed.add_field(name=f"-", value="**(YOU)\n #{i2 + 1} {str(ctx.author)[:-5]}\nPocket: {:,.2f} Bank: {:,.2f} Total Bal: {:,.2f}**".format(pocket, bank, total), inline=False)
			except:
				pass
		await ctx.send(embed=embed)

	@commands.command()
	@commands.is_owner()
	async def createorganization(self, name: str):
		personhandler(person, server)
		# select from people
		c.execute("SELECT * FROM organization")
		# commit
		conn.commit()
		# fetch
		fetchall = c.fetchall()[0]
		# fetchlength
		fetchlength = len(fetchall)
		for i in range(fetchlength):
			pass

	@commands.command(aliases=['dep',])
	async def deposit(self, ctx, amount):
		# persons name
		person = str(ctx.author.id)
		server = str(ctx.guild.id)
		# select from people
		c.execute("SELECT * FROM people WHERE id=? AND server=?", (person, server))
		# commit
		conn.commit()
		# fetch
		fetchall = c.fetchall()
		# user vars
		pocket = float(fetchall[0][1])
		bank = float(fetchall[0][2])
		bankmax = float(fetchall[0][3])
		leftovers = bankmax - bank
		# get the type of amount
		try:
			amount = round(float(amount), 2)
		except:
			if amount == 'all' or amount == 'max':
				amount = leftovers - pocket
				if amount <= 0:
					amount = leftovers
				else:
					amount = pocket
			elif amount == 'half':
				amount = (pocket/2)
			elif amount == 'quarter':
				amount = (pocket/4)
			else:
				# Silly random color
				color = random.randint(0, 0xFFFFFF)
				embed=discord.Embed(title=f"That's not a valid amount...", color=color)
				embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
				embed.add_field(name="-", value=f"That is not a valid amount of money to deposit, it must be **MAX** or a number", inline=True)
				await ctx.send(embed=embed)
		newpocket = pocket - amount
		newbank = bank + amount
		if amount > pocket:
			# Silly random color
			color = random.randint(0, 0xFFFFFF)
			embed=discord.Embed(title=f"Not Enough...", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name="-", value=f"You Don't have enough in your pocket for that", inline=True)
			await ctx.send(embed=embed)
		elif amount > bankmax:
			# Silly random color
			color = random.randint(0, 0xFFFFFF)
			embed=discord.Embed(title=f"Bankmax Too Small...", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name="-", value=f"You Don't have enough room in your bank for that", inline=True)
			await ctx.send(embed=embed)
		elif amount > leftovers:
			# Silly random color
			color = random.randint(0, 0xFFFFFF)
			embed=discord.Embed(title=f"Bankmax Too Small...", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name="-", value=f"You Don't have enough room in your bank for that", inline=True)
			await ctx.send(embed=embed)
		else:
			# Silly random color
			color = random.randint(0, 0xFFFFFF)
			embed=discord.Embed(title=f"Depositing...", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name="-", value=f"Depositing {amount} Ʀ", inline=True)
			await ctx.send(embed=embed)
			# update their bal
			c.execute("UPDATE people SET coin=?, bank=? WHERE id=? AND server=?", (newpocket, newbank, person, server))
			# commit
			conn.commit()

	@commands.command(aliases=['with',])
	async def withdraw(self, ctx, amount):
		# persons name
		person = str(ctx.author.id)
		server = str(ctx.guild.id)
		# select from people
		c.execute("SELECT * FROM people WHERE id=? AND server=?", (person, server))
		# commit
		conn.commit()
		# fetch
		fetchall = c.fetchall()
		# user vars
		pocket = float(fetchall[0][1])
		bank = float(fetchall[0][2])
		bankmax = float(fetchall[0][3])
		# get the type of amount
		try:
			amount = round(float(amount), 2)
		except:
			if amount == 'all' or amount == 'max':
				amount = bank
			elif amount == 'half':
				amount = (bank/2)
			elif amount == 'quarter':
				amount = (bank/4)
			else:
				# Silly random color
				color = random.randint(0, 0xFFFFFF)
				embed=discord.Embed(title=f"That's not a valid amount...", color=color)
				embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
				embed.add_field(name="-", value=f"That is not a valid amount of money to deposit, it must be **MAX** or a number", inline=True)
				await ctx.send(embed=embed)
		newpocket = pocket + amount
		newbank = bank - amount
		if amount > bank:
			# Silly random color
			color = random.randint(0, 0xFFFFFF)
			embed=discord.Embed(title=f"Not Enough...", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name="-", value=f"You Don't have enough in your bank for that", inline=True)
			await ctx.send(embed=embed)
		else:
			# Silly random color
			color = random.randint(0, 0xFFFFFF)
			embed=discord.Embed(title=f"Withdrawing...", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name="-", value=f"Withdrawing {amount} Ʀ", inline=True)
			await ctx.send(embed=embed)
			# update their bal
			c.execute("UPDATE people SET coin=?, bank=? WHERE id=? AND server=?", (newpocket, newbank, person, server))
			# commit
			conn.commit()

	@commands.command(hidden=True)
	@commands.cooldown(1, 3600, commands.BucketType.user)
	async def beg(self, ctx):
		enabled = False
		if enabled == False:
			await ctx.send("Disabled Command")
			return
		# persons name
		person = str(ctx.author.id)
		server = str(ctx.guild.id)
		personhandler(person, server)
		taxs = open("F:/IEE/storage/tax.txt", 'r')
		tax = taxs.read()
		addtax = (float(int(tax)) / 100) + 1
		removetax = float(int(tax)) / 100
		taxs.close()
		# select from people
		c.execute("SELECT * FROM people WHERE id=? AND server=?", (person, server))
		# commit
		conn.commit()
		# fetch
		fetchall = c.fetchall()
		# user vars
		pocket = float(fetchall[0][1])
		randommoney = float(random.randint(1, 50))
		newpocket = pocket + (randommoney - (randommoney * removetax))
		realearned = randommoney - (randommoney * removetax)
		taxearned = randommoney * removetax
		taxgive(taxearned, server)
		# update their bal
		color = random.randint(0, 0xFFFFFF)
		embed=discord.Embed(title=f"Money +", color=color)
		embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
		embed.add_field(name="-", value=f"You Got Donated {realearned} Ʀ", inline=True)
		await ctx.send(embed=embed)
		c.execute("UPDATE people SET coin=? WHERE id=? AND server=?", (newpocket, person, server))
		# commit
		conn.commit()

			
class gambling(commands.Cog, name="Gambling Commands"):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=['bj'])
	@commands.is_owner()
	@commands.cooldown(1, 5, commands.BucketType.user)
	async def blackjack(self, ctx, gambleamount: int):
		async def author(message):
			return message.author.id == ctx.author.id
		player = []
		dealer = []
		for x in range(2):
			rng = random.randint(1,11)
			if rng == 11:
				await ctx.send("You got an ace, do you want it to be a 1 or a 11")
				message = await self.bot.wait_for('message', timeout=60.0, check=author)
				if message == '1':
					player += '1'
				elif message == '11':
					player += '11'
				else:
					await ctx.send("Not a valid option, defaulting to 1")
					player += '1'
			else:
				await ctx.send(rng)
				player += str(rng)
		await ctx.send(player)


	@commands.command()
	async def slots(self, ctx, gambleamount: int):
		if gambleamount < 100:
			color = random.randint(0, 0xFFFFFF)
			embed=discord.Embed(title=f"Not Enough...", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name="-", value=f"You must gamble atleast 100 Ʀ", inline=True)
			await ctx.send(embed=embed)
			return
		person = str(ctx.author.id)
		server = str(ctx.guild.id)
		c.execute("SELECT * FROM people WHERE id=? AND server=?", (person, server))
		# commit
		conn.commit()
		# fetch
		fetchall = c.fetchall()
		# user vars
		pocket = float(fetchall[0][1])
		if gambleamount > pocket:
			color = random.randint(0, 0xFFFFFF)
			embed=discord.Embed(title=f"Not Enough...", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name="-", value=f"You don't have that amount in your pocket to gamble {gambleamount} Ʀ", inline=True)
			await ctx.send(embed=embed)
			return
		slot1 = random.randint(1, 5)
		slot2 = random.randint(1, 5)
		slot3 = random.randint(1, 5)
		# 1 = 2
		# 1 = 3
		# 2 = 3
		if slot1 == slot2 and slot2 == slot3 and slot1 == slot3:
			randfruit = random.randint(1, 20)
			# 🍇 4x
			# 🍌 2x
			# 🍍 1.5x
			# 🥭 1x
			color = random.randint(0, 0xFFFFFF)
			embed=discord.Embed(title="Slots", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			embed.add_field(name=f"Rates", value=f"\n**2x Fruits**\n🍇 1x\n🍌 0.5x\n🍍 0x\n🥭 -1x\n**3x Fruits**\n🍇 4x\n🍌 2x\n🍍 1.5x\n🥭 1x", inline=True)
			if randfruit in range(1, 11):
				fruit = "🥭"
				gambleamount *= 1
				embed.add_field(name=f"You Won: {gambleamount} Ʀ", value=f"{fruit} {fruit} {fruit}", inline=True)
			elif randfruit in range(11, 18):
				fruit = "🍍"
				gambleamount *= 1.5
				embed.add_field(name=f"You Won: {gambleamount} Ʀ", value=f"{fruit} {fruit} {fruit}", inline=True)
			elif randfruit in range(18, 20):
				fruit = "🍌"
				gambleamount *= 2
				embed.add_field(name=f"You Won: {gambleamount} Ʀ", value=f"{fruit} {fruit} {fruit}", inline=True)
			elif randfruit in 20:
				fruit = "🍇"
				gambleamount *= 4
				embed.add_field(name=f"You Won: {gambleamount} Ʀ", value=f"{fruit} {fruit} {fruit}", inline=True)
			earned = pocket + gambleamount
			c.execute("UPDATE people SET coin=? WHERE id=? AND server=?", (earned, person, server))
			# commit
			conn.commit()
			await ctx.send(embed=embed)
		else:
			randfruit1 = 1
			randfruit2 = 1
			randfruit3 = 1
			while randfruit1 == randfruit2 and randfruit2 == randfruit3 and randfruit1 == randfruit3:
				randfruit1 = random.randint(1, 6)
				randfruit2 = random.randint(1, 6)
				randfruit3 = random.randint(1, 6) 
				if randfruit1 in range(1, 4):
					randfruit1 = "🥭"
				elif randfruit1 == 4:
					randfruit1 = "🍍"
				elif randfruit1 == 5:
					randfruit1 = "🍌"
				elif randfruit1 == 6:
					randfruit1 = "🍇"

				if randfruit2 in range(1, 4):
					randfruit2 = "🥭"
				elif randfruit2 == 4:
					randfruit2 = "🍍"
				elif randfruit2 == 5:
					randfruit2 = "🍌"
				elif randfruit2 == 6:
					randfruit2 = "🍇"

				if randfruit3 in range(1, 4):
					randfruit3 = "🥭"
				elif randfruit3 == 4:
					randfruit3 = "🍍"
				elif randfruit3 == 5:
					randfruit3 = "🍌"
				elif randfruit3 == 6:
					randfruit3 = "🍇"

			color = random.randint(0, 0xFFFFFF)
			embed=discord.Embed(title="Slots", color=color)
			embed.set_author(name=str(ctx.author)[:-5],icon_url=ctx.author.avatar_url)
			# 🍇 2x
			# 🍌 1x
			# 🍍 0.5x
			# 🥭 0x
			embed.add_field(name=f"Rates", value=f"\n**2x Fruits**\n🍇 1x\n🍌 0.5x\n🍍 0x\n🥭 -1x\n**3x Fruits**\n🍇 4x\n🍌 2x\n🍍 1.5x\n🥭 1x", inline=True)
			if randfruit1 == randfruit2 and randfruit2 == "🥭" or randfruit1 == randfruit3 and randfruit3 == "🥭" or randfruit2 == randfruit3 and randfruit3 == "🥭":
				gambleamount *= -1
				embed.add_field(name=f"You Won: {gambleamount} Ʀ", value=f"{randfruit1} {randfruit2} {randfruit3}", inline=True)
			elif randfruit1 == randfruit2 and randfruit2 == "🍍" or randfruit1 == randfruit3 and randfruit3 == "🍍" or randfruit2 == randfruit3 and randfruit3 == "🍍":
				gambleamount *= 0
				embed.add_field(name=f"You Won: {gambleamount} Ʀ", value=f"{randfruit1} {randfruit2} {randfruit3}", inline=True)
			elif randfruit1 == randfruit2 and randfruit2 == "🍌" or randfruit1 == randfruit3 and randfruit3 == "🍌" or randfruit2 == randfruit3 and randfruit3 == "🍌":
				gambleamount *= 0.5
				embed.add_field(name=f"You Won: {gambleamount} Ʀ", value=f"{randfruit1} {randfruit2} {randfruit3}", inline=True)
			elif randfruit1 == randfruit2 and randfruit2 == "🍇" or randfruit1 == randfruit3 and randfruit3 == "🍇" or randfruit2 == randfruit3 and randfruit3 == "🍇":
				gambleamount *= 1
				embed.add_field(name=f"You Won: {gambleamount} Ʀ", value=f"{randfruit1} {randfruit2} {randfruit3}", inline=True)
			else:
				gambleamount = gambleamount * -1
				embed.add_field(name=f"You Lost: {gambleamount} Ʀ", value=f"{randfruit1} {randfruit2} {randfruit3}", inline=True)
			# handle the money
			earned = pocket + gambleamount
			c.execute("UPDATE people SET coin=? WHERE id=? AND server=?", (earned, person, server))
			# commit
			conn.commit()
			await ctx.send(embed=embed)

def taxgive(give, server):
	if server == '636996896161923093':
		person = str(407313426751160353)
	elif server == '577072824355782656':
		person = str(670719216852140158)
	elif server == '680036875603542118':
		person = str(600798393459146784)
	c.execute("SELECT * FROM people WHERE id=? AND server=?", (person, server))
	# commit
	conn.commit()
	# fetch
	fetchall = c.fetchall()
	# user vars
	pocket = float(fetchall[0][1])

	earned = pocket + give

	c.execute("UPDATE people SET coin=? WHERE id=? AND server=?", (earned, person, server))
	# commit
	conn.commit()

# person handler handles the people of the universe
def personhandler(person, server):
	# select from people
	c.execute("SELECT * FROM people WHERE id=? AND server=?", (person, server))
	# commit
	conn.commit()
	# fetch
	if c.fetchone() == None:
		# insert values for person
		c.execute("INSERT INTO people (id, coin, bank, bankmax, server, inventory, mines) VALUES (?, 0, 0, 50, ?, '', 0)", (person, server))
		conn.commit()

def ded(person):
	c.execute("UPDATE people SET coin=0, bank=0, bankmax=50 WHERE id=? AND server=?", (person, server))
	conn.commit()

# sort 
def sortSecond(val): 
	return val[2]
# sort 
def sortFirst(val): 
	return val[1]

# setup the Cog
def setup(bot):
	print("Economy Commands Loaded...")
	bot.add_cog(Economy(bot))
	bot.add_cog(gambling(bot))
def teardown(bot):
	print("Economy Commands Unloaded...")