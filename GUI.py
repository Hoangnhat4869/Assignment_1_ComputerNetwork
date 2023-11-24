# import tkinter as tk
# import customtkinter as ctk
# from client import *


# app = ctk.CTk()
# def setup():
#     ctk.set_appearance_mode('dark')
#     ctk.set_default_color_theme('blue')
#     app.title('ClientUI')
#     app.geometry('800x400')

# #tabView = ctk.CTkTabview


# login_Frame = ctk.CTkFrame(master=app,
#                            width=800,
#                            height=200,
#                            bg_color='black')
# login_Frame.pack(padx=10, pady=10, expand=True, fill="both", side="left")

# # serverIP_Label = ctk.CTkLabel(master = app,
# #                               text = 'Server IP:',
# #                               width = 80,
# #                               height = 25,
# #                               text_color = 'white',
# #                               corner_radius = 8)
# # serverIP_Label.place(x=30, y=20)

# serverIP_Entry = ctk.CTkEntry(master=login_Frame,
#                               placeholder_text='Server IP',
#                               width=200,
#                               height=30,
#                               text_color='white',
#                               corner_radius=10)
# serverIP_Entry.configure(state='normal')
# serverIP_Entry.place(x=120, y=20)

# hostname_Entry = ctk.CTkEntry(master=login_Frame,
#                               placeholder_text='Hostname',
#                               width=200,
#                               height=30,
#                               text_color='white',
#                               corner_radius=10)
# hostname_Entry.configure(state='normal')
# hostname_Entry.place(x=120, y=60)

# SIZE = 1024
# REPOSITORY_PATH = 'repository/'
# FORMAT = 'utf-8'

# client = Client('',0,'')

# def start_connect():
#     SERVER_IP = serverIP_Entry.get()
#     SERVER_PORT = 4869
#     hostname = hostname_Entry.get()
#     client = Client(SERVER_IP, SERVER_PORT, hostname)
#     client.start()


# # def disconnect():
#     # client.disconnect(client.client_socket, client.server_IP, client.server_Port)


# # SERVER_IP = input("Enter Server's IP: ")
# # SERVER_PORT = 4869


# # hostname = str(serverIP_Textbox.get('0.0', 'end'))
# # print(hostname)
# # client = Client(SERVER_IP, SERVER_PORT, hostname)

# connect_Button = ctk.CTkButton(master=app, text='Connect', command=start_connect)
# connect_Button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# # disconnect_Button = ctk.CTkButton(master=app, text='Disconnect', command=client.disconnect)
# # disconnect_Button.place(relx=0.8, rely=0.7, anchor=tk.CENTER)
# if __name__ == '__main__':
#     setup()
#     app.mainloop()

import tkinter as tk
import customtkinter as ctk
from client import *
import threading
import time
from tkinter import filedialog
import os
from tkinter import messagebox

SIZE = 1024
REPOSITORY_PATH = 'repository/'
FORMAT = 'utf-8'

class MyApp:
    def __init__(self):
        self.app = ctk.CTk()
        self.client =  Client('',0,'')
        self.UIobject()

    def setup(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('blue')
        self.app.title('ClientUI')
        self.app.geometry('800x400')


    def UIobject(self):
        self.login_Frame = ctk.CTkFrame(master=self.app,
                            width=800,
                            height=200,
                            bg_color='black')
        self.login_Frame.pack(padx=10, pady=10, expand=True, fill="both", side="left")


        self.serverIP_Entry = ctk.CTkEntry(master=self.login_Frame,
                                    placeholder_text='Server IP',
                                    width=200,
                                    height=30,
                                    text_color='white',
                                    corner_radius=10)
        self.serverIP_Entry.configure(state='normal')
        self.serverIP_Entry.place(x=120, y=20)

        self.hostname_Entry = ctk.CTkEntry(master=self.login_Frame,
                                    placeholder_text='Hostname',
                                    width=200,
                                    height=30,
                                    text_color='white',
                                    corner_radius=10)
        self.hostname_Entry.configure(state='normal')
        self.hostname_Entry.place(x=120, y=60)

        

        self.connect_Button = ctk.CTkButton(master=self.app, text='Connect', command=self.start_connect)
        self.connect_Button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    

    def start_connect(self):
        SERVER_IP = self.serverIP_Entry.get()
        SERVER_PORT = 4869
        hostname = self.hostname_Entry.get()

        if not SERVER_IP or not hostname:
            # Handle empty fields
            print("Please enter both Server IP and Hostname.")
            return

        self.client = Client(SERVER_IP, SERVER_PORT, hostname)
        self.client.start()
        time.sleep(1)
        
        # Hide the login frame
        self.login_Frame.pack_forget()

        self.show_repository_frame()

    

    def show_repository_frame(self):
        # Create a new frame for repository display
        self.repo_frame = ctk.CTkFrame(master=self.app, width=800, height=400, bg_color='black')
        self.repo_frame.pack(padx=10, pady=10, expand=True, fill="both", side="left")

        # Add labels, lists, or any other widgets to display the repositories
        # Customize this based on your repository data structure

        # Example label
        self.font1 = ('Arial',20,'bold')
        self.font2 = ('Arial',15,'bold')
        self.font3 = ('Arial',10,'bold')
        self.user_repo_label = ctk.CTkLabel(master=self.repo_frame,font=self.font1, text='File Sharing', text_color='white')
        self.user_repo_label.pack()

        self.publish_button = ctk.CTkButton(master=self.repo_frame, 
                                            font=self.font2, text_color='white', 
                                            text='Publish', fg_color='#06911f', 
                                            hover_color='#06911f', 
                                            bg_color = '#09112e', 
                                            cursor= 'hand2', corner_radius=5, width=120, command=self.openFile)
        self.publish_button.place(x=300, y=80)

        self.repo_list = tk.Listbox(master=self.repo_frame,width=40, height=15, font=self.font3)
        # repo_list.place(x=40, y=80)
        self.repo_list.pack(anchor='w')

        path = os.getcwd()
        newpath = path + '/repository'
        repo_filename = os.listdir(newpath)
        
        for filename in repo_filename:
            self.repo_list.insert(tk.END,filename)
        

        self.quit_Button = ctk.CTkButton(master=self.repo_frame, text='Quit', command=self.quitCli)
        self.quit_Button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
        
        self.fetch_Entry = ctk.CTkEntry(master=self.repo_frame,
                                    placeholder_text='File name',
                                    width=200,
                                    height=30,
                                    text_color='white',
                                    corner_radius=10)
        self.fetch_Entry.configure(state='normal')
        self.fetch_Entry.place(x=400, y=200)

        self.fetch_button = ctk.CTkButton(master=self.repo_frame, 
                                            font=self.font2, text_color='white', 
                                            text='Fetch', fg_color='#06911f', 
                                            hover_color='#06911f', 
                                            bg_color = '#09112e', 
                                            cursor= 'hand2', corner_radius=5, width=120, command=self.fetchFile)
        self.fetch_button.place(x=300, y=120)
            

    def openFile(self): 
        filepath = filedialog.askopenfilename()
        # print(filepath.split('/')[-1:])
        directory, filename = os.path.split(filepath)
        print(directory)
        print(filename)
        self.client.publish(directory,filename)
        self.repo_list.insert(tk.END,filename)

    def quitCli(self):
        self.app.withdraw()
        self.client.quitCli()
    
    def fetchFile(self):
        if self.fetch_Entry.get() == '':
            messagebox.showinfo("Error", "Please enter file name!")
        else:
            msg = self.client.fetch(self.fetch_Entry.get())
            if msg == 'These are clients having the file:':
                self.repo_list.insert(tk.END,self.fetch_Entry.get())
                messagebox.showinfo("Success", "Done fetch file!")
            else:
                messagebox.showerror("Error",msg)



if __name__ == '__main__':
    app = MyApp()
    app.setup()
    app.app.mainloop()
