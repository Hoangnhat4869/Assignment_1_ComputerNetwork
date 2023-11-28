import tkinter as tk
import customtkinter as ctk
from server import *
import threading
from PIL import Image
import time
from tkinter import filedialog
import os
import re
from CTkListbox import *


SERVER_IP = get_local_ip()
SERVER_PORT = 4869

SIZE = 1024
FORMAT = 'utf-8'


class ServerUI:
    def __init__(self):
        self.app = ctk.CTk()
        self.server = Server(SERVER_IP, SERVER_PORT)
        self.tinyFont = ctk.CTkFont('Lucida Sans Unicode', 12, 'bold')
        self.smallFont = ctk.CTkFont('Lucida Sans Unicode', 15, 'bold')
        self.mediumFont = ctk.CTkFont('Lucida Sans Unicode', 20, 'bold')
        self.bigFont = ctk.CTkFont('Lucida Sans Unicode', 25, 'bold')
        #self.ClientListName = list()
        self.setup_app()
        self.display_main()

    
    def setup_app(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')
        self.app.title('Server')
        self.app.geometry('800x500')
        threading.Thread(target=self.start_server).start()
        self.create_object()


    def create_object(self):
        self.MainFrame = ctk.CTkFrame(self.app, 800, 500, fg_color='#527a7a', corner_radius=10)
        self.AppTitle = ctk.CTkLabel(self.MainFrame, text='File-Sharing Application', font=self.bigFont,
                                      text_color='black', corner_radius=15)
        self.ServerInfo = ctk.CTkLabel(self.app, text='Server IP: ' + get_local_ip(), font=self.mediumFont,
                                       text_color='black', fg_color='#527a7a', bg_color='#527a7a')
        self.ClientListBox = CTkListbox(self.MainFrame, fg_color='#333333', corner_radius=10, border_width=3, text_color='white',
                                   hover_color='#75a3a3', font=self.smallFont, select_color='#527a7a')
        self.IPHeader = ctk.CTkLabel(self.MainFrame, fg_color='#333333',
                                     text='Client IP', font=self.smallFont, text_color='white')
        self.NameHeader = ctk.CTkLabel(self.MainFrame, fg_color='#333333',
                                       text='Client Name', font=self.smallFont, text_color='white')
        self.RepoList = CTkListbox(self.MainFrame, fg_color='#333333', corner_radius=1, border_width=3, text_color='white',
                                   hover_color='#75a3a3', font=self.tinyFont, select_color='#527a7a')
        self.PingButton = ctk.CTkButton(self.MainFrame, fg_color='#e60000', corner_radius=5, text_color='white',
                                        text='PING', font=self.mediumFont, hover_color='#800000', command=self.ping)
        self.DiscoverButton = ctk.CTkButton(self.MainFrame, fg_color='#333399', corner_radius=5, text_color='white',
                                        text='DISCOVER', font=self.mediumFont, hover_color='#19194d', command=self.discover)
        self.RefreshButton = ctk.CTkButton(self.NameHeader, 20, 20, fg_color='#333333', text='',
                                            hover_color='#666666', command=self.update_client_listbox)

    def display_main(self):
        self.MainFrame.place(relwidth=0.95, relheight=0.95, relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.AppTitle.place(relwidth=0.8, relheight=0.15, relx=0.5, rely=0.08, anchor=ctk.CENTER)
        self.ServerInfo.place(relx=0.25, rely=0.2, anchor=ctk.CENTER)
        self.ClientListBox.place(relwidth=0.5, relheight=0.6, relx=0.3, rely=0.65, anchor=ctk.CENTER)
        self.IPHeader.place(relwidth=0.22, relheight=0.08, relx=0.16, rely=0.3, anchor=ctk.CENTER)
        self.NameHeader.place(relwidth=0.32, relheight=0.08, relx=0.39, rely=0.3, anchor=ctk.CENTER)
        self.RefreshButton.configure(image=ctk.CTkImage(Image.open('Refresh.png'), size=(20,20)))
        self.RefreshButton.place(relwidth=0.15, relheight=0.8, relx=0.9, rely=0.5, anchor=ctk.CENTER)
        self.RepoList.place(relwidth=0.35, relheight=0.4, relx=0.77, rely=0.75, anchor=ctk.CENTER)
        self.PingButton.place(relwidth=0.16, relheight=0.08, relx=0.68, rely=0.3, anchor=ctk.CENTER)
        self.DiscoverButton.place(relwidth=0.16, relheight=0.08, relx=0.87, rely=0.3, anchor=ctk.CENTER)


    def ping(self):
        client = self.ClientListBox.get()
        if client == None:
            msg = 'Please select the client to ping!'
            MessageLabel = ctk.CTkLabel(self.MainFrame, text=msg, text_color='#991f00', font=self.tinyFont)
        else:
            hostname = client.split('\t')[-1]
            status = self.server.ping(hostname)
            if status == 'ONLINE':
                MessageLabel = ctk.CTkLabel(self.MainFrame, text=f'{hostname}: {status}', text_color='white', fg_color='green', font=self.mediumFont)
            else:
                MessageLabel = ctk.CTkLabel(self.MainFrame, text=f'{hostname}: {status}', text_color='white', fg_color='red', font=self.mediumFont)
        
        MessageLabel.place(relx=0.77, rely=0.43, anchor=ctk.CENTER)
        MessageLabel.after(2000, lambda: MessageLabel.place_forget())


    def discover(self):
        client = self.ClientListBox.get()
        if client == None:
            msg = 'Please select the client to discover!'
            MessageLabel = ctk.CTkLabel(self.MainFrame, text=msg, text_color='#991f00', font=self.tinyFont)
            MessageLabel.place(relx=0.77, rely=0.43, anchor=ctk.CENTER)
            MessageLabel.after(2000, lambda: MessageLabel.place_forget())
        else:
            hostname = client.split('\t')[-1]
            repoLabel = ctk.CTkLabel(self.MainFrame, text=hostname + "'s Repository", text_color='#991f00',
                                      font=self.smallFont, fg_color='#527a7a')
            repoLabel.place(relx=0.77, rely=0.5, anchor=ctk.CENTER)
            listFile = self.server.discover(hostname)
            if self.RepoList.size():
                self.RepoList.delete(0,'END')
            for file in listFile:
                self.RepoList.insert('END',file)


    def update_client_listbox(self):
        if self.ClientListBox.size():
            self.ClientListBox.delete(0,'END')
        for hostname in self.server.connectedClient:
            value = self.server.connectedClient[hostname][0] + '\t\t' + hostname
            self.ClientListBox.insert('END', value)


    def start_server(self):
        self.server.start()



if __name__ == '__main__':
    UI = ServerUI()
    UI.app.mainloop()