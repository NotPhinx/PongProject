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
server = "192.168.68.115"
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

players_objData = []  # Declare players_objData outside the loop

#function to reset the game for both players
def reset_game():
    global player0_objData, player1_objData\

    # Reset player0_objData
    player0_objData = {
        "player_paddle": "",
        "ball": "",
        "score": (0, 0),
        "sync": 0,
        "play_again": False
    }
    # Reset player1_objData
    player1_objData = {
    "player_paddle": "",
    "ball": "",
    "score": (0, 0),
    "sync": 0,
    "play_again": False
    }

# initializing object data for both players
reset_game()

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
            if connected_clients >= 2:
                data = pickle.loads(conn.recv(4096))
                print(data)
                if not data:
                    print("Disconnected")
                    break
                else:
                    if data == 'PLAY_AGAIN':
                        players_objData[player]['play_again'] = True

                        #If all players want to play again, reset the game state and send to the clients to restart the game
                        if all(player_data['play_again'] for player_data in players_objData):
                            for connection in connections:
                                connection.sendall(pickle.dumps('GAME_RESET'))
                                reset_game()
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
# Counter to track the number of connected clients
connected_clients = 0

while True:
    conn, addr = sock.accept()
    print("Connected to:", addr)

    players_objData.append({
        "player_paddle": "",
        "ball": "",
        "score": (0, 0),
        "sync": 0,
        "play_again": False

    })

    connections.append(conn)
    connected_clients += 1

    thread = threading.Thread(target=threadClient, args=(conn, currentPlayer))
    thread.start()
    currentPlayer += 1
    