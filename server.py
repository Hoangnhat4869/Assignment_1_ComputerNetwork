import socket as sk
import threading
import time
import os

def get_local_ip():
    s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    try:
        s.connect(('192.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
 
SERVER_IP = get_local_ip()
SERVER_PORT = 4869
#SERVER_IP = sk.gethostbyname(sk.gethostname())

SIZE = 1024
FORMAT = 'utf-8'

class Server:
    def __init__(self, ip, port):
        self.server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.server_ip = ip
        self.server_port = port
        self.server.bind((ip, port))
        self.server.listen()
        self.onlineClient = dict()
        self.connectedClientAdd = dict()
        self.connectedClientName = dict()
        self.clientFileList = dict()

    def start(self):
        print(f"Server is listening on {self.server_ip}:{self.server_port}")
        while True:
            threading.Thread(target=self.start_request).start()
            
            client_socket, client_address = self.server.accept()
            client_name = client_socket.recv(SIZE).decode(FORMAT)
            print('\nClient ' + client_name + f' (IP Address: {client_address}) connected.')
            self.connectedClientAdd[client_name] = client_address
            self.connectedClientName[client_address] = client_name
            if client_name not in self.clientFileList:
                self.clientFileList[client_name] = []
            client_socket.send('_'.encode(FORMAT))
            self.onlineClient[client_name] = client_address

            threading.Thread(target=self.handle_client, args=(client_socket, client_address, client_name)).start()
            time.sleep(1)
            

    def start_request(self):
        while True:
            self.server_option()


    def server_option(self):
        print('\nEnter your command:\n> discover `hostname`: discover the list of local files of hostname\n> ping `hostname`: live check hostname')
        option = input('\nYour command: ')
        if option.startswith('discover'):
            print(self.discover(option.split(' ')[1]))
        elif option.startswith('ping'):
            print(self.ping(option.split(' ')[1]))


    def handle_client(self, client_socket, client_address, client_name):
        while True:
            
            # Receive client's requests
            try:
                client_request = client_socket.recv(SIZE).decode(FORMAT)
            except:
                print('Waiting for a request...')

            client_command, client_message = client_request.split('@')         # Client request in format `cmd@msg`
            
            if client_command != 'DISCONNECT':
                print(f"\n[{client_address}]Client's request: [{client_command}]", client_message)

            if client_command == 'PUBLISHALL':
                fileName = client_message.split(':')
                fileName = fileName[:-1]
                if client_name in self.clientFileList:
                    self.clientFileList[client_name] = []
                    for file in fileName:
                        self.clientFileList[client_name].append(file)
                else:
                    self.clientFileList[client_name] = fileName
                
                cmd = 'OK'
                msg = 'Uploaded successfully!'
                
                self.send_message(client_socket, cmd, msg)
                print(msg)

            elif client_command == 'PUBLISH':
                fileName = client_message
                if client_name in self.clientFileList:
                    self.clientFileList[client_name].append(fileName)
                else:
                    self.clientFileList[client_name] = [fileName]
                
                cmd = 'OK'
                msg = 'Uploaded successfully!'
                
                self.send_message(client_socket, cmd, msg)
                print(msg)
                
            elif client_command == 'FETCH':
                fileName = client_message
                curClientList = list()
                curClientList.clear()
                for cli in self.clientFileList:
                    if fileName in self.clientFileList[cli]:
                        curClientList.append(cli)
                if curClientList:
                    self.send_message(client_socket, 'OK', 'These are clients having the file:')
                    for client in curClientList:
                        add = self.connectedClientAdd[client]
                        status = 'Offline'
                        if client in self.onlineClient:
                            status = 'Online'
                        res = add[0] + ':' + str(add[1]) + ':' + client + ':' + status
                        client_socket.send(res.encode(FORMAT))
                        _ = client_socket.recv(SIZE).decode(FORMAT)
                    
                    self.send_message(client_socket, 'DONE', 'All clients are sent.')
                    self.clientFileList[client_name].append(fileName)
                    print(f'All clients are sent to [{client_name}]')
                else:
                    self.send_message(client_socket, 'ERROR', 'Filename does not exist on server.')
                    print('Filename does not exist.')

            elif client_command == 'ERROR':
                print(client_message)

            elif client_command == 'DELETE':
                fileName = client_message
                self.clientFileList[client_name].remove(fileName)
                self.send_message(client_socket, 'OK', 'Deleted successfully!')
                print('Deleted successfully!')

            elif client_command == 'GETALL':
                allFile = list()
                for cli in self.clientFileList:
                    for fileName in self.clientFileList[cli]:
                        if fileName not in allFile:
                            allFile.append(fileName)
                
                for file in allFile:
                    client_socket.send(file.encode(FORMAT))
                    _ = client_socket.recv(SIZE).decode(FORMAT)
                self.send_message(client_socket, 'DONE?', 'All files are sent.')
                print(f'All files are sent to [{client_name}]')

            else:
                print(f'Client {client_name} disconnected.')
                self.onlineClient.pop(client_name)
                client_socket.close()
                break
    
    def send_message(self, client_socket, cmd, msg):
        respond = cmd + '@' + msg
        client_socket.send(respond.encode(FORMAT))

    def ping(self, hostname = ''):
        if hostname not in self.connectedClientAdd:
            return 'This host has not connected to server yet.'
        else:
            if hostname in self.onlineClient:
                output = 'ONLINE'
            else:
                output = 'OFFLINE'
            return output

    # def ping(self, hostname):
    #     if hostname not in self.connectedClientAdd:
    #         return 'This host has not connected to server yet.'
    #     else:
    #         add = self.connectedClientAdd[hostname]
    #         respond = os.system(f'ping -w 1 {add[0]}')
    #         if respond == 0:
    #             output = 'ONLINE'
    #         else:
    #             if hostname in self.onlineClient:
    #                 self.onlineClient.pop(hostname)
    #             output = 'OFFLINE'
    #         return output

    def discover(self, hostname = ''):
        if hostname in self.connectedClientAdd:
            return self.clientFileList[hostname]
        else:
            return hostname + " has not connected to server yet."

def main():
    server = Server(SERVER_IP, SERVER_PORT)
    server.start()

if __name__ == '__main__':
    main()