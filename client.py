import socket as sk
import os
import threading
import shutil
import time

# Enter the server's IP
# SERVER_IP = input("Enter Server's IP: ")
# SERVER_PORT = 4869

SIZE = 1024
REPOSITORY_PATH = 'repository/'
FORMAT = 'utf-8'

#SERVER_IP = sk.gethostbyname(sk.gethostname())
#SERVER_PORT = 4869

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


class Client:
    def __init__(self, IP, port, hostname):
        self.client_socket = None
        self.server_IP = IP
        self.server_Port = port
        self.hostname = hostname
        self.isConnected = False

        self.peer_socket = None

        self.allFile = list()

    ##### START CONNECT TO SERVER #####
    def start(self):
        # Create local repository
        if not os.path.exists(REPOSITORY_PATH):
            os.makedirs(REPOSITORY_PATH)

        # Connect to the server
        self.client_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_IP, self.server_Port))
        except:
            print(f"Failed to connect to server: {self.server_IP}:{self.server_Port}")
            return False
        self.isConnected = True
        self.client_socket.send(self.hostname.encode(FORMAT))
        _ = self.client_socket.recv(SIZE).decode(FORMAT)
        print(f"Connected to server: {self.server_IP}:{self.server_Port}")
        self.publish_all()
        self.GetAllFile()
        self.request_thread = threading.Thread(target=self.start_request)
        self.request_thread.start()
        time.sleep(0.2)

        # Listen to other peers
        self.client_server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self.client_server.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
        self.client_server.bind((get_local_ip(), 6969))
        self.client_server.listen()
        
        self.listen_thread = threading.Thread(target=self.listening)
        self.listen_thread.start()



    def getfile_from_target_peer(self, target_IP = '127.0.0.1', target_Port = 6969, fileName = ''):
        self.peer_socket = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        try:
            self.peer_socket.connect((target_IP, target_Port))
        except:
            print(f'Failed to connect to peer: {target_IP}:{target_Port}')
            return('FAIL@Connection failed')
        print(f'Connected to peer: {target_IP}:{target_Port}')

        request = 'FETCH@' + fileName
        self.peer_socket.send(request.encode(FORMAT))


        #data = self.peer_socket.recv(SIZE)
        
        filePath = os.path.join(os.getcwd(), REPOSITORY_PATH)
        filePath += fileName
        file = open(filePath, 'wb')
        while True:
            data = self.peer_socket.recv(SIZE)
            if not data or data == 'DONE'.encode(FORMAT):
                break
            file.write(data)
            self.peer_socket.send('OK'.encode(FORMAT))
        file.close()
        msg = 'Received ' + fileName + f' from {target_IP}'
        self.targetIP = target_IP
        print(msg)
        self.peer_socket.close()
        if fileName not in self.allFile:
            self.allFile.append(fileName)
        self.publish_all()
        return msg


    ##### Start send request #####
    def start_request(self):
        while self.isConnected:
            self.choosing_option()


    ##### Client choose option #####
    def choosing_option(self):

        print('Enter your command:\n> publish `lname` `fname`: Add a file named `fname` from `lname` to repository and convey to the server\n> fetch `fname`: Find some copy of the file named `fname` and add it to repository\n> quit: Disconnect from server\n> delete fname: Delete fname from your repository')
        
        option = input('Your command: ')
        if option.startswith('publish'):
            lname = option.split(' ')[1]
            fname = option.split(' ')[2]
            self.publish(lname, fname)
        elif option.startswith('fetch'):
            fname = option.split(' ')[1]
            self.fetch(fname)
            targetIP = input('Enter IP to connect: ')
            self.getfile_from_target_peer(targetIP, 6969, fname)
        elif option.startswith('delete'):
            fname = option.split(' ')[1]
            self.deleteFile(fname)
        elif option.startswith('getall'):
            self.GetAllFile()
        elif option == 'quit':
            self.disconnect(self.client_socket, self.server_IP, self.server_Port)
            self.isConnected = False
            self.client_server.close()
            exit(0)
        else:
            print('Invalid Command')


    ####### Disconnect from server ########
    def disconnect(self, my_socket = sk.socket, other_IP = '127.0.0.1', other_Port = 4869):

        msg = f'DISCONNECT@Disconnected from server {other_IP}:{other_Port}'

        my_socket.send(msg.encode(FORMAT))
        print(msg.split('@')[1])
        my_socket.close()


    ##### Publish all file in repository when connect to server #####
    def publish_all(self):

        filePath = os.path.join(os.getcwd(), REPOSITORY_PATH)
        fileList = ''
        
        for file in os.listdir(filePath):
            fileList += file + ':'
        
        if fileList != '':
            msg = 'PUBLISHALL@' + fileList
            self.client_socket.send(msg.encode(FORMAT))
            server_respond = self.client_socket.recv(SIZE).decode(FORMAT)
            _ = server_respond.split('@')
            print('Published all file to the server.')


    def publish(self, lname = '', fname = ''):
        
        filePath = os.path.join(lname, fname)
        if not os.path.exists(filePath):
            print('This file does not exist on your system.')
            return('ERROR', 'Please select a file to upload')
        else:
            if fname in os.listdir(os.path.join(os.getcwd(), REPOSITORY_PATH)):
                print('File name existed in your repository')
                return('ERROR', 'File name existed in repository.')
            else:
                shutil.copy(filePath, os.path.join(os.getcwd(), REPOSITORY_PATH))

                msg = 'PUBLISH@' + fname
                self.client_socket.send(msg.encode(FORMAT))
                
                server_respond = self.client_socket.recv(SIZE).decode(FORMAT)
                server_command, server_message = server_respond.split('@')
                if fname not in self.allFile:
                    self.allFile.append(fname)
                print(server_message)
                return server_command, server_message


    def fetch(self, fname = ''):

        filePath = os.path.join(REPOSITORY_PATH, fname)
        if not os.path.exists(filePath):
            msg = 'FETCH@' + fname
            self.client_socket.send(msg.encode(FORMAT))
            
            server_respond = self.client_socket.recv(SIZE).decode(FORMAT)
            server_command, server_message = server_respond.split('@')
            if server_command == 'OK':
                clientList = []
                while True:
                    clients = self.client_socket.recv(SIZE).decode(FORMAT)
                    if clients.startswith('DONE'):
                        break
                    else:
                        clientList.append(clients)
                    self.client_socket.send('Received'.encode(FORMAT))
                if (clientList):
                    print(server_message, clientList)
                    # target_IP = clientList[0].split(':')[0]
                    # msg = self.getfile_from_target_peer(target_IP, 6969, fname)
                    print(msg)
                    return clientList
                else:
                    msg = 'File is not found on the server'
                    print(msg)
                    return msg
            else:
                print(server_message)
                return server_message
        else:
            msg = 'File existed in repository.'
            print(msg)
            return msg


    def deleteFile(self, fname):
        filePath = os.path.join(REPOSITORY_PATH, fname)
        if not os.path.exists(filePath):
            print('File does not exist in repository.')
            return('ERROR', 'File does not exist in repository.')
        else:
            os.remove(filePath)
            msg = 'DELETE@' + fname
            self.client_socket.send(msg.encode(FORMAT))
            _, server_msg = self.client_socket.recv(SIZE).decode(FORMAT).split('@')
            self.allFile.remove(fname)
            print(server_msg)


    def listening(self):
        while self.isConnected:
            self.sending_to_peers()


    def sending_to_peers(self):
        try:
            other_socket, other_address = self.client_server.accept()
            print(f"Peer {other_address} connected.")
            try:
                request = other_socket.recv(SIZE).decode(FORMAT)
            except:
                print('Waiting for request...')

            #request = other_socket.recv(SIZE).decode(FORMAT)
            fileName = request.split('@')[1]
            self.transfer_file(other_socket, other_address[0], fileName)
        except:
            if not self.isConnected:
                print('CLOSE')
                exit(0)  

        
    def transfer_file(self, receiver = sk.socket, receiver_IP = '127.0.0.1', fileName = ''):
        filePath = os.path.join(os.getcwd(), REPOSITORY_PATH)
        filePath += fileName
        file = open(filePath, 'rb')
        while True:
            data = file.read(SIZE)
            if not data:
                receiver.send('DONE'.encode(FORMAT))
                break
            receiver.send(data)
            _ = receiver.recv(SIZE).decode(FORMAT)
        file.close()
        print('Sent ' + fileName + f' to peer: {receiver_IP}')
        receiver.close()


    def GetAllFile(self):
        self.allFile = []
        self.client_socket.send('GETALL@Get'.encode(FORMAT))
        
        while True:
            file = self.client_socket.recv(SIZE).decode(FORMAT)
            if not file or file.startswith('DONE?'):
                break
            if file not in self.allFile:
                self.allFile.append(file)
            self.client_socket.send('_'.encode(FORMAT))

        msg = 'Received all files from server.'
        print(msg)
        return msg



def main():
    SERVER_IP = input("Enter server's IP: ")
    SERVER_PORT = 4869
    hostname = input("Enter your name: ")
    client = Client(SERVER_IP, SERVER_PORT, hostname)
    client.start()

if __name__ == "__main__":
    main()