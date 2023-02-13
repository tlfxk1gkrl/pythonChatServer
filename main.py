from socket import *
import threading

port = 10000

server_socket = socket(AF_INET, SOCK_STREAM) ## socket definition
server_socket.bind(('', port))               ## server port = 10000
server_socket.listen(5)                      ## max client socket = 5

user_list = {}                               ## chat user dic
def receive(client_socket, addr, user):
    while 1:                                 
        data = client_socket.recv(1024)      ## get data from client socket
        string = data.decode()               ## decode

        if string == "/exit" :
            msg = f'{user.decode()} has exited.'
            for con in user_list.values():                    
              try:
                  con.sendall(msg.encode())
              except:
                  print("Detect killed socket")
            print(msg)
            break
        string = "%s : %s"%(user.decode(), string)
        print(string)
        for con in user_list.values():                    ## send message to clients
            try:
                con.sendall(string.encode())            
            except:
                print("Detect killed socket")
    del user_list[user]                                   ## remove client from dic
    client_socket.close()                                 ## remove client

while True:
    client_socket, addr = server_socket.accept()          ## def client socket
    user = client_socket.recv(1024)                       ## first data when def client socket
                                                          ## rec user name from client
    user_list[user] = client_socket                       ## add user list
    print(f'{user.decode()} has entered.')

    receive_thread = threading.Thread(target=receive, args=(client_socket, addr,user))
    ## rec and send data from each client to chat   >> def thread
    receive_thread.start()