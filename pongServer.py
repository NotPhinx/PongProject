# =================================================================================================
# Contributing Authors:	    <Anyone who touched the code>
# Email Addresses:          <Your uky.edu email addresses>
# Date:                     <The date the file was last edited>
# Purpose:                  <How this file contributes to the project>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================

import socket
import threading

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
server = ""
port = 5555

# socket for connection to server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


try: 
    sock.bind((server, port))
except socket.error as e:
    str(e)

sock.listen(2)
print("Server launched successfully, waiting for connection")

def threadClient(conn):
    reply = ""
    while True:
        try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Disconnected")
                break
            else:
                print("Received:", reply)
                print("Sending:", reply)

            conn.sendall(str.encode(reply))
        except:
            break

    print("Loss connection")
    conn.close()


while True:
    conn, addr = sock.accept()
    print("Connected to:", addr)

    thread = threading.Thread(target=threadClient, args=(conn,))
