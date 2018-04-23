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
        if len(self.guild_list.selectedItems()) > 0:
            self.guildid = self.guild_list.selectedItems()[0].data(QtCore.Qt.UserRole)
            self.update_channels()


    def select_channel(self):
        if len(self.channel_list.selectedItems()) > 0:
            self.channelid = self.channel_list.selectedItems()[0].data(QtCore.Qt.UserRole)
            self.channel = self.guild.get_channel(self.channelid)
            perms = self.channel.permissions_for(self.guild.get_member(self.client.user.id))
            if perms.send_messages:
                self.message_send_btn.setDisabled(False)
                self.message_entry.setDisabled(False)
            else:
                self.message_send_btn.setDisabled(True)
                self.message_entry.setDisabled(True)

            self.sync(self.update_messages())

    def home(self):
        self.message_send_btn = QtGui.QPushButton("Send", self)
        self.message_send_btn.resize(60,30)
        self.message_send_btn.move(1140,670)
        self.message_send_btn.clicked.connect(self.send_message)

        self.message_entry = QtGui.QLineEdit(self)
        self.message_entry.resize(800,30)
        self.message_entry.move(340,670)
        self.message_entry.returnPressed.connect(self.send_message)
        self.message_entry.setFocus()


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
        self.message_list.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom)

        self.show()

    def update_guilds(self):
        scroll = self.guild_list.verticalScrollBar().value()
        self.guild_list.clear()
        for i in sorted(list(self.client.guilds), key=lambda x: x.name.lower()):
            item = QtGui.QListWidgetItem(str(i.name))
            item.setData(QtCore.Qt.UserRole,i.id)
            self.guild_list.addItem(item)

        self.guild_list.verticalScrollBar().setValue(scroll)

    def update_channels(self):
        if self.guildid != None:
            self.guild = self.client.get_guild(self.guildid)
            scroll = self.channel_list.verticalScrollBar().value()
            self.channel_list.clear()
            for i in self.guild.channels:
                perms = i.permissions_for(self.guild.get_member(self.client.user.id))
                if type(i) == discord.channel.TextChannel:
                    item = QtGui.QListWidgetItem(str(i.name))
                    item.setData(QtCore.Qt.UserRole,i.id)

                    if not perms.read_messages:
                        item.setFlags(QtCore.Qt.NoItemFlags)

                    self.channel_list.addItem(item)

            self.channel_list.verticalScrollBar().setValue(scroll)

    async def update_messages(self):
        if self.channelid != None:
            self.channel = self.guild.get_channel(self.channelid)
            self.message_list.clear()
            async for msg in self.channel.history(reverse=True):
                item = QtGui.QListWidgetItem(str(msg.author)+": "+str(msg.content))
                item.setData(QtCore.Qt.UserRole,msg)
                item.setToolTip(str(msg.created_at))
                self.message_list.addItem(item)





    def new_message(self,msg):
        if self.channelid != None:
            if self.channelid == msg.channel.id:
                item = QtGui.QListWidgetItem(str(msg.author)+": "+str(msg.content))
                item.setData(QtCore.Qt.UserRole,msg)
                item.setToolTip(str(msg.created_at))
                self.message_list.addItem(item)




    def scroll_to_bottom(self, bypass=False):
        print(self.message_list.verticalScrollBar().value())
        if abs(self.message_list.verticalScrollBar().value() - self.message_list.verticalScrollBar().maximum()) < 10 or bypass:
            self.message_list.verticalScrollBar().setValue(self.message_list.verticalScrollBar().maximum())

    def send_message(self):
        self.sync(self.channel.send(self.message_entry.text()))
        self.message_entry.clear()
        self.message_entry.setFocus()

    def ready(self):
        self.update_guilds()

if __name__ == "__main__":
    import main
