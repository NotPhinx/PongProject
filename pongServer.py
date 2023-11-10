# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading
import pickle

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the game

# initialize server and its information
# connect to various hosts to specific port
# begin threads to handle separate communication from server to each client

# need to decide if threads should be created and joined before or after getting info from client

# add ip address of local machine that will host server
server = "192.168.0.112"
port = 5555

# socket for connection to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try: 
    sock.bind((server, port))
except socket.error as e:
    str(e)

sock.listen(2)
print("Server launched successfully, waiting for connection")

player0_objData = {
    "player_paddle": "",
    "ball": "",
    "score": (0, 0),
    "sync": 0
}
player1_objData = {
    "player_paddle": "",
    "ball": "",
    "score": (0, 0),
    "sync": 0
}

def threadClient(conn:socket.socket, player:int) -> None:
    if player == 0:
        conn.send(pickle.dumps("left"))
    elif player == 1:
        conn.send(pickle.dumps("right"))
    reply = ""
    while True:
        try:
            print("here1")
            data = pickle.loads(conn.recv(4096))
            print(data)

            if not data:
                print("Disconnected")
                break
            else:
                if player == 0:
                    for key in data:
                        player0_objData[key] = data[key]
                    reply = player1_objData
                elif player == 1:
                    for key in data:
                        player1_objData[key] = data[key]
                    reply = player0_objData

            print("here2")
            print(reply)
            conn.send(pickle.dumps(reply))
        except:
            break

    print("Loss connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = sock.accept()
    print("Connected to:", addr)

    thread = threading.Thread(target=threadClient, args=(conn, currentPlayer))
    thread.start()
    currentPlayer += 1
