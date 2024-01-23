import random
import sys
from datetime import time
from socket import *

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', 3025))
print("istek !!!!")

server_list = {
    "2526": 0,
    "2527": 0,
    "2528": 0
}

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
clientSocket = socket(AF_INET, SOCK_DGRAM)

# To set waiting time of one second for reponse from server
clientSocket.settimeout(1)

while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    message = bytes.decode(message, 'utf-8') + ' (This message came from load balancer !!!) '
    counter = 0
    for k, v in server_list.items():
        if v == 0:
            message = message + ' The port of this server is ' + k
            remoteAddr = ('', int(k))
            server_list[k] = 1
            break
        else:
            counter += 1
            if counter == 3:  # tüm serverlar kullanıldı mı ?
                for key, value in server_list.items():  # dict resetlendi
                    server_list[key] = 0
                first_item_key = list(server_list.items())[0][0]
                message = message + ' The port of this server is ' + first_item_key
                remoteAddr = ('', int(first_item_key))
                server_list[first_item_key] = 1
                counter = 0
            continue
    clientSocket.sendto(bytes(message, 'utf-8'), remoteAddr)
    # Capitalize the message from the client
    message = message.upper()
    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
        continue
    # Otherwise, the server responds
    serverSocket.sendto(bytes(message, 'utf-8'), address)
