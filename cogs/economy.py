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
		mines = fetch[5]
		c.execute("UPDATE people SET coin=?, bank=? WHERE id=? AND server=?", (pocket, bank, person, server))
		# commit
		conn.commit()
		pocket = float('{:0.2f}'.format(fetch[1]))
		bank = float('{:0.2f}'.format(fetch[2]))
		# embeds
		embed=discord.Embed(title=f"Balance", color=color)
		embed.set_author(name=membername[:-5],icon_url=personog.avatar_url)
		embed.add_field(name="Pocket", value="{:,.2f} Ʀ".format(pocket), inline=True)
		embed.add_field(name="Bank", value="{:,.2f} Ʀ".format(bank,), inline=True)
		embed.add_field(name="Total", value="{:,.2f} Ʀ".format(pocket + bank), inline=True)
		embed.add_field(name="Mines", value="You have {:,.2f} mines".format(float(mines)), inline=True)
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
		# get the type of amount
		try:
			amount = round(float(amount), 2)
		except:
			if amount == 'all' or amount == 'max':
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

def taxgive(give, server):
	if server == '636996896161923093':
		person = str(407313426751160353)
	elif server == '418499762321358848':
		person = str(418499762321358848)
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
		c.execute("INSERT INTO people (id, coin, bank, server, inventory, mines) VALUES (?, 0, 0, ?, '', 0)", (person, server))
		conn.commit()

def ded(person):
	c.execute("UPDATE people SET coin=0, bank=0 WHERE id=? AND server=?", (person, server))
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
def teardown(bot):
	print("Economy Commands Unloaded...")