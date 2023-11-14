Contact Info
============

Group Members & Email Addresses:

    Braden Howell, brho231@uky.edu
    Ethan Binkley, rebi227@uky.edu
    Jaden Vaught, jva231@uky.edu

Versioning
==========

Github Link: 
https://github.com/NotPhinx/PongProject

General Info
============
This code repository is for UKY's CS 371 Pong Project. It includes a server and client file
as well as some helper functions in auxiliary files (found in assets). The server currently 
supports the connection of two clients and the communication between them. It stores the data
necessary and sends it to the respective client. The client is where the game is actually run, 
using updates from the server to determine which client is most up-to-date. It uses a TCP 
connection which allows for reliablility between the two clients, but does create some delay
on traversal of the ball. 

Install Instructions
====================

Run the following line to install the required libraries for this project:

`pip3 install -r requirements.txt`

Known Bugs
==========
- The game is a few frames behind at times, but doesn't effect the gameplay.

