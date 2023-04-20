# Project II

## Overview
The goal of this project is to develop an application that utilizes an Informed Search algorithm to solve a given problem. To evaluate the performance of the search algorithms, we have selected the same application from Project 1. The problem statement and a brief summary of the informed search technique that will be utilized to solve it are described below.

## Problem statement
 In classroom 308, students taking the Artificial Intelligence exam are seated in rows of two-person benches arranged in three columns. Some spots are free, meaning there are no students occupying those seats. Oscar wants to help his friend Carina cheat on the exam by sending him the answers through a message. However, there are restrictions on how messages can be passed. Students can only pass the message to the bank colleague behind or in front of them, or the one right beside them, but not diagonally. Additionally, passing messages between rows is challenging since the teacher can easily notice it. Only the penultimate and final benches on each row can be used for message transfer. To ensure she does not get lost in the classroom, Oscar wants to include on the note the path it needs to take from one colleague to the next. To make matters worse, some students are upset with each other or disagree with cheating. This may make them unwilling to participate in the message transfer, or they will report it to the TAs if they notice it happening. Therefore, Oscar needs to be cautious about selecting trustworthy colleagues who are willing to help him.

## Solution
We will employ the A* search algorithm and compare its performance and effectiveness with DFS and BFS to solve this problem. By adhering to the problem statement's limitations, we will apply these algorithms to determine the optimal path for sending the message from Oscar to Carina.

#### Usage
To utilize this project, you need to clone the repository and execute the `ProjectII_Dana_Dascalescu.py` file. The program does not prompt the user to input details such as the number of rows, the seating arrangement of the students, or the locations of Carina and Oscar. Instead, these details are located in the `inputs` directory. The algorithm's output is displayed and saved in the `outputs` directory, which includes the shortest path for transmitting the message from Oscar to Carina, the execution time, and the maximum memory usage.

#### Performance analysis
Our experiments demonstrate that A* search outperforms BFS and DFS in terms of execution time, taking only 0.0020 seconds to complete. While all three algorithms have comparable memory usage, BFS and DFS require slightly more memory than A* search. It is important to note that we ensured a fair comparison by executing all three algorithms on the same configuration. These findings indicate that A* search is a promising choice for search problems that require efficient execution. However, the suitability of each algorithm may vary depending on the problem's characteristics, such as the size and complexity of the search space.


***[Project documentation](https://github.com/danadascalescu00/FMI/blob/master/PSS/ProjectII/ProjectII_Dana_Dascalescu.py)***
