Contact Info
============

Group Members & Email Addresses:

    Braden Howell, brho231@uky.edu
    Ethan Binkley, rebi227@uky.edu
    Jaden Vaught, jva231@uky.edu

Versioning
==========

GitHub Link: 
https://github.com/NotPhinx/PongProject

Report Link:
https://docs.google.com/document/d/19_ldL_nmP29nleiZ-YYSQyoq11BeDDCffjT2Hk_minU/edit?usp=sharing 

General Info
============
This code repository is for UKY's CS 371 Pong Project. It includes a server and client file
as well as some helper functions in auxiliary files (found in assets). The server currently 
supports the connection of two clients and the communication between them. It stores the data
necessary and sends it to the respective client. The client is where the game is actually run, 
using updates from the server to determine which client is most up-to-date. It uses a TCP 
connection which allows for reliability between the two clients but does create some delay
on the traversal of the ball. 

Install Instructions
====================

Run the following line to install the required libraries for this project:
`pip3 install -r requirements.txt`

The best practice is to have 3 devices to play:
Device 1: Will run the server code
Device 2: Will run the client code and will connect to the server using the IPv4 of Device 1 
    and port 5555
Device 3: Will run the client code and will connect to the server using the IPv4 of Device 1
    and port 5555

Known Bugs
==========
- The game is a few frames behind at times but that doesn't affect the gameplay.
- When you quickly hit up and down to move the paddle paddle will not move

