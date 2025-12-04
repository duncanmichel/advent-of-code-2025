#!/usr/bin/python3
import logging
import sys
from io import IOBase
import pprint

TESTING_STATE = False
logging_level = logging.DEBUG if TESTING_STATE else logging.INFO
logging.basicConfig(level=logging_level)

class Solver:
    def __init__(self):
        test_filename = "input.test"
        live_filename = "input"
        self.input_filename = test_filename if TESTING_STATE else live_filename

    def process_input(self,input_file):
        assert isinstance(input_file, IOBase)
        logging.info("'process_input' Not Implemented")
        return None
    
    def read_input(self):
        try:
            with open(self.input_filename,'r') as input_file:
                processed = self.process_input(input_file)
            return processed
        except FileNotFoundError as e:
            logging.error(f"FileNotFoundError: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"General Error: {e}")
            sys.exit(1)
    
    def work_solution(self,processed_input):
        assert processed_input == None
        logging.info("'work_solution' Not Implemented")
        return None
    
    def test_input(self,solution) -> bool:
        assert solution == None
        logging.info("'test_input' Not Implemented")
        return False
    
    def solve(self):
        solution = self.work_solution(self.read_input())
        #testing
        if TESTING_STATE:
            try:
                assert self.test_input(solution)
                logging.debug("TEST PASSED")
            except:
                logging.error("TEST FAILURE")

        logging.info(f"Solution: {solution}")

class ContextualSolver(Solver):
    def __init__(self):
        super().__init__()

    def process_input(self,input_file):
        processed = input_file.readlines()
        return processed
    
    def work_solution(self,grid_rows:list) -> int:
        printing_floor = [list(row.strip()) for row in grid_rows]
        movable_rolls, new_floor_grid = assess_adjacency(fill_adjacency_matrix(printing_floor),printing_floor)
        new_movable_rolls = 1
        while new_movable_rolls > 0:
            new_movable_rolls,new_floor_grid = assess_adjacency(fill_adjacency_matrix(new_floor_grid),new_floor_grid)
            movable_rolls += new_movable_rolls
        return movable_rolls
    
    def test_input(self,solution:int) -> bool:
        return solution == 43

def fill_adjacency_matrix(grid:list[list]) -> list[list]:
    adjacency_matrix = [[0 for row_item in range(0,len(grid[0]))] for row in range(0,len(grid))]
    for y in range(0,len(grid)):
        for x in range(0,len(grid[0])):
            here_roll_count = 1 if grid[y][x] == '@' else 0
            if y + 1 < len(grid): # if there is a row below
                if x + 1 < len(grid): # if there is a column to the right
                    if grid[y+1][x+1] == '@': # check diagonally toward bottom right
                        adjacency_matrix[y][x] += 1
                        adjacency_matrix[y+1][x+1] += here_roll_count
                if grid[y+1][x] == '@': # check position below in the same column
                    adjacency_matrix[y][x] += 1
                    adjacency_matrix[y+1][x] += here_roll_count
                    if x + 1 < len(grid): # if there is a column to the right
                        if grid[y][x+1] == '@': # check position to the right in the same row, help that position know about the diagonal
                            adjacency_matrix[y][x+1] += 1
                            adjacency_matrix[y+1][x] += 1

            if x + 1 < len(grid): # if there is a column to the right
                if grid[y][x+1] == '@': # check position to the right in the same row
                    adjacency_matrix[y][x] += 1
                    adjacency_matrix[y][x+1] += here_roll_count
            if here_roll_count == 0: # make empty positions impossibly adjacent so as to not call them "movable rolls of paper"
                adjacency_matrix[y][x] = 9
    if TESTING_STATE:
        logging.debug("Original Grid:")
        pprint.pprint(grid)
    if TESTING_STATE:
        logging.debug("Adjacency Matrix:")
        pprint.pprint(adjacency_matrix)
    return adjacency_matrix

def assess_adjacency(adj_grid:list[list],floor_grid:list[list]) -> int:
    movable = 0
    for y in range(0,len(adj_grid)):
        for x in range(0,len(adj_grid[0])):
            if adj_grid[y][x] < 4:
                movable += 1
                floor_grid[y][x] = '.' # remove the roll
    return movable, floor_grid


def main():
    todaySolver = ContextualSolver()
    todaySolver.solve()
    
if __name__ == "__main__":
    main()