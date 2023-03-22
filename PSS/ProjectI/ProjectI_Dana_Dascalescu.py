"""
    Author: Dăscălescu Dana, groupe 507, Artificial Intelligence
    
    Problem description and requirements for applicability of the BFS and DFS algorithms:
        * Description: The students taking the Artificial Intelligence exam are arranged in rows of two-person benches in classroom 308.
        The benches are arranged in two columns. Diana wants to help her friend Calin by sending him the answers to the exam's grid
        through a message. A student can only pass the message to the bank colleague behind or in front of them, or the one right beside
        them, but not diagonally. Moreover, passing the message between rows is challenging since the teacher can easily notice it. As
        a result, only the penultimate and final banks on each row can be utilized for message transfer. Diana wants to include the 
        path she needs to take from one colleague to the next on the note to avoid getting lost in the classroom and reaching her 
        friend only after the exam ends.
        * Task requirements: A software application that uses two algorithms of Uninformed Search.
"""

import re
import sys
import timeit

from abc import ABC, abstractmethod

from typing import List

from collections import deque


def read_input_file(input_filename):
    fin = None
    try:
        fin = open(input_filename, "r")
    except:
        print('Error: {}. {}, line: {}'.format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
        
    maze_configuration, start_scope_nodes_names = [], []
    for line in fin:
        if 'mesaj' in line:
            start_scope_nodes_names = re.split('->', line)
            start_scope_nodes_names[0] = start_scope_nodes_names[0].strip().split()[-1]
            start_scope_nodes_names[1] = start_scope_nodes_names[1].strip()
            break
        
        try:
            students = line.split()
        except ValueError:
            print("Something went wrong! Invalid input!")
            fin.close()
        maze_configuration.append(students)
            
    fin.close()
    
    return maze_configuration, start_scope_nodes_names 


class Node(ABC):
    """
        This abstract class provides a basic structure for defining nodes in a graph and 
        allows for customization by subclassing and implementing the required methods.

    Methods:
        * __eq__(self, other): Determines if two nodes are equal or not
        * __hash__(self): Returns a hash value for the node, which is used for fast lookup in hash tables
        * __str__(self): Returns a string representation of the node
    """
    
    @abstractmethod
    def __eq__(self, __o: object) -> bool:
        pass
    
    @abstractmethod
    def __hash__(self) -> int:
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass
    
    
class Student(Node):
    """
        This class is used to represent a student in the graph.

        Args:
            Node (_type_): _description_
            
        Attributes:
            * row (int): The row in which the student is located
            * col (int): The column in which the student is located
            * name (str): The name of the student
            * parent (Student): The parent of the student in the search tree
            
        Methods:
            * __init__(self, row, col, name=None, parent=None): Initializes the student with the given row, column, name, and parent
            * __eq__(self, other): Determines if two students are equal or not
            * __hash__(self): Returns a hash value for the student
            * __str__(self): Returns a string representation of the student
    """
    def __init__(self, row, col, name=None, parent=None) -> None:
        self.row = row
        self.col = col
        self.name = name
        self.parent = parent
    
    def __eq__(self, __o: object) -> bool:
        return self.row == __o.row and self.col == __o.col
    
    def __hash__(self) -> int:
        return hash((self.row, self.col))
        
    def __str__(self) -> str:
        if self.name:
            return self.name
     
        
class Problem:
    def __init__(self, matrix_config, start_scope_nodes_names ) -> None:
        """
            Initialize a new instance of the problem class.
            
            Args:
                * matrix_confix (list): A list of lists representing the matrix configuration.
                * start_scope_nodes_names (list): A list of two strings representing the start and goal node names.
        
        """
        self.maze = matrix_config
        self.rows = len(self.maze) # number of rows in the maze
        self.cols = len(self.maze[0]) # number of columns in the maze
        self.start_node = self.get_node(start_scope_nodes_names[0]) # starting node
        self.scope_node = self.get_node(start_scope_nodes_names[1]) # goal node
        
    def get_node(self, node_name):
        """
        Finds in the matrix configuration and returns a node object based on the string representation.

        Args:
            node_name (str): The name of the node (string representation) to retrieve. In our context the Student object.

        Returns:
            Student: A student object representing the node.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.maze[i][j] == node_name:
                    return Student(i, j, node_name)
                

class Search():
    def __init__(self, problem) -> None:
        self.problem_configuration = problem
    
    
    def reconstruct_path(self, node) -> List[Student]:
        # Reconstructs the path of the solution
        path = []
        while node:
            path.append(node)
            node = node.parent
            
        return path[::-1]
    
    
    def show_path(self, path):
        # Shows the reconstructed path of the solution
        print("Reconstructed path:")
        print("\t", end="")        
        for it, node in enumerate(path):
            if it != len(path) - 1:
                print(f"{node.name} ---> ", end="") 
            else:
                print(node.name)
    
    
    def get_successors(self, node) -> List[Student]:
        """
            Returns a list with all the successors (neighboring nodes) of a given node. 
            
            Args:
                node (Student): The node whose successors we want to find.
                
            Returns:
                List[Student]: The list of nodes that are the successors of the current node.
        """
        row, col = node.row, node.col
        successors = []
        
        # Check back 
        if row < self.problem_configuration.rows - 1 and self.problem_configuration.maze[row + 1][col] != "X":
            successors.append(Student(node.row + 1, node.col, \
                name=self.problem_configuration.maze[row + 1][col], parent=node))
            
        # Check right
        if col >= 0 and col % 2 != 1 and self.problem_configuration.maze[row][col + 1] != "X":
            successors.append(Student(node.row, node.col + 1, \
                name=self.problem_configuration.maze[row][col + 1], parent=node))
        # Check for last benches
        elif col % 2 == 1 and col < self.problem_configuration.cols - 1 and row == (self.problem_configuration.rows - 1):
            if self.problem_configuration.maze[row][col + 1] != "X":
                successors.append(Student(node.row, node.col + 1, \
                    name=self.problem_configuration.maze[row][col + 1], parent=node))
        elif col % 2 == 1 and col < (self.problem_configuration.cols - 1) and row == (self.problem_configuration.rows - 2):
            if self.problem_configuration.maze[row][col + 1] != "X":
                successors.append(Student(node.row, node.col + 1, \
                    name=self.problem_configuration.maze[row][col + 1], parent=node))
                
        # Check left
        if col > 0 and col % 2 and self.problem_configuration.maze[row][col - 1] != "X":
            successors.append(Student(node.row, node.col - 1, \
                name=self.problem_configuration.maze[row][col - 1], parent=node))
        # Check for last benches
        elif col > 0 and row == (self.problem_configuration.rows - 1):
            if self.problem_configuration.maze[row][col - 1] != "X":
                successors.append(Student(node.row, node.col - 1, \
                    name=self.problem_configuration.maze[row][col - 1], parent=node))
        elif col > 0 and row == (self.problem_configuration.rows - 2):
            if self.problem_configuration.maze[row][col - 1] != "X":
                successors.append(Student(node.row, node.col - 1, \
                    name=self.problem_configuration.maze[row][col - 1], parent=node))
                
        # Check front
        if row > 0 and self.problem_configuration.maze[row - 1][col] != "X":
            successors.append(Student(node.row - 1, node.col, \
                name=self.problem_configuration.maze[row - 1][col], parent=node))
                
                
        return successors
    
    
    def BFS(self):
        # Performs breadth-first search on a given problem and returns the path from the start node to the scope node
        frontier = deque([self.problem_configuration.start_node])
        visited = set()
        
        while frontier:
            node = frontier.popleft()
            visited.add(node)
            
            if node == problem.scope_node:
                path = self.reconstruct_path(node)
                print("The length of the path:", len(path))
                self.show_path(path)
                return path
            
            successors = self.get_successors(node)
            for successor in successors:
                if successor not in visited and successor not in frontier:
                    frontier.append(successor)
                    
        print("Path not found!")
        
        
    def DFS(self):
        # Performs depth-first search on a given problem and returns the path from the start node to the scope node
        frontier = [self.problem_configuration.start_node]
        visited = set()
        
        while frontier:
            node = frontier.pop()
            visited.add(node)
            
            if node == problem.scope_node:
                path = self.reconstruct_path(node)
                print("The length of the path:", len(path))
                self.show_path(path)
                return path
            
            successors = self.get_successors(node)
            for successor in successors:
                if successor not in visited and successor not in frontier:
                    frontier.append(successor)
                    
        print("Path not found!")
    
    
    
if __name__ == "__main__":
    # Get class configuration
    class_grid, start_scope_nodes_names = read_input_file("project1_input.txt")
    problem = Problem(class_grid, start_scope_nodes_names)
    search = Search(problem)
    
    print("*" * 100)
    # measure the execution time of the BFS algorithm
    execution_time = timeit.timeit(search.BFS, number=1)
    print(f"Execution time of BFS search: {execution_time:.4f} seconds")
    print("*" * 100)
    print()
    print("*" * 100)
    # measure the execution time of the BFS algorithm
    execution_time = timeit.timeit(search.DFS, number=1)
    print(f"Execution time of DFS search: {execution_time:.4f} seconds")
    print("*" * 100)
