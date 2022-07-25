"""
    server side interface for simple GUI chat
"""
import socket
import threading
# import time
# import sys
import os
# Set environment variable
os.environ['TK_SILENCE_DEPRECATION'] = '1'
# declare the host address
HOST = '127.0.0.1'
PORT = 9090

SERVER = socket.gethostbyname(socket.gethostname())

# declare server in socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# specifying the type of socket
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))

# opens ports to signals
# listens for 8 active clients.
server.listen(8)

# need to expand for DB lookup
# can pull from main DB for website
clients = []
nicknames = []

# formatting
FORMAT = 'utf-8'


# broad
def broadcast(message):
    for client in clients:
        client.send(message)


def receive():

    while True:  # can expand this to do signal handling
        client, address = server.accept()
        print(f'connected with {str(address)}') # server logging of message

        client.send("NICK".encode('utf-8'))  # will ask for nickname
        nickname = client.recv(1024)

        # room for improvement here, nickname handling can be built out
        clients.append(client)
        nicknames.append(nickname)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} connected to server \n".encode("utf-8"))
        client.send("Connected to server".encode("utf-8"))

        thread = threading.Thread(target=handle, args=(client,))
        # start threading, passing the comma in args= to make tuple
        thread.start()


def remove_conn(connection):
    if connection in clients:
        clients.remove(connection)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[client.index(client)]} is saying {message}" ) # logging statement for server
            # need to develop index of nicknames for server side handling
            # this prints on server console log
            broadcast(message)
        except:
            # below needs to be handled with SQL
            index = clients.index(client)  # looks up current client
            clients.remove(client)  # remove client from chatroom
            client.close()  # close connection
            nickname = nicknames[index]  # loops up current index
            nicknames.remove(nickname)  # could also use .pop() here
            remove_conn(client)
            break  # this ends thread since connection is done


if __name__ == '__main__':
    print('server running... ')
    receive()
