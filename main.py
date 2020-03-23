"""
MIT License

Copyright (c) 2020 LonnonjamesD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import time
import json
import random
import math
import discord
import os
import sys
import sqlite3
import secret
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from os import listdir
import datetime
import asyncio
# import the token
from config import *

bottype = list(sys.argv)
print(bottype)
if bottype[1] == 'normal':
	token = normaltoken
elif bottype[1] == 'beta':
	token = betatoken

conn = sqlite3.connect("people.db")
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS people (
			id blob,
			coin real,
			bank real,
			bankmax real,
			server blob,
			inventory blob
			)""")
conn.commit()

# shard id
shardids = 1
# shard count
shardcount = 1
# command prefix
commandprefix = ('.',)

path = f'F:/IEE/cogs'
cogs = []
for f in listdir(path):
	file = f"cogs.{f}".replace('.py', '')
	cogs += [file]
cogs.remove('cogs.__pycache__')
#cogs.remove('cogs.errorhandler')


# get the bot started
bot = commands.AutoShardedBot(case_insensitive=True, loop=None, shard_id=shardids, shard_count=shardcount, command_prefix=commands.when_mentioned_or(*commandprefix))

# loads the cogs
for extension in cogs:
	bot.load_extension(extension)

print("Loaded")
bot.run(token)
