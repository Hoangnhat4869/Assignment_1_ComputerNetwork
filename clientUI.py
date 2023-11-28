import tkinter as tk
import customtkinter as ctk
from client import *
import threading
from PIL import Image
import time
from tkinter import filedialog
import os
import re
from CTkListbox import *


SIZE = 1024
REPOSITORY_PATH = 'repository/'
FORMAT = 'utf-8'

def validate_ip_address(ip_address):
    # Format of IP address
    text = r"^([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})$"

    # Check if ip_address is valid?
    if re.match(text, ip_address):
        return True
    else:
        return False

class ClientUI:
    def __init__(self):
        self.app = ctk.CTk()
        self.client = Client('', 0, '')
        self.tinyFont = ctk.CTkFont('Lucida Sans Unicode', 12, 'bold')
        self.smallFont = ctk.CTkFont('Lucida Sans Unicode', 15, 'bold')
        self.mediumFont = ctk.CTkFont('Lucida Sans Unicode', 20, 'bold')
        self.bigFont = ctk.CTkFont('Lucida Sans Unicode', 25, 'bold')
        self.setup_app()
        self.start_login()


    def setup_app(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')
        self.app.title('Client')
        self.app.geometry('800x500')
        self.create_object()
        #self.display_main()


    def create_object(self):

        # Login Page
        self.LoginFrame = ctk.CTkFrame(self.app, 700, 400, fg_color='#b3cccc', corner_radius=0)
        # Objects
        self.EntryFrame = ctk.CTkFrame(self.LoginFrame, 350, 200, fg_color='#b3cccc', corner_radius=15, border_width=2, border_color='white')
        self.AppTitleLogin = ctk.CTkLabel(self.LoginFrame, text='File-Sharing Application', font=self.bigFont,
                                      text_color='black', corner_radius=15)
        self.AppIcon = ctk.CTkLabel(self.LoginFrame, 70, 70, fg_color='#75a3a3', text='', corner_radius=15)
        self.ServerIPLabel = ctk.CTkLabel(self.LoginFrame, 100, 30, text='SERVER IP', font=self.smallFont, 
                                          text_color='black')
        self.ServerIPEntry = ctk.CTkEntry(self.LoginFrame, 200, 30,
                                    corner_radius=10, placeholder_text='Server IP', text_color='white')
        self.HostnameLabel = ctk.CTkLabel(self.LoginFrame, 100, 30, text='HOSTNAME', font=self.smallFont,
                                          text_color='black')
        self.HostnameEntry = ctk.CTkEntry(self.LoginFrame, 200, 30,
                                    corner_radius=10, placeholder_text='Hostname', text_color='white')
        self.connect_Button = ctk.CTkButton(self.LoginFrame, text='Connect', command=self.connect, fg_color='#3d5c5c')

        #############################################

        # Main Page
        self.MainFrame = ctk.CTkFrame(self.app, 700, 400, fg_color='#75a3a3', corner_radius=0)
        # Objects
        self.Avatar = ctk.CTkLabel(self.MainFrame, 60, 60, text='')
        self.AppTitleMain = ctk.CTkLabel(self.MainFrame, text='File-Sharing Application', font=self.mediumFont,
                                      text_color='black', corner_radius=15)
        self.PublishButton = ctk.CTkButton(self.MainFrame, text='UPLOAD', command=self.upload, 
                                           fg_color='#3d5c5c', font=self.smallFont)
        self.FetchButton = ctk.CTkButton(self.MainFrame, text='DOWNLOAD', command=self.download, 
                                         fg_color='#3d5c5c', font=self.smallFont)
        self.ViewRepoButton = ctk.CTkButton(self.MainFrame, text='MY REPOSITORY', command=self.view_repo, 
                                            fg_color='#3d5c5c', font=self.smallFont)
        self.ViewServerButton = ctk.CTkButton(self.MainFrame, text='SERVER FILES', command=self.view_server, 
                                            fg_color='#3d5c5c', font=self.smallFont)
        
        ############################################

        # My Repository
        self.RepoFrame = ctk.CTkFrame(self.MainFrame, 550, 300, fg_color='#b3cccc', corner_radius=10)
        # Objects
        self.RepoTitle = ctk.CTkLabel(self.RepoFrame, fg_color='#b3cccc', text='My Repository', text_color='black', font=self.mediumFont)
        self.RepoList = CTkListbox(self.RepoFrame, fg_color='#333333', corner_radius=1, border_width=3, text_color='white',
                                   hover_color='#75a3a3', font=self.smallFont, select_color='#527a7a')

        # DeleteFile Button
        self.DeleteFileButton = ctk.CTkButton(self.RepoFrame, text='Delete Selected File', command=self.deleteFile, 
                                            fg_color='#b30000', font=self.smallFont)

        ###########################################

        # Server Files
        self.ServerFileFrame = ctk.CTkFrame(self.MainFrame, 550, 300, fg_color='#b3cccc', corner_radius=10)
        # Objects
        self.ServerFileTitle = ctk.CTkLabel(self.ServerFileFrame, fg_color='#b3cccc', text='Server Files', 
                                            text_color='black', font=self.mediumFont)
        self.ServerFileList = CTkListbox(self.ServerFileFrame, fg_color='#333333', corner_radius=1, border_width=3, text_color='white',
                                   hover_color='#75a3a3', font=self.smallFont, select_color='#527a7a')
        
        # Download button
        self.DownFileButton = ctk.CTkButton(self.ServerFileFrame, text='FETCH', command=self.fetch_file, 
                                            fg_color='#3d5c5c', font=self.smallFont)
        
        # Disconnect button
        self.DisconnectButton = ctk.CTkButton(self.MainFrame, text='DISCONNECT', command=self.disconnect, 
                                            fg_color='#b30000', font=self.smallFont)
        

    # UI

    def start_login(self):
        self.MainFrame.place_forget()
        self.LoginFrame.place(relwidth=0.96, relheight=0.96, relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.EntryFrame.place(relwidth=0.55, relheight=0.5, relx=0.5, rely=0.7, anchor=ctk.CENTER)
        self.AppTitleLogin.place(relwidth = 0.8, relheight=0.2, relx=0.5, rely=0.13, anchor=ctk.CENTER)
        self.AppIcon.configure(image=ctk.CTkImage(Image.open('FileSharingIcon.png'), size=(70,70)))
        self.AppIcon.place(relwidth=0.15, relheight=0.2, relx=0.5, rely=0.3, anchor=ctk.CENTER)
        self.ServerIPLabel.place(relwidth=0.2, relheight=0.08, relx=0.35, rely=0.55, anchor=ctk.CENTER)
        self.ServerIPEntry.configure(state='normal')
        self.ServerIPEntry.place(relwidth=0.25, relheight=0.08, relx=0.55, rely=0.55, anchor=ctk.CENTER)
        self.HostnameLabel.place(relwidth=0.2, relheight=0.08, relx=0.35, rely=0.68, anchor=ctk.CENTER)
        self.HostnameEntry.configure(state='normal')
        self.HostnameEntry.place(relwidth=0.25, relheight=0.08, relx=0.55, rely=0.68, anchor=ctk.CENTER)
        self.connect_Button.place(relwidth=0.15, relheight=0.06, relx=0.5, rely=0.85, anchor=ctk.CENTER)

    
    def display_main(self):
        # Frames and Title
        self.MainFrame.place(relwidth=1, relheight=1, relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.AppTitleMain.place(relwidth=0.72, relheight=0.15, relx=0.64, rely=0.075, anchor=ctk.CENTER)
        self.RepoFrame.place(relwidth=0.7, relheight=0.76, relx=0.63, rely=0.58, anchor=ctk.CENTER)

        # Client Info
        self.Avatar.configure(image=ctk.CTkImage(Image.open('avatar.png'), size=(50,50)))
        self.Avatar.place(relx=0.07, rely=0.15, anchor=ctk.CENTER)
        self.HostnameDis = ctk.CTkLabel(self.MainFrame, 80, 15, fg_color='#75a3a3', 
                                        text='Hostname: ' + self.client.hostname, text_color='black', font=self.tinyFont)
        self.IPDis = ctk.CTkLabel(self.MainFrame, 80, 15, fg_color='#75a3a3', text='IP: ' + get_local_ip(),
                                  text_color='black', font=self.tinyFont)
        self.ServerIPDis = ctk.CTkLabel(self.MainFrame, 80, 15, fg_color='#75a3a3', text='ServerIP: ' + self.client.server_IP,
                                  text_color='black', font=self.tinyFont)
        self.HostnameDis.place(relx=0.2, rely=0.13, anchor=ctk.CENTER)
        self.IPDis.place(relx=0.2, rely=0.17, anchor=ctk.CENTER)
        self.ServerIPDis.place(relx=0.14, rely=0.95, anchor=ctk.CENTER)

        # Buttons
        self.PublishButton.place(relwidth=0.2, relheight=0.08, relx=0.14, rely=0.3, anchor=ctk.CENTER)
        self.FetchButton.place(relwidth=0.2, relheight=0.08, relx=0.14, rely=0.43, anchor=ctk.CENTER)
        self.ViewRepoButton.place(relwidth=0.2, relheight=0.08, relx=0.14, rely=0.56, anchor=ctk.CENTER)
        self.ViewServerButton.place(relwidth=0.2, relheight=0.08, relx=0.14, rely=0.69, anchor=ctk.CENTER)
        self.DisconnectButton.place(relwidth=0.16, relheight=0.07, relx=0.14, rely=0.85, anchor=ctk.CENTER)

        self.view_repo()


    # Functions for buttons

    def connect(self):
        SERVER_IP = self.ServerIPEntry.get()
        SERVER_PORT = 4869
        hostname = self.HostnameEntry.get()
        if not SERVER_IP or not hostname:
            # Handle empty fields
            self.WarningLabel = ctk.CTkLabel(self.LoginFrame, text='Please enter both Server IP and Hostname.',
                                              text_color='red', font=self.tinyFont)
            self.WarningLabel.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)
            return
        
        if not validate_ip_address(SERVER_IP):
            # Handle invalid IP address
            self.WarningLabel = ctk.CTkLabel(self.LoginFrame, text='Server IP is not valid.',
                                              text_color='red', font=self.tinyFont)
            self.WarningLabel.place(relx=0.5, rely=0.75, anchor=ctk.CENTER)
            return

        self.client = Client(SERVER_IP, SERVER_PORT, hostname)
        if (self.client.start() == False):
            return
        time.sleep(0.5)
        
        # Hide the LoginFrame
        self.LoginFrame.pack_forget()
        # Display the MainFrame
        self.display_main()


    def upload(self):
        filePath = filedialog.askopenfilename()
        lname, fname = os.path.split(filePath)
        cmd, msg = self.client.publish(lname, fname)
        if cmd == 'OK':
            MessageLabel = ctk.CTkLabel(self.MainFrame, text=msg, text_color='green', font=self.tinyFont)
            self.client.allFile.append(fname)
        else:
            MessageLabel = ctk.CTkLabel(self.MainFrame, text=msg, text_color='red', font=self.tinyFont)
        MessageLabel.place(relx=0.14, rely=0.78, anchor=ctk.CENTER)
        MessageLabel.after(3000, lambda:MessageLabel.place_forget())
        
        # Update Repository after uploading
        self.update_RepoList()
        self.view_repo()


    def download(self):
        self.view_server()
        self.DownFileButton.place(relwidth=0.2, relheight=0.08, relx=0.5, rely=0.9, anchor=ctk.CENTER)


    def view_repo(self):
        self.ServerFileFrame.place_forget()
        self.update_RepoList()
        self.RepoFrame.place(relwidth=0.7, relheight=0.76, relx=0.63, rely=0.58, anchor=ctk.CENTER)
        self.RepoTitle.place(relwidth=0.8, relheight=0.2, relx=0.5, rely=0.1, anchor=ctk.CENTER)
        self.RepoList.place(relwidth=0.8, relheight=0.6, relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.DeleteFileButton.place(relx=0.5, rely=0.9, anchor=ctk.CENTER)


    def view_server(self):
        self.RepoFrame.place_forget()
        self.DownFileButton.place_forget()
        self.update_ServerFileList()
        self.ServerFileFrame.place(relwidth=0.7, relheight=0.76, relx=0.63, rely=0.58, anchor=ctk.CENTER)
        self.ServerFileTitle.place(relwidth=0.8, relheight=0.2, relx=0.5, rely=0.1, anchor=ctk.CENTER)
        self.ServerFileList.place(relwidth=0.8, relheight=0.6, relx=0.5, rely=0.5, anchor=ctk.CENTER)


    def deleteFile(self):
        fName = self.RepoList.get()
        if fName == None:
            msg = 'Please select a file to delete!'
            MessageLabel = ctk.CTkLabel(self.RepoFrame, text=msg, text_color='red', font=self.tinyFont)
        else:
            self.client.deleteFile(self.RepoList.get())
            self.RepoList.delete(self.RepoList.curselection())
            self.client.allFile.remove(self.RepoList.curselection())
            msg = fName + ' deleted successfully!'
            MessageLabel = ctk.CTkLabel(self.RepoFrame, text=msg, text_color='green', font=self.tinyFont)
        
        MessageLabel.place(relx=0.5, rely=0.98, anchor=ctk.CENTER)
        MessageLabel.after(3000, lambda:MessageLabel.place_forget())


    def fetch_file(self):
        fName = self.ServerFileList.get()
        if fName == None:
            msg = 'Please select a file to fetch!'
            MessageLabel = ctk.CTkLabel(self.ServerFileFrame, text=msg, text_color='red', font=self.tinyFont)
        else:
            self.client.fetch(self.ServerFileList.get())
            self.RepoList.insert('END', self.ServerFileList.get())
            msg = 'Fetch ' + fName + f' successfully!'
            MessageLabel = ctk.CTkLabel(self.RepoFrame, text=msg, text_color='green', font=self.tinyFont)
        
        MessageLabel.place(relx=0.5, rely=0.98, anchor=ctk.CENTER)
        MessageLabel.after(3000, lambda:self.MessageLabel.place_forget())


    def disconnect(self):
        self.client.disconnect(self.client.client_socket, self.client.server_IP, self.client.server_Port)
        self.client.isConnected = False
        self.client.client_server.close()
        self.start_login()

    # Others functions

    def update_RepoList(self):
        if self.RepoList.size():
            self.RepoList.delete(0,'END')
        filePath = os.path.join(os.getcwd(), REPOSITORY_PATH)
        for fileName in os.listdir(filePath):
            self.RepoList.insert('END',fileName)


    def update_ServerFileList(self):
        self.client.GetAllFile()
        if self.ServerFileList.size():
            self.ServerFileList.delete(0,'END')
        for fileName in self.client.allFile:
            self.ServerFileList.insert('END',fileName)


if __name__ == '__main__':
    UI = ClientUI()
    UI.app.mainloop()