"""
    Author: Dăscălescu Dana, groupe 507, Artificial Intelligence
    
    Task requirements: 
        An application that uses two algorithms of Uninformed Search.
    
    Problem description and requirements for applicability of the BFS and DFS algorithms:
        The students taking the Artificial Intelligence exam are arranged in rows of two-person benches in classroom 308.
        The benches are arranged in two columns. Diana wants to help her friend Calin by sending him the answers to the exam's grid
        through a message. A student can only pass the message to the bank colleague behind or in front of them, or the one right beside
        them, but not diagonally. Moreover, passing the message between rows is challenging since the teacher can easily notice it. As
        a result, only the penultimate and final banks on each row can be utilized for message transfer. Diana wants to include the 
        path she needs to take from one colleague to the next on the note to avoid getting lost in the classroom and reaching her 
        friend only after the exam ends.
"""

import re
import sys

from time import sleep, time
from memory_profiler import memory_usage
import gc # Garbage Collector

from abc import ABC, abstractmethod

from typing import List, Tuple

from collections import deque


def read_input_file(input_filename: str) -> Tuple[List[List[str]], List[str]]:
    """
    Reads the input file and extracts the maze configuration and start scope nodes names from it.
    
    Args:
    input_filename (str): The filename of the input file.
    
    Returns:
    maze_configuration (List[List[str]]): The maze configuration as a 2D list of strings.
    start_scope_nodes_names (List[str]): The start scope nodes names as a list of strings.
    """
    
    try:
        fin = open(input_filename, "r")
    except:
        print('Error: {}. {}, line: {}'.format(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2].tb_lineno))
        return None
        
    maze_configuration, start_scope_nodes_names = [], []
    
    # Loop through each line of the input file
    for line in fin:
        # If the line contains "message", extract the start and scope nodes
        if 'message' in line:
            start_scope_nodes_names = re.split('->', line)
            start_scope_nodes_names[0] = start_scope_nodes_names[0].strip().split()[-1]
            start_scope_nodes_names[1] = start_scope_nodes_names[1].strip()
            break
        
        try:
            students = line.split()
            maze_configuration.append(students)
        except ValueError:
            # If an error occurs while splitting the line, print an error message and close the file
            print("Something went wrong! Invalid input!")
            fin.close()
        
    # Close the input file and return the maze configuration and start scope nodes names      
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
    """
    Problem and goal formulation
    """
    def __init__(self, matrix_config: List[List[str]], start_scope_nodes_names: List[str]) -> None:
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
        
    def get_node(self, node_name: str) -> Student:
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
    """
    Infrastructure for search algorithms.
    """
    def __init__(self, problem) -> None:
        self.problem_configuration = problem
    
    
    def reconstruct_path(self, node) -> List[Student]:
        # Reconstructs the path of the solution
        path = []
        while node:
            path.append(node)
            node = node.parent
            
        return path[::-1]
    
    
    def show_path(self, path: List[Node]) -> None:
        # Shows the reconstructed path of the solution
        print("Reconstructed path:")
        print("\t", end="")        
        for it, node in enumerate(path):
            if it != len(path) - 1:
                print(f"{node.name} ---> ", end="") 
            else:
                print(node.name)
    
    
    def get_successors(self, node: Student) -> List[Student]:
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
    
    
    def BFS(self) -> List[Node]:
        """
        Performs breadth-first search on a given problem and returns the path from the start node to the scope node.
        
        Returns:
        path (List[Node]): The path from the start node to the scope node.
        """

        # Initialize the frontier and visited set
        frontier = deque([self.problem_configuration.start_node])
        visited = set()
        
        # Loop through each node in the frontier until the scope node is found or the frontier is empty
        while frontier:
            node = frontier.popleft()
            visited.add(node)
            
            # If the scope node is found, reconstruct the path and return it
            if node == problem.scope_node:
                path = self.reconstruct_path(node)
                print("The length of the path:", len(path))
                self.show_path(path)
                return path
            
            # Otherwise, add the node's successors to the frontier if they have not been visited or added to the frontier before
            successors = self.get_successors(node)
            for successor in successors:
                if successor not in visited and successor not in frontier:
                    frontier.append(successor)
        
        # If the scope node is not found, print an error message and return None           
        print("Path not found!")
        return None
        
      
    def DFS(self) -> List[Node]:
        """
        Performs depth-first search on a given problem and returns the path from the start node to the scope node.
        
        Returns:
        path (List[Node]): The path from the start node to the scope node.
        """
        
        # Initialize the frontier and visited set
        frontier = [self.problem_configuration.start_node]
        visited = set()
        
        # Loop through each node in the frontier until the scope node is found or the frontier is empty
        while frontier:
            node = frontier.pop()
            visited.add(node)
            
            # If the scope node is found, reconstruct the path and return it
            if node == problem.scope_node:
                path = self.reconstruct_path(node)
                print("The length of the path:", len(path))
                self.show_path(path)
                return path
            
            # Otherwise, add the node's successors to the frontier if they have not been visited or added to the frontier before
            successors = self.get_successors(node)
            for successor in successors:
                if successor not in visited and successor not in frontier:
                    frontier.append(successor)
         
        # If the scope node is not found, print an error message and return None           
        print("Path not found!")
        return None
        
        
    def DLS(self, l: int = 18) -> List[Node]:
        """
        Performs depth-limited search on a given problem and returns the path from the start node to the scope node.
        
        Args:
        l (int): The maximum depth to search to.
        
        Returns:
        path (List[Node]): The path from the start node to the scope node.
        """
        
        # Initialize the frontier and visited set
        frontier = [self.problem_configuration.start_node]
        visited = set()
        
        curr_depth = 0
        print(f"The maximum depth to search to: {l}")
        
        # Loop through each node in the frontier until either the scope node is found or the maximum depth is reached
        while frontier and curr_depth < l:
            node = frontier.pop()
            visited.add(node)
            
            # If the scope node is found, reconstruct the path and return it
            if node == problem.scope_node:
                path = self.reconstruct_path(node)
                print("The length of the path:", len(path))
                self.show_path(path)
                return path
            
            # Otherwise, add the node's successors to the frontier if they have not been visited or added to the frontier before
            successors = self.get_successors(node)
            for successor in successors:
                if successor not in visited and successor not in frontier:
                    frontier.append(successor)
            
            curr_depth += 1
        
        # If the scope node is not found, print an error message and return None            
        print("Path not found!")
        return None
    

    def IDS(self) -> List[Node]:
        """
        Performs iterative deepening search on a given problem and returns the path from the start node to the scope node

        Returns:
            path (List[Node]): The path from the start node to the scope node.
        """
        
        for depth_limit in range(1, 100): # We set a maximum limit of 100 levels
            print(f"Current depth limit {depth_limit}")
            result = self.DLS(depth_limit)
            if result is not None:
                return result
            
        print("Path not found!")
        return None
    
    
if __name__ == "__main__":
    # Get class configuration
    class_grid, start_scope_nodes_names = read_input_file("project1_input.txt")
    problem = Problem(class_grid, start_scope_nodes_names)
    search = Search(problem)
    
    print("*" * 127)
    # measure the execution time of the BFS algorithm
    start_time_bfs = time()
    mem_usage = memory_usage(search.BFS, max_usage=True, max_iterations=1)
    end_time_bfs = time()
    execution_time = end_time_bfs - start_time_bfs
    print(f"Execution time of BFS search: {execution_time:.4f} seconds")
    print('Maximum memory usage of BFS: %s' % mem_usage)
    print("*" * 127)
    print()
    gc.collect()

    
    # delay the execution of the next search
    sleep(1)
    
    print("*" * 127)
    # measure the execution time of the DFS algorithm
    start_time_dfs = time()
    mem_usage = memory_usage(search.DFS, max_usage=True, max_iterations=1)
    end_time_dfs = time()
    execution_time = end_time_dfs - start_time_dfs
    print(f"Execution time of DFS search: {execution_time:.4f} seconds")
    print('Maximum memory usage of DFS: %s' % mem_usage)
    print("*" * 127)
    print()
    gc.collect()

    
    # delay the execution of the next search
    sleep(1)
    
    print("*" * 127)
    # measure the execution time of the DLS algorithm
    start_time_dls = time()
    mem_usage = memory_usage(search.DLS, max_usage=True, max_iterations=1)
    end_time_dls = time()
    execution_time = end_time_dls - start_time_dls
    print(f"Execution time of DLS search: {execution_time:.4f} seconds")
    print('Maximum memory usage of DLS: %s' % mem_usage)
    print("*" * 127)
    print()
    gc.collect()

    
    # delay the execution of the next search
    print("*" * 127)
    # measure the execution time of the IDS algorithm
    start_time_ids = time()
    mem_usage = memory_usage(search.IDS, max_usage=True, max_iterations=1)
    end_time_ids = time()
    print(f"Execution time of IDS search: {execution_time:.4f} seconds")
    print('Maximum memory usage of IDS: %s' % mem_usage)
    print("*" * 127)
    print()
    gc.collect()
