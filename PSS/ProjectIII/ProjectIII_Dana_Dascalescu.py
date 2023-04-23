"""
    Author: Dăscălescu Dana, groupe 507, Artificial Intelligence
    
    Task requirements: 
        Develop an application that uses an Informed Search algorithm. This application can be the same as the one used in Project 1, as 
        it would be interesting to compare the performance of the two search algorithms.
    
    Problem formulation:
        In classroom 308, students taking the Artificial Intelligence exam are seated on two-person benches arranged in rows and columns.
        Some of the seats are empty. Ana wants to help her colleague Vlad succeed on the exam by giving him the correct answers. There 
        are restrictions on how notes may be sent, however. Students are only able to communicate with a fellow student who is 
        immediately behind, in front of, or next to them. Furthermore, it is difficult to interact across rows since the teacher may see
        students attempting to share notes. The feasible options for message transfer are limited to the last seats in each row.
        Therefore, the challenge at hand is to devise an optimal strategy for Ana to transfer the answers to Vlad within the given 
        restrictions.


"""
import sys
import random

from typing import List, Tuple, Dict


LIST_STUDENTS = 'input.txt'
LIST_UPSET_PAIRS = 'upset_students.txt'

"""
Helper functions 
"""
def read_strings_from_file(file_path):
    """
    Reads a list of strings from a file, with each string placed in a different row.
    :param file_path: the path to the input file
    :return: a list of strings
    """
    try:
        with open(file_path, 'r') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        print(f'File {file_path} not found.')
        sys.exit(1)
        

def get_classroom_information(students_names_path: str, upset_pairs_path: str) -> Tuple[List[str], List[List[str]]]:
    """
    Reads the names of the students and the upset pairs from the input files and returns them as lists.

    Args:
        students_names_path: The path to the file containing the names of the students.
        upset_pairs_path: The path to the file containing the upset pairs.

    Returns:
        A tuple containing the list of students names and the list of upset pairs.
    """
    students_names = read_strings_from_file(students_names_path)
    upset_pairs = [line.split() for line in read_strings_from_file(upset_pairs_path)]
    return students_names, upset_pairs


class Classroom:
    def __init__(self, n_rows: int, n_cols: int) -> None:
        """
        Initializes a Classroom object with a given number of rows and columns.
        Args:
            n_rows (int): The number of rows in the classroom.
            n_cols (int): The number of columns in the classroom.
        """
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.grid = [[None] * n_cols for _ in range(n_rows)]
        self.students = []
        
    def add_student(self, row: int, col: int, name: str, trustworthiness: float):
        """
        Adds a student to the classroom at the given row and column.
        
        Args:
            row (int): The row in which the student will be seated.
            col (int): The column in which the student will be seated.
            name (str): The name of the student.
            trustworthiness (float): A measure of how trustworthy the student is.
        """
        self.grid[row][col] = len(self.students)
        self.students.append({'row': row, 'col': col, 'name': name.strip(), 'trustworthiness': trustworthiness})
        
    @classmethod
    def create_class_from_list_of_students(cls, names: List[str]) -> 'Classroom':
        """
        Creates a new Classroom object from a list of students' names.

        Args:
            names (List[str]): A list of students' names.

        Returns:
            Classroom: A new Classroom object with a seting arrangement represented as a grid based on the given list of students' names.
        """
        n_cols: int = 4 # number of seats per row
        n_rows: int = (len(names) + 1) // 4
        classroom: Classroom = cls(n_rows, n_cols)
        for i, name in enumerate(names):
            row: int = i // n_cols
            col: int = i % n_cols
            # add student with a random trustworthiness value between 0.1 and 1.0
            classroom.add_student(row, col, name, random.uniform(0.1, 1.0))
        return classroom
    
    def get_coordinates(self, student_index: int) -> Tuple[int, int]:
        """
        Returns the coordinates of the seat where the student with the given index is sitting.

        Args:
            student_index (int): The index of the student in the list of students.

        Returns:
            Tuple[int, int]: The row and column coordinates of the student's seat.
        """
        return self.students[student_index]['row'], self.students[student_index]['col']
    
    def get_index(self, row: int, col: int) -> int:
        """
        Returns the index of the student sitting at the given coordinates.

        Args:
            row (int): The row coordinate of the student's seat.
            col (int): The column coordinate of the student's seat.

        Returns:
            int: The index of the student in the list of students.
        """
        return self.grid[row][col]
        
    def is_valid(self, row: int, col: int, neighbor_row: int, neighbor_col: int) -> bool:
        """
        Checks if the given neighbor is a valid option for message transfer.

        Args:
            row (int): row index of the student in the grid representation of the classroom
            col (int): column index of the student in the grid representation of the classroom
            neighbor_row (int): row index of the student' neighbor in the grid representation of the classroom
            neighbor_col (int): col index of the student' neighbor in the grid representation of the classroom

        Returns:
            bool: True if the neighbor is a valid option for message transfer, False otherwise.
        """
        if neighbor_row < 0 or neighbor_row >= self.n_rows or neighbor_col < 0 or neighbor_col >= self.n_cols: # neighbor is within the classroom boundaries
            return False
        
        student_index = self.grid[neighbor_row][neighbor_col]
        if self.students[student_index]['name'] == 'X': # empty seat
            return False
        
        if are_students_upset(self.students[self.grid[row][col]], self.students[self.grid[neighbor_row][neighbor_col]]): # students are upset
            return False
        
        # Check if the message can be passed on different columns
        # Students can pass the message to another column of two benches only if they are sitting in the last two rows of the classroom
        if col % 2 == 1 and neighbor_col % 2 == 0 and col < neighbor_col:
            if row < (self.n_rows - 3):
                return False
            return True
        elif col % 2 == 0 and neighbor_col % 2 == 1 and col > neighbor_col:
            if row < (self.n_rows - 3):
                return False
            return True
        
        return True
        
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        This function returns a list of the valid neighbors (i.e., students that are trustworthy and can pass the message forward) of the 
        student at the given row and column.

        Args:
            row (int): the row index of the student in the classroom grid
            col (int): the column index of the student in the classroom grid

        Returns:
            List[Tuple[int, int]]: a list of coordinates of the valid neighbors of the student
        """
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if abs(dr) + abs(dc) == 1 and self.is_valid(row, col, row + dr, col + dc):
                    neighbors.append((row + dr, col + dc))
        return neighbors
        
    def get_distance(self, i: int, j: int) -> int:
        """
        Returns the Manhattan distance between the positions in class of two students, i.e. the sum in abslute differences in row and column.

        Args:
            i (int): index of the first student
            j (int): index of the second student

        Returns:
            int: the Manhattan distance between the positions in class of the two students
        """
        si = self.students[i]
        sj = self.students[j]
        return abs(si['row'] - sj['row']) + abs(si['col'] - sj['col'])
        
    def get_cost(self, path: List[int], trustworthiness: Dict[Tuple[int, int], float]) -> float:
        """
        Returns the total cost of a fiven path of students, where the cost is the sum of the distances weighted by the trustworthiness of the students.
        """
        cost = 0.0
        for i in range(len(path) - 1):
            j = i + 1
            d = self.get_distance(path[i], path[j])
            t =  1. / (trustworthiness.get((path[i], path[j]), 0.0) + 1e-7)
            cost += d * t
        return cost
        
    def get_trustworthiness(self) -> Dict[Tuple[int, int], float]:
        """
        Returns a dictionary of trustworthiness values for each seat in the classroom.
        """
        n_cols = 4
        trustworthiness = {}
        for i in range(len(self.students)):
            row = i // n_cols
            col = i % n_cols
            trustworthiness[(row, col)] = self.students[i]['trustworthiness']
        return trustworthiness
    
    
def show_classroom(classroom: Classroom) -> None:
    """
    Prints the classroom grid to the console.

    Args:
        classroom (Classroom): Classroom object representing the classroom layout.
    """
    for row in classroom.grid:
        for idx_student in row:
            print(classroom.students[idx_student]['name'], end=' ')
        print()
        

def are_students_upset(student1: Dict, student2: Dict) -> bool:
    """
    Check if two students are upset with each other.

    Args:
        student1 (str): Name of the first student.
        student2 (str): Name of the second student.

    Returns:
        bool: True if the two students are upset with each other, False otherwise.
    """
    global upset_pairs
    
    for pair in upset_pairs:
        if (student1['name'] == pair[0] and student2['name'] == pair[1]) or \
        (student1['name'] == pair[1] and student2['name'] == pair[0]):
            return True
    return False

        
def initial_solution(classroom, start: int, end: int, max_attempts: int = 10000) -> List[int]:
    """
    Generates an initial path starting at the given start index and ending at the given end index.

    Args:
        classroom: The Classroom object representing the classroom layout.
        start: The index of the starting point in the path.
        end: The index of the ending point in the path.

    Returns:
        A list of grid point indices representing the initial path.
    """
    path = [start]
    check_unvisited = 0
    attempts = 0
    
    # Keep loooping until the end index is reached or the maximum number of attempts have been reached
    while path[-1] != end and attempts < max_attempts:
        attempts += 1
        row, col = classroom.get_coordinates(path[-1])
        # Get the neighbors of the last point in the path
        neighbors = classroom.get_neighbors(row, col) 
        #  Remove any neighbors that are already in the path
        unvisited_neighbors = [n for n in neighbors if classroom.get_index(*n) not in path]
        # If there are no unvisited neighbors, backtrack to the previous point in the path
        if not unvisited_neighbors:
            path.pop()
            check_unvisited += 1     
            if check_unvisited > 5: # If there are no unvisited neighbors for 5 consecutive steps, restart the building of the path
                path = [start]
                check_unvisited = 0
        else:
            # Choose a random unvisited neighbor to add to the path
            next_point = random.choice(unvisited_neighbors)
            path.append(classroom.get_index(*next_point))
            
    
    if attempts == max_attempts:
        print("Could not generate an initial path.")
        sys.exit(1)
    
    return path
    

def hill_climbing(classroom, start_name: str, end_name: str, max_iterations: int = 10000) -> List[str]:
    """
    Uses the hill-climbing algorithm to find a path through the classroom
    that minimizes the total cost of interactions between students.

    Args:
    - classroom: a Classroom object representing the classroom layout and student data
    - start_name: the name of the student at the beginning of the path
    - end_name: the name of the student at the end of the path
    - max_iterations: the maximum number of iterations to perform

    Returns:
    - a list of student names representing the optimal path through the classroom
    """

    # convert student names to indices
    start_index = classroom.students.index(next((s for s in classroom.students if s['name'] == start_name), None))
    end_index = classroom.students.index(next((s for s in classroom.students if s['name'] == end_name), None))
    
    if start_index is None or end_index is None: # if either student name is invalid
        print("Invalid student name(s).")
        sys.exit(1)
    elif are_students_upset(classroom.students[start_index], classroom.students[end_index]): # if the students are upset with each other
        print("Students are upset with each other. They definetely wouldn't want to pass each other a message")
        sys.exit(1)
    elif start_index == end_index: # if the students are the same
        print("Wrong input! Sender and receiver are the same person.")
        sys.exit(1)

    # calculate trustworthiness and initial path cost
    trustworthiness = classroom.get_trustworthiness()
    current_path = initial_solution(classroom, start_index, end_index)
    current_cost = classroom.get_cost(current_path, trustworthiness)

    # iterate until max_iterations or until a local minimum is reached    
    for _ in range(max_iterations):
        neighbors = []

        # generate all neighboring paths by reversing a subsequence of the current path
        for j in range(len(current_path) - 1):
            for k in range(j + 1, len(current_path)):
                if classroom.get_distance(current_path[j], current_path[k]) <= 1:
                    neighbor = current_path[:j] + current_path[j:k][::-1] + current_path[k:]
                    neighbors.append(neighbor)

        # calculate the cost of each neighboring path
        neighbor_costs = [classroom.get_cost(neighbor, trustworthiness) for neighbor in neighbors]

        # find the neighbor with the lowest cost
        best_neighbor_index = neighbor_costs.index(min(neighbor_costs))
        best_neighbor_cost = neighbor_costs[best_neighbor_index]

        # if the lowest cost neighbor is better than the current path, update the current path and cost
        if best_neighbor_cost < current_cost:
            current_path = neighbors[best_neighbor_index]
            current_cost = best_neighbor_cost
        else:
            # if no neighbor is better than the current path, terminate the search
            break

    # convert indices to student names
    if current_path:
        path_names = [classroom.students[i] for i in current_path]

    return path_names


def show_path(path: List[Dict]) -> None:
    """
    Prints the path to the console.

    Args:
        path (List[Dict]): List of students in the path.
    """
    print("Path: ", end='')
    for idx, student in enumerate(path):
        if idx == len(path) - 1:
            print(student['name'])
        else:
            print(student['name'], end=' -> ')
        

if __name__ == "__main__":
    try:
        students_names, upset_pairs = get_classroom_information(LIST_STUDENTS, LIST_UPSET_PAIRS)
        # Create a Classroom instance from the list of student names
        classroom = Classroom.create_class_from_list_of_students(students_names)
        # Display the classroom grid
        show_classroom(classroom)
        
        while True:
            start_path = input("Enter the name of the students who is the sender: ")
            start_path = start_path.lower().strip()
            if start_path not in students_names:
                print("Invalid student name.")
                continue
            
            end_path = input("Enter the name of the students who is the receiver: ")
            end_path = end_path.lower().strip()
            if end_path not in students_names:
                print("Invalid student name.")
                continue
            break
                
        # Find a path from the sender to the receiver using the hill-climbing algorithm 
        path = hill_climbing(classroom, start_path, end_path)
        if len(path) == 0:
            print("No path found.")
        else:
            show_path(path)
            
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    