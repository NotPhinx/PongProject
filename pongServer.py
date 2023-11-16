# =================================================================================================
# Contributing Authors:	    Braden Howell
#                           Ethan Binkley
# 
# Email Addresses:          brho231@uky.edu
#                           rebi227@.uky.edu
#      
# Date:                     11/13/2023
# Purpose:                  This file contains the code to run the server for Python's Pong. It 
#                           currently supports 2 clients and the communication between them. 
# =================================================================================================

import socket
import threading
import pickle
from flask import Flask, jsonify
app = Flask(__name__)

#initialize leaderboard
leaderboard = {}

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

# catching socket binding errors
try: 
    sock.bind((server, port))
except socket.error as e:
    print("here")
    str(e)

# socket listens for 2 connections before refusing further ones
sock.listen()
print("Server launched successfully, waiting for connection")


# initializing object data for both players
players_objData = []

#function to reset the game for both players
def reset_game():
    global player0_objData, player1_objData

    # Reset player0_objData
    player0_objData = {
        "player_paddle": "",
        "ball": "",
        "score": (0, 0),
        "sync": 0
    }
    # Reset player1_objData
    player1_objData = {
    "player_paddle": "",
    "ball": "",
    "score": (0, 0),
    "sync": 0
    }

# thread target function that handles the majority of the continuous communication between server and each client
# it passes in a connection and player number to differentiate between clients
def threadClient(conn:socket.socket, player:int) -> None:
    # first player to connect will be the left paddle and second will be right
    if player == 0:
        conn.send(pickle.dumps("left"))
    elif player == 1:
        conn.send(pickle.dumps("right"))
    reply = ""

    # main loop for sending data between clients and update object data on server
    while True:
        try:
            data = pickle.loads(conn.recv(4096))

            if not data:
                print("Disconnected")
                break
            else:
                if data == b'PLAY_AGAIN':
                    #update the leaderboard
                    leaderboard[addr] = leaderboard.get(addr, 0) + 1
                    #reset game state
                    reset_game()
                    #send "GAME_RESET" to both clients'
                    for connection in connections:
                        connection.send(pickle.dumps("GAME_RESET"))
                else:
                    
                    if player == 0:
                        for key in data:
                            player0_objData[key] = data[key]
                        reply = player1_objData
                    elif player == 1:
                        for key in data:
                            player1_objData[key] = data[key]
                        reply = player0_objData

            conn.send(pickle.dumps(reply))
        except:
            break

    print("Loss connection")
    conn.close()

@app.route('/leaderboard')
def get_leaderboard():
    return jsonify(leaderboard)

# main loop for accepting new connections and passing them into the thread function
connections = []
currentPlayer = 0
while True:
    conn, addr = sock.accept()
    print("Connected to:", addr)

    players_objData.append({
        "player_paddle": "",
        "ball": "",
        "score": (0, 0),
        "sync": 0
    })

    connections.append(conn)

    thread = threading.Thread(target=threadClient, args=(conn, currentPlayer))
    thread.start()
    currentPlayer += 1
    
