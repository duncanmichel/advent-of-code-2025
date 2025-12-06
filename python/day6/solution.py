#!/usr/bin/python3
import logging
import sys
from io import IOBase
import re 
import math

TESTING_STATE = False
logging_level = logging.DEBUG if TESTING_STATE else logging.INFO
logging.basicConfig(level=logging_level)
part1 = 1
part2 = 2

# custom constants
MUL='*'
ADD='+'

class Solver:
    def __init__(self):
        test_filename = "input.test"
        live_filename = "input"
        self.input_filename = test_filename if TESTING_STATE else live_filename

    def processInput(self,input_file):
        assert isinstance(input_file, IOBase)
        logging.info("'processInput' Not Implemented")
        return None
    
    def readInput(self):
        try:
            with open(self.input_filename,'r') as input_file:
                processed = self.processInput(input_file)
            return processed
        except FileNotFoundError as e:
            logging.error(f"FileNotFoundError: {e}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"General Error: {e}")
            sys.exit(1)
    
    def workSolution(self,processed_input,initialization):
        assert processed_input == None
        assert initialization == 0
        logging.info("'workSolution' Not Implemented")
        return None
    
    def testInput(self,solution,initialization) -> bool:
        assert solution == None
        assert initialization == 0
        logging.info("'testInput' Not Implemented")
        return False
    
    def solve(self,initialization):
        solution = self.workSolution(self.readInput(),initialization) if initialization != 0 else None
        #testing
        if TESTING_STATE:
            try:
                assert self.testInput(solution,initialization)
                logging.debug("TEST PASSED")
            except:
                logging.error("TEST FAILURE")

        logging.info(f"Solution: {solution}")

class ContextualSolver(Solver):
    def __init__(self):
        super().__init__()

    def processInput(self,input_file):
        processed = input_file.readlines() #list(map(str.strip,input_file.readlines()))
        return processed # will be passed as first argument to workSolution
    
    def workSolution(self,processed_input:list, starter_val:int) -> int:
        operation_map,problems = parseAndTransform(processed_input,starter_val)
        logging.debug(f"Operations: {operation_map}")
        logging.debug(f"problems: {problems}")
        solution = calcSolution(operation_map,problems)
        return solution
    
    def testInput(self,solution:int,starter_val:int) -> bool:
        if starter_val == part1:
            return solution == 4277556 # expected result of part 1 test
        return solution == 3263827 # expected result of part 2 test

def parseAndTransform(processed_input:list[str],starter_val:int) -> (list[str],list[list[int]]):
    if starter_val == part1:
        file_data = [re.sub(r' +', ' ', line.strip()) for line in processed_input]
        op_map = file_data[-1].split()
        probs = [list(map(int,line.split(' '))) for line in file_data[:-1]]
        return op_map,transformProblems(probs)
    elif starter_val == part2:
        processed_input = [line.strip('\n') for line in processed_input]
        flipped_columns = [['' for row_idx in range(len(processed_input))] for col_idx in range(len(processed_input[0]))]
        for row_idx in range(len(processed_input)):
            for col_idx in range(len(processed_input[0])):
                flipped_columns[col_idx][row_idx] = processed_input[row_idx][col_idx]
        op_map = []
        probs = []
        prob_idx = -1
        for row in flipped_columns:
            int_str = ''.join(row[:-1]).strip()
            if int_str == '':
                continue
            if row[-1] != ' ':
                prob_idx += 1
                probs.append([])
                op_map.append(row[-1])
            probs[prob_idx].append(int(int_str))
        return op_map,probs

def transformProblems(probList:list[list[int]]) -> list[list[int]]:
    newProbList = [[] for i in range(len(probList[0]))]
    for row in range(len(probList)):
        for idx in range(len(newProbList)):
            newProbList[idx].append(probList[row][idx])
    #logging.debug(f"Transformed prob list: {newProbList}")
    return newProbList

def calcSolution(opMap:list[str], probList:list[list[int]]) -> int:
    sol = 0
    for idx in range(len(probList)):
        if opMap[idx] == MUL:
            sol += math.prod(probList[idx])
        elif opMap[idx] == ADD:
            sol += sum(probList[idx])
        else:
            raise Exception
    return sol


def main():
    todaySolver = ContextualSolver()
    logging.info(f"Solving Part 1 with starter value {part1}")
    todaySolver.solve(part1)
    logging.info(f"Solving Part 2 with starter value {part2}")
    todaySolver.solve(part2)
    
if __name__ == "__main__":
    main()