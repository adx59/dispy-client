import sys
from PyQt4 import QtGui, QtCore
import discord
import gui
from threading import Thread
import asyncio
import time

client = discord.AutoShardedClient()

token = input("token: ")
print("Logging In...")

app = QtGui.QApplication(sys.argv)
window = gui.Window(client)





@client.event
async def on_ready():
    print("Logged In!")
    window.ready()


@client.event
async def on_guild_join(guild):
    window.update_guilds()


@client.event
async def on_guild_remove(guild):
    window.update_guilds()


@client.event
async def on_guild_update(before, after):
    window.update_guilds()


@client.event
async def on_channel_create(channel):
    window.update_channels()

@client.event
async def on_channel_delete(channel):
    window.update_channels()

@client.event
async def on_channel_update(before,after):
    window.update_channels()


@client.event
async def on_message(msg):
    window.new_message(msg)



def run():
    sys.exit(app.exec_())



t = Thread(target=client.run, args=[token])
t.daemon = True
t.start()

run()
