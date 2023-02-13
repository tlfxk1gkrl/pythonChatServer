from socket import *
import argparse
import threading

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('127.0.0.1', 10000))    ## set address and port

parser = argparse.ArgumentParser()             ## def parser to set user name >> python client.py (username)
parser.add_argument('user')
args = parser.parse_args()
user = args.user

print(f'{user} 접속 완료')

def handle_receive(client_socket, user):       ## rec data from server
    while 1:
        try:
            data = client_socket.recv(1024)    ## rec data exist >> print

        except:                                ## disconnected
            print("disconnected...")
            break
        data = data.decode()
        if not user in data:
            print(data)

def handle_send(client_socket, user):          ## sen data to server
    while 1:
        data = input()
        client_socket.sendall(data.encode())
        if data == "/exit":
            break
    client_socket.close()


receive_thread = threading.Thread(target=handle_receive, args=(client_socket, user,))
receive_thread.start()
send_thread = threading.Thread(target=handle_send, args=(client_socket, user))
send_thread.start()
## def sending and receiving data as multi-thread so that they can operate separately.

client_socket.sendall(user.encode()) ## The first data to send after the client socket is defined is user name