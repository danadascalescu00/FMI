"""
    Author: Dăscălescu Dana, groupe 507, Artificial Intelligence
    
    Task requirements: 
        Develop an application that uses an Informed Search algorithm. This application can be the same as the one used in Project 1, 
        as it would be interesting to compare the performance of the two search algorithms.
    
    Problem description and requirements for applicability of A* algorithm:
        * Description: The students taking the Artificial Intelligence exam are arranged in rows of two-person benches in classroom 308.
        The benches are arranged in two columns. Diana wants to help her friend Calin by sending him the answers to the exam's grid
        through a message. A student can only pass the message to the bank colleague behind or in front of them, or the one right beside
        them, but not diagonally. Moreover, passing the message between rows is challenging since the teacher can easily notice it. As
        a result, only the penultimate and final banks on each row can be utilized for message transfer. Diana wants to include the 
        path she needs to take from one colleague to the next on the note to avoid getting lost in the classroom and reaching her 
        friend only after the exam ends. To make matters worse, some students are upset with each other or they disagree with cheating.
        This may make them unwilling to participate in the message transfer or report it to the TAs if they notice it happening. Therefore,
        Diana needs to be cautious about selecting trustworthy colleagues who are willing to help her.
        
        * Algorithm admissibility: 
            The following set of conditions must be met in order to ensure that the A* algorithm can find a minimum cost path to a goal node.
            These conditions include having a finite number of successors for any node in the graph that admits successors, having edges with
            weigths greater than a positive quantity µ (i.e. negative weights are not allowed), and ensuring that the heuristic function is
            admissible. Admissibility means that the heuristic function can never overestimate the cost of reaching the goal.

            Examples of admissible heuristics for our problem:
            I) Manhattan distance - the distance between two points measured along the axes at right angles.
                In a plane with points P1(x1, y1) and P2(x2, y2), it is equal to |x1 - x2| + |y1 - y2|. The Manhattan distance is often used
                when we can only move in four directions (North, West, South, East). 
                Since a student can pass the message (the note) to their seatmate or to the student behind or in front of them, but not 
                diagonally, we choose Manhattan distance as the heuristic evaluation of a node.
                
            II) Diagonal distance - it is often used when we can move in eight directions, similar to the king on a chessboard:
                    NW           N              NE
                        \        |         /
                    W  --   current_cell    --   E
                        /        |         \
                    SW           S              SE
    
            III) Euclidean distance - it is often used when we can move in any direction.
                Although though the Euclidean distance is smaller than the Manhattan or diagonal distance, and we will still have the 
                minimal cost path from a start node to a goal node, this heuristic will cause the A* algorithm to execute more slowly.
    
    A particular case of A* is the breadth-first algorithm. In this case, we have f^(n) = g^(n) = depth(n) for any node in the 
    search graph n, so h = 0, hence this is an admissible heuristic, but it does not provide search performance (it is an uninformed search).
"""

import re
import sys
import copy
import timeit

from typing import List, Tuple, Optional, Union

NUM_INPUT_FILES = 4
INPUT_FILE_NAME = '507_Dăscălescu_Dana_input_'

"""
Helpers function
"""
def read_class_info(input_file_name: str) -> Tuple[List[List[str]], List[List[str]], List[str]]:
    """
    Reads the input file and returns a tuple containing the class information, upset children, and message.

    Args:
    input_file_name (str): The name of the input file.

    Returns:
    Tuple[List[List[str]], List[List[str]], List[str]]: A tuple containing the class information,
    upset children, and message.

    Raises:
    FileNotFoundError: If the input file is not found.
    ValueError: If the input format is invalid.
    """
    try:
        with open(input_file_name, "r") as input_file:
            class_info, upset_children, message = [], [], []
            
            for line in input_file:
                if 'angry' in line:
                    break
                
                try:
                    name = line.split()
                except ValueError:
                    raise ValueError("Invalid input format!")

                class_info.append(name)

            for line in input_file:
                if 'message' in line:
                    message = re.split('[:>,-]', line)
                    del message[0], message[1]
                    message[0] = message[0].strip()
                    message[1] = message[1].strip()
                    break

                upset_children.append(line.split())

            return class_info, upset_children, message
           
    except FileNotFoundError:
        print("Input file not found!")
        sys.exit()
    

def show_classroom(classroom_grid: List[List[str]]) -> None:
    """
    Prints the classroom grid to the console.

    Args:
        classroom_grid: A 2D list representing the classroom grid.

    Returns:
        None
    """
    for row in classroom_grid:
        print(row)


"""
Problem Definition
"""
class Configuration:
    def __init__(self, matrix: List[List], message: str) -> None:
        self.matrix = matrix
        self.seating_arrangement = self.generate_seating_arrangement()
        self.message_position = self.get_message_position(message)


    def generate_seating_arrangement(self) -> dict:
        """
        Generate a dictionary that maps the names of children to their positions in the seating arrangement.

        The dictionary keys are the names of the children, and the values are tuples (i, j) representing the row and
        column indices of their positions in the classroom.
        """
        seating_arrangement = {}
        for i, row in enumerate(self.matrix):
            for j, child in enumerate(row):
                seating_arrangement[child] = (i, j)
        return seating_arrangement


    def get_message_position(self, child_name) -> tuple:
        """
        Return the position of the message associated with the given child name.

        Args:
            child_name (str): The name of the child.

        Returns:
            tuple: A tuple (i, j) representing the row and column indices of the child's position in the classroom.
        """
        return self.seating_arrangement.get(child_name)


    def manhattan_distance(self) -> int:
        """
        Compute the Manhattan distance between the current configuration and the final configuration.

        The Manhattan distance is the sum of the absolute differences between the row and column indices of the message
        positions in the current configuration and the final configuration.

        Returns:
            int: The Manhattan distance between the current configuration and the final configuration.
        """
        global final_configuration
        return abs(self.message_position[0] - final_configuration.message_position[0]) \
            + abs(self.message_position[1] - final_configuration.message_position[1])

    def diagonal_distance(self) -> int:
        """
        Compute the diagonal distance between the current configuration and the final configuration.

        The diagonal distance is the maximum of the absolute differences between the row and column indices of the message
        positions in the current configuration and the final configuration.

        Returns:
            int: The diagonal distance between the current configuration and the final configuration.
        """
        global final_configuration
        return max(abs(self.message_position[0] - final_configuration.message_position[0]), \
            abs(self.message_position[1] - final_configuration.message_position[1]))

    def __eq__(self, other) -> bool:
        """
        Test whether two configurations are equal based on the positions of their messages.

        Args:
            other (Configuration): The other configuration to compare.

        Returns:
            bool: True if the two configurations have messages in the same position, False otherwise.
        """
        return self.message_position == other.message_position

    def __repr__(self) -> str:
        """
        Return a string representation of the configuration based on the position of the message.

        Returns:
            str: A string representation of the configuration based on the position of the message.
        """
        return f"{self.matrix[self.message_position[0]][self.message_position[1]]}"
    
    
class Node:
    def __init__(self, configuration) -> None:
        """
        Constructor for Node class. Initializes Node object with the given configuration.

        :param configuration: Configuration object.
        :type configuration: Configuration
        """
        self.info = configuration
        self.h = configuration.manhattan_distance()

    def __str__(self) -> str:
        """
        Returns string representation of the Node object.

        :return: String representation of the Node object.
        :rtype: str
        """
        return "{}".format(self.info)
    
    def __repr__(self) -> str:
        """
        Returns string representation of the Node object.

        :return: String representation of the Node object.
        :rtype: str
        """
        return f'{self.info}'
    
    
class Edge:
    """
    A class that represents an edge between two nodes in a graph.
    """
    def __init__(self, start_node: Node, end_node: Node) -> None:
        """
        Initializes a new instance of the Edge class.

        Args:
            start_node (Node): The index of the starting node of the edge.
            end_node (Node): The index of the ending node of the edge.
        """
        self.start_node = start_node
        self.end_node = end_node
        self.cost = 1 # The cost of transmitting a message from one child to another is 1
    
    def __repr__(self) -> str:
        """
        Returns a string representation of the edge.

        Returns:
            str: A string representation of the edge.
        """
        return f"Edge(start_node={self.start_node}, end_node={self.end_node}, cost={self.cost})"
    

class Problem:
    def __init__(self, initial_configuration: list, final_configuration: list) -> None:
        """
        Initializes a new instance of the Problem class.

        Args:
            initial_configuration (list): The initial configuration of the problem.
            final_configuration (list): The final configuration of the problem.
        """
        self.nodes = [
            Node(initial_configuration)
        ]
        self.edges = []
        self.start_node = self.nodes[0]
        self.goal_node = final_configuration

    def find_node_by_configuration(self, configuration: list) -> Optional[Node]:
        """
        Finds a node in the list of nodes that has the given configuration.

        Args:
            configuration (list): The configuration to search for.

        Returns:
            Node or None: The node with the given configuration, or None if it is not found.
        """
        for node in self.nodes:
            if node.configuration == configuration:
                return node
        return None
            
            
class NodeTraversal:
    """
    A class that contains information associated with a node in the open/closed lists.
    Contains a reference to the node itself (from the graph), but also has properties specific to the A* algorithm
    (heuristic evaluation function f, g, an estimate of the depth of a node n in the graph, i.e. the length of the shortest path
    from the starting node to n). It is assumed that h (the heuristic evaluation of a node) is a property of the node in the graph.
    """
    problem: Problem # Reference to the Problem instance associated with the search

    def __init__(self, graph_node: Node, parent_node: Union[None, Node] = None, g_cost: int = 0, f_cost: Optional[int] = None) -> None:
        """
        Initializes a new NodeTraversal instance.
        :param graph_node: The Node instance associated with this traversal node.
        :param parent_node: The parent NodeTraversal instance, if any.
        :param g_cost: The cost of the path from the starting node to this node.
        :param f_cost: The estimated total cost from the starting node to the goal node, through this node.
        """
        self.graph_node = graph_node
        self.parent_node = parent_node
        self.g_cost = g_cost  # cost of the path from the root to the current node
        if f_cost is None:
            self.f_cost = self.g_cost + self.graph_node.h
        else:
            self.f_cost = f_cost

    def get_path(self) -> List[Node]:
        """
        Returns the path associated with this node traversal, from the starting node to this node.
        :return: A list of Node instances representing the path from the starting node to this node.
        """
        current_node = self
        path = [current_node.graph_node]
        while current_node.parent_node is not None:
            path = [current_node.parent_node] + path
            current_node = current_node.parent_node
        return path

    def contains_node(self, node: Node) -> bool:
        """
        Checks whether a node is contained in the path from the starting node to this node.
        :param node: The Node instance to check.
        :return: True if the given node is in the path from the starting node to this node, False otherwise.
        """
        current_node = self
        while current_node.parent_node is not None:
            if current_node.graph_node.info == node.info:
                return True
            current_node = current_node.parent_node
        return False

    def expand(self) -> List[Tuple[Node, int]]:
        """
        Returns a list of all possible successor nodes of this node, along with their edge costs.
        :return: A list of tuples (successor, cost), where successor is a NodeTraversal instance representing a successor
                node of this node, and cost is the cost of the edge between this node and the successor node.
        """
        global num_rows, num_cols, classroom

        current_message_position = self.graph_node.info.message_position
        valid_moves = [[1, 0], [0, 1], [0, -1], [-1, 0]]

        successors = []
        for move in valid_moves:
            new_position = [current_message_position[0] + move[0], current_message_position[1] + move[1]]
            # Check if the new position is valid
            if 0 <= new_position[0] < num_rows and 0 <= new_position[1] < num_cols:
                name1 = classroom[current_message_position[0]][current_message_position[1]]
                name2 = classroom[new_position[0]][new_position[1]]
                if can_pass_on_message(name1, name2):
                    new_class = copy.deepcopy(classroom)
                    new_config = Configuration(new_class, name2)
                    successor = Node(new_config)
                    successors.append((successor, 1))
        return successors

    def is_goal(self) -> bool:
        """
        Returns True if the current graph node is the goal node of the problem, False otherwise.
        """
        return self.graph_node.info == self.problem.goal_node

    def __str__(self) -> str:
        """
        Returns a string representation of the current node traversal object, showing the path from the root node to
        the current node. The string contains arrows that indicate the direction of the path, as well as the message
        associated with the current graph node.
        """
        parent = self.parent_node if self.parent_node is None else self.parent_node.graph_node.info
        if parent is None:
            return f"{self.graph_node.info}"
        else:
            pos1, pos2 = self.parent_node.graph_node.info.message_position, self.graph_node.info.message_position
            if pos1[0] > pos2[0]:
                return f" ^  {self.graph_node.info}"
            elif pos1[0] < pos2[0]:
                return f" v  {self.graph_node.info}"
            elif pos1[1] < pos2[1]:
                if pos1[1] % 2 == 1:
                    return f" >> {self.graph_node}"
                return f" > {self.graph_node}"
            elif pos1[1] > pos2[1]:
                if pos1[1] % 2 == 1:
                    return f" << {self.graph_node}"
                return f" < {self.graph_node}"
            return f"{self.graph_node}"
               
        
"""
Helper functions for A* algorithm
"""
def node_info_str(node_list: List[Node]) -> str:
    """
    Returns a string representation of a list of nodes.
    """
    global classroom
    
    num_rows = len(classroom)
    result = "[ "
    if len(node_list) > 0:
        for node in node_list:
            if node is not None:
                result += str(node) + "  "
        result += "]"

    return result


def successor_info_str(successors: List[Node]) -> str:
    """
    Returns a string representation of a list of successor nodes.
    """
    return "".join(["\nnod: "+ str(node) +", cost arc: "+ str(cost) for (node, cost) in successors])


def find_node_in_list(node_list: List[Node], node: Node) -> Optional[Node]:
    """
    Given a list of graph nodes and a target node, returns the first node in the list with the same info as the target node,
    or None if no such node is found.
    """
    for i in range(len(node_list)):
        if node_list[i].graph_node.info == node.info:
            return node_list[i]
    return None


def are_kids_angry(kid1: Node, kid2: Node) -> bool:
    """
    Check if two kids are in an angry pair.
    """
    global upset_students_pairs
    for pair in upset_students_pairs:
        if (kid1 == pair[0] and kid2 == pair[1]) or (kid2 == pair[0] and kid1 == pair[1]):
            return True
    return False


def can_pass_on_message(bank1, bank2) -> bool:
    """
    Check if a message can be passed from bank1 to bank2.
    """
    global start_configuration
    global num_rows
    
    if "X" in bank1 or "X" in bank2:
        return False
    elif are_kids_angry(bank1, bank2):
        return False
    else:
        pos1, pos2 = start_configuration.get_message_position(bank1), start_configuration.get_message_position(bank2)
        if pos1[1] > pos2[1]:
            pos1, pos2 = pos2, pos1
        
        # Check if kids are on different columns
        if (pos1[1] % 2 == 1 and pos2[1] % 2 == 0):
            # Kids can only pass on a message between columns if they are in the last two rows (on the same row)
            if pos1[0] != pos2[0] or pos1[0] < num_rows - 2:
                return False
        # If they are on the same column, check if they are NEIGHBOURS or if they are on different rows (they can't pass on the message diagonally)
        elif pos1[0] != pos2[0] and pos1[1] != pos2[1]:
            return False 
    
    return True
     
            
            

def a_star(output_file):
    """
    Runs the A* algorithm to find the minimum cost path from the start node to the goal node in a given problem,
    and writes the results to a file.
    :param output_file: The name of the file to write the results to.
    """
    start_time = timeit.default_timer()

    tree_root = NodeTraversal(NodeTraversal.problem.start_node)
    OPEN = [tree_root]
    closed = []
    scope_node_found = False

    while len(OPEN) > 0:
        # the first node is extracted from the OPEN list and put into the CLOSED list
        current_node = OPEN.pop(0)
        closed.append(current_node)

        # if the current node is the goal node, the search is stopped
        if current_node.is_goal():
            scope_node_found = True
            break

        successors = current_node.expand() # the current node is expanded, obtaining its successors in the graph
        for (successor_node, successor_cost ) in successors:
            # checking if the successor is not on the path between the root and its parent (to avoid forming a circuit)
            if not current_node.contains_node(successor_node):
                # successors that are on the path from the start node to the current node will not be considered
                g_succesor = current_node.g_cost + successor_cost 
                f_succesor = g_succesor + successor_node.h

                """
                "For all successors that are already in the OPEN or CLOSED lists, if a lower f value is obtained for the path that passes through the current_node, 
                their parent is changed to current_node, and their f value is updated. Afterwards, they will be repositioned in the OPEN list.
                """
                old_traversal_node  = find_node_in_list(closed, successor_node)
                if old_traversal_node is not None:
                    if f_succesor < old_traversal_node .f_cost:
                        closed.remove(old_traversal_node)
                        old_traversal_node.parent_node = current_node
                        old_traversal_node.g_cost = g_succesor
                        old_traversal_node.f_cost = f_succesor
                        new_node = old_traversal_node 
                else:
                    old_traversal_node  = find_node_in_list(OPEN, successor_node)
                    if old_traversal_node is not None:
                        if f_succesor < old_traversal_node .f_cost:
                            OPEN.remove(old_traversal_node)
                            old_traversal_node.parent_node = current_node
                            old_traversal_node.g = g_succesor
                            old_traversal_node.f = f_succesor
                            new_node = old_traversal_node 
                    else: # when the successor_node is not in either the closed or open set
                        new_node = NodeTraversal(graph_node=successor_node, parent_node=current_node, g_cost=g_succesor)

                if new_node:
                    """
                    All successors are inserted into the OPEN list in such a way that it continues to be ordered in ascending order based on f.
                    If there are two nodes with the same f value, the node with the greater g value is placed first.
                    """
                    i = 0
                    while i < len(OPEN):
                        if OPEN[i].f_cost < new_node.f_cost:
                            i += 1
                        else:
                            while i < len(OPEN) and OPEN[i].f_cost == new_node.f_cost and OPEN[i].g_cost > new_node.g_cost:
                                i += 1
                            break
                    OPEN.insert(i, new_node)

    write_path(output_file, OPEN, scope_node_found, current_node, start_time)



def write_path(output_file: str, open_list: List[Node], scope_node_found: bool, scope_node: Node, start_time: float) -> None:
    """    Writes the path found by the algorithm to a file, along with the execution time.

    Args:
        output_file (str): the name of the file to write the output to.
        open_list (List[Node]): the list of nodes in the open set.
        scope_node_found (bool): a boolean indicating if the goal node has been found.
        scope_node (Node): the goal node.
        start_time (float): the starting time of the algorithm.
    """
    try:
        with open(output_file, "w+") as fout:
            fout.write("\n------------------ Conclusion -----------------------\n")
            if len(open_list) == 0:
                if scope_node_found:
                    fout.write("The start node is also the root node.")
                else:
                    fout.write("The OPEN list is empty, we don't have a path from the start node to the goal node.")
            else:
                fout.write("Minimum cost path:\n" + node_info_str(scope_node.get_path()))
            fout.write("\nExecution time: ")
            fout.write(str(timeit.default_timer() - start_time))
    except Exception as e:
        print(f"Error: {e}.")



if __name__ == "__main__":
    for it in range(1, NUM_INPUT_FILES + 1):
        # read the problem definition
        current_input_file = INPUT_FILE_NAME + str(it) + ".txt"
        current_output_file = INPUT_FILE_NAME + str(it) + "_output.txt"
        
        classroom, upset_students_pairs, message = read_class_info(current_input_file) 
        num_rows, num_cols = len(classroom), len(classroom[0])       
        show_classroom(classroom)
        
        start_configuration = Configuration(classroom, message[0])
        final_configuration = Configuration(classroom, message[1])
        
        problem = Problem(start_configuration, final_configuration)
        NodeTraversal.problem = problem
        a_star(current_output_file)
            
