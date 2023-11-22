import tkinter as tk
import customtkinter as ctk
from client import *


app = ctk.CTk()
def setup():
    ctk.set_appearance_mode('dark')
    ctk.set_default_color_theme('blue')
    app.title('ClientUI')
    app.geometry('800x400')

#tabView = ctk.CTkTabview


login_Frame = ctk.CTkFrame(master=app,
                           width=800,
                           height=200,
                           bg_color='black')
login_Frame.pack(padx=10, pady=10, expand=True, fill="both", side="left")

# serverIP_Label = ctk.CTkLabel(master = app,
#                               text = 'Server IP:',
#                               width = 80,
#                               height = 25,
#                               text_color = 'white',
#                               corner_radius = 8)
# serverIP_Label.place(x=30, y=20)

serverIP_Entry = ctk.CTkEntry(master=login_Frame,
                              placeholder_text='Server IP',
                              width=200,
                              height=30,
                              text_color='white',
                              corner_radius=10)
serverIP_Entry.configure(state='normal')
serverIP_Entry.place(x=120, y=20)

hostname_Entry = ctk.CTkEntry(master=login_Frame,
                              placeholder_text='Hostname',
                              width=200,
                              height=30,
                              text_color='white',
                              corner_radius=10)
hostname_Entry.configure(state='normal')
hostname_Entry.place(x=120, y=60)

SIZE = 1024
REPOSITORY_PATH = 'repository/'
FORMAT = 'utf-8'

client = Client('',0,'')

def start_connect():
    SERVER_IP = serverIP_Entry.get()
    SERVER_PORT = 4869
    hostname = hostname_Entry.get()
    client = Client(SERVER_IP, SERVER_PORT, hostname)
    client.start()

# def disconnect():
    # client.disconnect(client.client_socket, client.server_IP, client.server_Port)


# SERVER_IP = input("Enter Server's IP: ")
# SERVER_PORT = 4869


# hostname = str(serverIP_Textbox.get('0.0', 'end'))
# print(hostname)
# client = Client(SERVER_IP, SERVER_PORT, hostname)

connect_Button = ctk.CTkButton(master=app, text='Connect', command=start_connect)
connect_Button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

# disconnect_Button = ctk.CTkButton(master=app, text='Disconnect', command=client.disconnect)
# disconnect_Button.place(relx=0.8, rely=0.7, anchor=tk.CENTER)
if __name__ == '__main__':
    setup()
    app.mainloop()