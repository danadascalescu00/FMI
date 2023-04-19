# Project I

## Overview
This project aims to create an application that applies at least two uninformed search methods to solve a given problem. Following is a description of the problem statement and a summary of the uninformed search techniques that will be utilized to solve it.

## Problem statement
In classroom 308, students taking the Artificial Intelligence examination are placed on two-person benches arranged in rows and columns. Some seats are unoccupied. Diana wishes to assist her friend Călin in passing on the exam by sending him the correct responses. However, there are restrictions on the transmission of notes. Students may only send a message to the colleague directly behind, in front of, or next to them, but not diagonally. Furthermore, passing messages between rows is difficult because the teacher can easily notice it. Only the second-to-last and last seats in each row may be utilized for message transfer.

## Solution
We will use the following search algorithms to solve the problem: _Depth-First Search (DFS)_, _Breadth-First Search (BFS)_, _Depth-Limited Search (DLS)_, and _Iterative Deepening Search (IDS)_. We will compare the performance and efficacy of DFS and BFS, as well as examine the applicability of DLS and IDS to this specific problem. Using the constraints specified in the problem statement, the algorithms will be used to determine the path the message must take from Diana to Călin.

To use this project, clone the repository and run the `ProjectI_Dana_Dascalescu.py` file. There is no user input prompt regarding the number of rows, the seating arrangement of the students, or the locations of Diana and Călin.  These are located in the text file `project1_input.txt`. The program will output the shortest path for passing the message from Diana to Călin, the execution time, and the maximum memory usage.
