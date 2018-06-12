import sys
from PyQt4 import QtGui, QtCore
import discord
import gui
from threading import Thread
import asyncio
import time

client = discord.AutoShardedClient()

@client.event
async def on_ready():
    print("Logged In!")
    window.ready()

@client.event
async def on_guild_join(guild):
    if client.is_ready():
        window.update_guilds()

@client.event
async def on_guild_remove(guild):
    if client.is_ready():
        window.update_guilds()

@client.event
async def on_guild_update(before, after):
    if client.is_ready():
        window.update_guilds()

@client.event
async def on_channel_create(channel):
    if client.is_ready():
        window.update_channels()

@client.event
async def on_channel_delete(channel):
    if client.is_ready():
        window.update_channels()

@client.event
async def on_channel_update(before,after):
    if client.is_ready():
        window.update_channels()

@client.event
async def on_message(msg):
    window.new_message(msg)

def run():
    sys.exit(app.exec_())

app = QtGui.QApplication(sys.argv)
window = gui.Window(client)

token, ok = QtGui.QInputDialog.getText(window, "Token",
                "Token:", QtGui.QLineEdit.Normal)


if ok:
    print("Logging In...")

    t = Thread(target=client.run, args=[token])
    t.daemon = True
    t.start()

    run()
else:
    sys.exit()
