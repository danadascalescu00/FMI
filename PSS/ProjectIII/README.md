# Project III

## Overview
Develop an application that uses a Local Search Algorithm to tackle a problem that you have formulated and defined.

## Problem statement
In classroom 308, students taking the Artificial Intelligence exam are seated on two-person benches arranged in rows and columns. Some of the seats are empty. Eve wants to help her colleague Adam succeed on the exam by giving him the correct answers. There are restrictions on how notes may be sent, however. Students can only communicate with a fellow student who is immediately behind, in front of, or next to them. Furthermore, it is difficult to interact across rows since the teacher may see students attempting to share notes. The feasible options for message transfer are limited to the last seats in each row. Therefore, the challenge is to devise an optimal strategy for Eve to transfer the answers to Adam within the given restrictions. 

## Solution
To utilise the functionality of this project, you should first clone the repository and subsequently execute the ProjectIII_Dana_Dascalescu.py file. The sender and receiver of the message will be prompted during runtime.

Furthermore, the students' list is expected to be provided in a text file named `input.txt`, with each student's name placed on a separate row. Additionally, the pairs of students upset with each other should be present in a file named `upset_students.txt`.

The project employs a local search algorithm called Hill Climb Search. The implementation includes a custom initialization function and a cost function that optimises both the trustworthiness of the students receiving the message and minimises the number of steps for the message to reach the receiver.

The seating arrangement of the students, the number of rows, and the locations of the sender and the receiver are taken from the input files and from the problem definition, and there is no need for any user input regarding these aspects. After execution, the programme will generate the path for passing the message from the sender to the receiver.
