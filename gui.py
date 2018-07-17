import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import asyncio
import discord
import pyperclip


class Window(QMainWindow):

    def __init__(self, client):
        super(Window, self).__init__()
        self.setFixedSize(1200, 700)
        self.setWindowTitle("Client")
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
        """)

        self.client = client
        self.guild = None
        self.guildid = None
        self.channel = None
        self.channelid = None
        self.message = None
        self.messageid = None
        self.home()


    def home(self):
        self.statusBar()
        main_menu = self.menuBar()


        main_menu_client = main_menu.addMenu('Client')
        item = QtGui.QAction("Restart", self)
        main_menu_client.addAction(item)


        main_menu_server = main_menu.addMenu('Server')
        item = QtGui.QAction("Info", self)
        item.triggered.connect(self.guild_info)
        main_menu_server.addAction(item)

        main_menu_channel = main_menu.addMenu('Channel')
        item = QtGui.QAction("Info", self)
        item.triggered.connect(self.channel_info)
        main_menu_channel.addAction(item)

        main_menu_message = main_menu.addMenu('Message')
        item = QtGui.QAction("Info", self)
        item.triggered.connect(self.message_info)
        main_menu_message.addAction(item)
        item = QtGui.QAction("Copy", self)
        item.triggered.connect(self.message_copy_content)
        main_menu_message.addAction(item)
        item = QtGui.QAction("Copy ID", self)
        item.triggered.connect(self.message_copy_id)
        main_menu_message.addAction(item)

        main_menu_member = main_menu.addMenu('Member')



        self.message_send_btn = QPushButton("Send", self)
        self.message_send_btn.resize(60,30)
        self.message_send_btn.move(979,670)
        self.message_send_btn.clicked.connect(self.send_message)
        self.message_send_btn.setStyleSheet("color: #dedede; background-color: #222222; border: 1px solid #1e1e1e;")


        self.message_entry = QLineEdit(self)
        self.message_entry.resize(638,30)
        self.message_entry.move(341,670)
        self.message_entry.returnPressed.connect(self.send_message)
        self.message_entry.setFocus()
        self.message_entry.setStyleSheet("color: #dedede; background-color: #2f3136; border: 1px solid #1e1e1e;")

        self.guild_list = QListWidget(self)
        self.guild_list.resize(200,650)
        self.guild_list.move(0,50)
        self.guild_list.itemSelectionChanged.connect(self.select_guild)
        self.guild_list.setStyleSheet("""
            .QListWidget {
                background-color: #202225;
                color: #dedede;
            }
            QListWidget::item:selected
            {
                background: #0a0a0a;
                color: #dedede;
            }
        """)

        self.channel_list = QListWidget(self)
        self.channel_list.resize(140,650)
        self.channel_list.move(200,50)
        self.channel_list.itemSelectionChanged.connect(self.select_channel)
        self.channel_list.setStyleSheet("""
            .QListWidget {
                background-color: #2f3136;
                color: #dedede;
            }
            QListWidget::item:selected
            {
                background: #0a0a0a;
                color: #dedede;
            }
        """)

        self.message_list = QListWidget(self)
        self.message_list.resize(700,620)
        self.message_list.move(340,50)
        self.message_list.itemSelectionChanged.connect(self.select_message)
        self.message_list.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom)
        self.message_list.setStyleSheet("""
            .QListWidget {
                background-color: #36393e;
                color: #dedede;
            }
            QListWidget::item:selected
            {
                background: #0a0a0a;
                color: #dedede;
            }
        """)


        self.member_list = QListWidget(self)
        self.member_list.resize(160,650)
        self.member_list.move(1040,50)
        self.member_list.itemSelectionChanged.connect(self.select_member)
        self.member_list.verticalScrollBar().rangeChanged.connect(self.scroll_to_bottom)
        self.member_list.setStyleSheet("""
            .QListWidget {
                background-color: #2f3136;
                color: #dedede;
            }
            QListWidget::item:selected
            {
                background: #0a0a0a;
                color: #dedede;
            }
        """)

        self.message_label = QLabel("None Selected",self)
        self.message_label.move(340,25)
        self.message_label.resize(700,25)
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setStyleSheet("color: #dedede")
        self.member_label = QLabel("None Selected",self)
        self.member_label.move(1040,25)
        self.member_label.resize(160,25)
        self.member_label.setAlignment(QtCore.Qt.AlignCenter)
        self.member_label.setStyleSheet("color: #dedede")
        self.guild_label = QLabel("None Selected",self)
        self.guild_label.move(0,25)
        self.guild_label.resize(200,25)
        self.guild_label.setAlignment(QtCore.Qt.AlignCenter)
        self.guild_label.setStyleSheet("color: #dedede")
        self.channel_label = QLabel("None Selected",self)
        self.channel_label.move(200,25)
        self.channel_label.resize(140,25)
        self.channel_label.setAlignment(QtCore.Qt.AlignCenter)
        self.channel_label.setStyleSheet("color: #dedede")




        self.message_send_btn.setDisabled(True)
        self.message_entry.setDisabled(True)


        self.show()

    def sync(self,coro):
        asyncio.run_coroutine_threadsafe(coro, asyncio.get_event_loop())

    def select_guild(self):
        if len(self.guild_list.selectedItems()) > 0:
            self.guildid = self.guild_list.selectedItems()[0].data(QtCore.Qt.UserRole)
            self.guild = self.client.get_guild(self.guildid)
            self.guild_label.setText(self.guild.name)
            self.update_channels()
            self.update_members()

    def select_message(self):
        if len(self.message_list.selectedItems()) > 0:
            self.messageid = self.message_list.selectedItems()[0].data(QtCore.Qt.UserRole).id
            self.message = self.message_list.selectedItems()[0].data(QtCore.Qt.UserRole)
            self.message_label.setText(str(self.message.content))

    def select_member(self):
        if len(self.member_list.selectedItems()) > 0:
            self.memberid = self.member_list.selectedItems()[0].data(QtCore.Qt.UserRole)
            self.member = self.guild.get_member(self.memberid)
            self.member_label.setText(self.member.name+"#"+str(self.member.discriminator))

    def select_channel(self):
        if len(self.channel_list.selectedItems()) > 0:
            self.channelid = self.channel_list.selectedItems()[0].data(QtCore.Qt.UserRole)
            self.channel = self.guild.get_channel(self.channelid)
            self.channel_label.setText(self.channel.name)
            perms = self.channel.permissions_for(self.guild.get_member(self.client.user.id))
            if perms.send_messages:
                self.message_send_btn.setDisabled(False)
                self.message_entry.setDisabled(False)
            else:
                self.message_send_btn.setDisabled(True)
                self.message_entry.setDisabled(True)

            self.sync(self.update_messages())

    def update_guilds(self):
        scroll = self.guild_list.verticalScrollBar().value()
        self.guild_list.clear()
        for i in sorted(list(self.client.guilds), key=lambda x: x.name.lower()):
            item = QListWidgetItem(str(i.name))
            item.setData(Qt.UserRole,i.id)
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

    def update_members(self):
        if self.guildid != None:
            self.guild = self.client.get_guild(self.guildid)
            scroll = self.member_list.verticalScrollBar().value()
            self.member_list.clear()
            for i in sorted(list(self.guild.members), key=lambda x: x.roles[-1], reverse=True):
                item = QtGui.QListWidgetItem(str(i))
                item.setData(QtCore.Qt.UserRole,i.id)

                if i.colour.value != 0:
                    item.setForeground(QtGui.QColor(i.colour.value))
                else:
                    item.setForeground(QtGui.QColor(14606046))

                self.member_list.addItem(item)

            self.member_list.verticalScrollBar().setValue(scroll)


    async def update_messages(self):
        if self.channelid != None:
            self.channel = self.guild.get_channel(self.channelid)
            self.message_list.clear()
            async for msg in self.channel.history(reverse=True, limit=500):
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
        if abs(self.message_list.verticalScrollBar().value() - self.message_list.verticalScrollBar().maximum()) < 10 or bypass:
            self.message_list.verticalScrollBar().setValue(self.message_list.verticalScrollBar().maximum())

    def send_message(self):
        self.sync(self.channel.send(self.message_entry.text()))
        self.message_entry.clear()
        self.message_entry.setFocus()

    def message_copy_content(self):
        if self.message != None:
            pyperclip.copy(self.message.content)
    def message_copy_id(self):
        if self.message != None:
            pyperclip.copy(str(self.messageid))
    def message_info(self):
       msg = QtGui.QMessageBox()
       msg.setWindowTitle("Message Info")
       msg.setText("Author: "+str(self.message.author))
       msg.setInformativeText("ID: "+str(self.message.id))
       msg.setDetailedText("Content: "+self.message.content+"\n\nTimestamp: "+str(self.message.created_at)+"\n\nPinned: "+str(self.message.pinned))
       msg.setStandardButtons(QtGui.QMessageBox.Ok)
       msg.exec_()

    def channel_info(self):
       msg = QtGui.QMessageBox()
       msg.setWindowTitle("Channel Info")
       msg.setText("Name: "+str(self.channel.name))
       msg.setInformativeText("ID: "+str(self.channel.id))
       msg.setDetailedText("Server: "+str(self.channel.guild)+"\n\nTopic: "+str(self.channel.topic)+"\n\nCreated: "+str(self.channel.created_at))
       msg.setStandardButtons(QtGui.QMessageBox.Ok)
       msg.exec_()

    def guild_info(self):
       msg = QtGui.QMessageBox()
       msg.setWindowTitle("Guild Info")
       msg.setText("Name: "+str(self.guild.name))
       msg.setInformativeText("ID: "+str(self.guild.id))
       msg.setDetailedText("Owner: "+str(self.guild.owner)+"\n\nMembers: "+str(len(self.guild.members))+"\n\nLarge: "+str(self.guild.large)+"\n\nChannels: "+str(len(self.guild.channels))+"\n\nCreated: "+str(self.guild.created_at))
       msg.setStandardButtons(QtGui.QMessageBox.Ok)
       msg.exec_()


    def ready(self):
        self.update_guilds()

if __name__ == "__main__":
    import main
