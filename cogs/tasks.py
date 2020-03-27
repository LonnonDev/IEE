import time
import json
import random
import math
import discord
import os
import sys
import sqlite3
import secrets
import datetime
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from discord.ext import tasks
import asyncio
import discord.utils
os.chdir('F:/IEE')

# Connects to the database
conn = sqlite3.connect("people.db")
c = conn.cursor()


class tasks(commands.Cog, name="tasks"):
	def __init__(self, bot):
		self.bot = bot
		self.weather.start()

	@tasks.loop(seconds=1.0, reconnect=True)
	async def weather(self):
		now = datetime.datetime.now()
		now = f"{now.hour}-{now.minute}-{now.second}"
		if now == '7-0-0':
			guild = self.bot.get_guild(418499762321358848)
			channel = guild.get_channel(691728835753934929)
			stats = []
			weather = random.randint(0, 100)
			if weather in range(0, 66):
				weather = 'Sunny'
				tempc = random.randint(-1, 15)
				tempf = random.randint(30, 60)
			elif weather in range(66, 77):
				weather = 'Rainy'
				tempc = random.randint(-6, 4)
				tempf = random.randint(20, 40)
			elif weather in range(77, 101):
				weather = 'Stormy'
				tempc = random.randint(16, 40)
				tempf = random.randint(60, 105)
			stats.append(tempc)
			stats.append(tempf)
			stats.append(weather)
			await channel.send(f"Weather is `{stats[2]}`\nTemperature in Celsius is `{stats[0]}`\nTemperature in Fahrenheit is `{stats[1]}`")



def setup(bot):
	print("Tasks Commands Loaded")
	bot.add_cog(tasks(bot))
def teardown(bot):
	print("Tasks Commands Unloaded...")