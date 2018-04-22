import sys
from PyQt4 import QtGui, QtCore
import asyncio
import discord
class Window(QtGui.QMainWindow):

    def __init__(self,client):
        super(Window, self).__init__()
        self.setFixedSize(1200, 700)
        self.setWindowTitle("Client")
        self.client = client
        self.guild = None
        self.guildid = None
        self.channel = None
        self.channelid = None

        self.statusBar()

        main_menu = self.menuBar()
        main_menu_client = main_menu.addMenu('Client')

        item = QtGui.QAction("Restart", self)
        main_menu_client.addAction(item)

        self.home()

    def sync(self,coro):
        asyncio.run_coroutine_threadsafe(coro, asyncio.get_event_loop())

    def select_guild(self):
        self.guildid = self.guild_list.selectedItems()[0].data(QtCore.Qt.UserRole)
        self.update_channels()


    def select_channel(self):
        self.channelid = self.channel_list.selectedItems()[0].data(QtCore.Qt.UserRole)
        self.sync(self.update_messages())

    def home(self):
        self.message_send_btn = QtGui.QPushButton("Send", self)
        self.message_send_btn.resize(60,30)
        self.message_send_btn.move(1140,670)
        self.message_send_btn.clicked.connect(self.send_message)

        self.message_entry = QtGui.QLineEdit(self)
        self.message_entry.resize(800,30)
        self.message_entry.move(340,670)

        self.guild_list = QtGui.QListWidget(self)
        self.guild_list.resize(200,700)
        self.guild_list.move(0,20)
        self.guild_list.itemSelectionChanged.connect(self.select_guild)


        self.channel_list = QtGui.QListWidget(self)
        self.channel_list.resize(140,700)
        self.channel_list.move(200,20)
        self.channel_list.itemSelectionChanged.connect(self.select_channel)

        self.message_list = QtGui.QListWidget(self)
        self.message_list.resize(860,650)
        self.message_list.move(340,20)

        self.show()

    def update_guilds(self):
        self.guild_list.clear()
        for i in sorted(list(self.client.guilds), key=lambda x: x.name.lower()):
            item = QtGui.QListWidgetItem(str(i.name))
            item.setData(QtCore.Qt.UserRole,i.id)
            self.guild_list.addItem(item)

    def update_channels(self):
        if self.guildid != None:
            self.guild = self.client.get_guild(self.guildid)
            self.channel_list.clear()
            for i in self.guild.channels:
                if type(i) == discord.channel.TextChannel:
                    item = QtGui.QListWidgetItem(str(i.name))
                    item.setData(QtCore.Qt.UserRole,i.id)
                    self.channel_list.addItem(item)



    async def update_messages(self):
        if self.channelid != None:
            self.channel = self.guild.get_channel(self.channelid)
            self.message_list.clear()
            async for msg in self.channel.history():
                item = QtGui.QListWidgetItem(str(msg.author)+": "+str(msg.content))
                item.setData(QtCore.Qt.UserRole,msg)
                self.message_list.addItem(item)
        self.message_list.verticalScrollBar().setValue(self.message_list.verticalScrollBar().maximum())

    def new_message(self,msg):

        if self.channelid != None:
            if self.channelid == msg.channel.id:
                item = QtGui.QListWidgetItem(str(msg.author)+": "+str(msg.content))
                item.setData(QtCore.Qt.UserRole,msg)
                self.message_list.addItem(item)
        self.message_list.verticalScrollBar().setValue(self.message_list.verticalScrollBar().maximum())

    def send_message(self):
        self.sync(self.channel.send(self.message_entry.text()))

    def ready(self):
        self.update_guilds()

if __name__ == "__main__":
    import main
