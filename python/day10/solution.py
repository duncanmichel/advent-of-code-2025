#!/usr/bin/python3
import logging
import sys
from io import IOBase
#import re 
import math
#from dataclasses import dataclass
from pprint import pprint
import itertools


TESTING_STATE = True
SUBMIT = True
logging_level = logging.DEBUG if TESTING_STATE else logging.INFO
logging.basicConfig(level=logging_level)
part1 = 1
part2 = 2

# custom constants
OFF='.'
ON='#'

class Solver:
    def __init__(self):
        test_filename = "input.test"
        live_filename = "input"
        self.input_filename = live_filename if SUBMIT else test_filename

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
        processed = list(map(str.strip,input_file.readlines()))
        return processed # will be passed as first argument to workSolution
    
    def workSolution(self,processed_input:list, starter_val:int) -> int:
        solution = 0
        factory_machines = [line.split() for line in processed_input]
        machine_tuples = [(machine[0], machine[1:-1], machine[-1]) for machine in factory_machines]
        for machine in machine_tuples:
            final_state_str,buttons_str_list,joltage_str = machine
            final_state = finalStateStrToInt(final_state_str)
            buttons_list = buttonsStrToList(buttons_str_list,len(final_state_str[1:-1]),starter_val)
            if starter_val == part2:
                logging.debug("==========================================")
                logging.debug(f"Converted buttons list: {[''.join(list(map(str,x))) for x in buttons_list]}")
            if starter_val == part2:
                joltage_list = joltageStrToList(joltage_str)
                logging.debug(f"Converted joltage list: {joltage_list}")
            solution += findFewestTotalPressesToStart(final_state,buttons_list) if starter_val == part1 else findFewestTotalPressesToConfig(joltage_list, buttons_list)
            #logging.debug(f"Current Solution Value: {solution}")
        return solution
    
    def testInput(self,solution:int,starter_val:int) -> bool:
        if starter_val == part1:
            return solution == 7 # expected result of part 1 test
        return solution == 33 # expected result of part 2 test

def finalStateStrToInt(state_str:str) -> int:
    bin_str = ''.join(['0' if x==OFF else '1' for x in state_str[1:-1]])
    #logging.debug(f"Converting state str: {state_str} to {bin_str}")
    return int(bin_str,2)

def buttonsStrToList(buttons_str_list:list[str],state_size:int,starter_val:int) -> list:
    #convert to list of tuples
    button_tuples = [tuple(map(int,x[1:-1].split(','))) for x in buttons_str_list]
    button_binary_list = [['1' if i in b else '0' for i in range(state_size)] for b in button_tuples]
    if starter_val == part1:
        return [int(''.join(x),2) for x in button_binary_list]
    return [list(map(int,b)) for b in button_binary_list]

def joltageStrToList(joltage_str:str) -> list[int]:
    return list(map(int,joltage_str[1:-1].split(',')))

def findFewestTotalPressesToStart(final_state:int,buttons_list:list[int]) -> int:
    presses = 1
    states = [0^press for press in buttons_list]
    #logging.debug(f"Starting states: {states}")
    while final_state not in states:
        next_iteration = [press^state for state in states for press in buttons_list for state in states]
        presses += 1
        
        states = list(set(next_iteration)) # set the new states, with de-duplication
        #logging.debug(f"Next iteration: {states}")
    return presses

def recursiveFindExclusive(joltage_list:list[int],current_buttons_list:list[list[int]],current_state:list[int],presses:int) -> (list[int],list[list[int]],int): # returns state after exclusive buttons pressed
    if joltage_list == current_state: # should never hit
            return current_state
    remaining_buttons = current_buttons_list # all are remaining at start
    # some joltages are exclusively incremented by pressing a single button. Let's increment them and remove the button
    exclusive_buttons = []
    for b_idx,b in enumerate(remaining_buttons):
        for j_idx,j in enumerate(b):
            if j == 1 and all([b[j_idx] != other[j_idx] for other in remaining_buttons[:b_idx] + remaining_buttons[b_idx+1:]]):
                exclusive_buttons.append((b_idx,j_idx))
    while len(exclusive_buttons) > 0:
        #logging.debug(f"Found exclusive buttons: {exclusive_buttons}")
        for b_idx,j_idx in exclusive_buttons:
            #logging.debug(f"bidx: {b_idx}, jidx: {j_idx}, state: {current_state}")
            incs = joltage_list[j_idx] - current_state[j_idx]
            presses += incs
            current_state = [current_state[i] + val * incs for i,val in enumerate(remaining_buttons[b_idx])]
        #logging.debug(f"State after pressing exclusive buttons: {current_state}")
        if joltage_list == current_state:
            return current_state, remaining_buttons,presses # return early if solution found after pressing only exclusive buttons
        # check for invalid state
        if any([joltage_list[i] < val for i,val in enumerate(current_state)]):
            #logging.error(f"Invalid state {current_state} for joltage {joltage_list}")
            return current_state, remaining_buttons, math.inf
        remaining_buttons = [b for idx,b in enumerate(remaining_buttons) if idx not in [x[0] for x in exclusive_buttons] ]
        #logging.debug(f"remaining buttons: {[''.join(list(map(str,x))) for x in remaining_buttons]}")
        exclusive_buttons = []
        for b_idx,b in enumerate(remaining_buttons):
            for j_idx,j in enumerate(b):
                if j == 1 and all([b[j_idx] != other[j_idx] for other in remaining_buttons[:b_idx] + remaining_buttons[b_idx+1:]]):
                    exclusive_buttons.append((b_idx,j_idx))
    return current_state,remaining_buttons, presses
    

def recursiveFindMin(joltage_list:list[int],current_buttons_list:list[list[int]],current_state:list[int],presses:int) -> int:
    if joltage_list == current_state: # solved
        return presses
    elif any([joltage_list[i] < val for i,val in enumerate(current_state)]): # no valid state from here
        return math.inf
    states = [current_state]
    remaining_buttons = current_buttons_list
    # find smallest joltage not reached
    min_idx = len(joltage_list)
    min_val = max(joltage_list)
    for idx,joltage in enumerate(joltage_list):
        j_diff = joltage - current_state[idx]
        if j_diff != 0: # 0 indicates joltage already reached in all states
            if j_diff < min_val:
                min_val = j_diff
                min_idx = idx
    if min_idx == len(joltage_list):
        logging.error(f"Failed to find max for joltage list {joltage_list}")
        sys.exit(1)
    #logging.debug(f"Attempting to reach new joltage val {joltage_list[min_idx]} at index {min_idx}")
    min_button_set = [b for b in remaining_buttons if b[min_idx] == 1]
    if min_button_set == []:
        #logging.error(f"Failed to find buttons to hit new joltage val {joltage_list[min_idx]} at index {min_idx}")
        return math.inf
        #sys.exit(1)
    #logging.debug(f"with buttons: {[''.join(list(map(str,x))) for x in min_button_set]}")
    next_iteration = [0]

    # create a set of states in which that joltage is reached
    while next_iteration != []:
        next_iteration = []
        #logging.debug(f"State to check: {len(states)}")
        for state in states:
            #new_state_size = len(next_iteration)
            for button in min_button_set:
                potential_state = [state[i]+val for i,val in enumerate(button)]
                
                if all([joltage_list[i] >= val for i,val in enumerate(potential_state)]):
                    if potential_state not in next_iteration: # check if valid final joltage and try to prevent duplication
                        next_iteration.append(potential_state)
                        #logging.debug(f"Adding potential state: {potential_state}")
                        # break early if match
                        if potential_state == joltage_list:
                            return presses + 1
                    else:
                        #logging.debug(f"Failed duplication check:{potential_state} ")
                        pass
                else:
                    #logging.debug(f"Failed joltage check: {potential_state} ")
                    pass
            # if len(next_iteration) == new_state_size and new_state_size > 0:
            #     logging.debug(f"no button press resulted in valid state; discarding: {state}")
        if next_iteration != []:  #list(next_iteration for next_iteration,_ in itertools.groupby(next_iteration)) #additional de-duplication
            states = next_iteration
            presses += 1 # make sure presses increments if a state progression is observed

    # remove any buttons that would increment that value further
    remaining_buttons = [b for b in remaining_buttons if b not in min_button_set]
    #logging.debug(f"remaining buttons: {[''.join(list(map(str,x))) for x in remaining_buttons]}")
    best = math.inf
    for s in states:
        t_s,t_b,t_p = recursiveFindExclusive(joltage_list,remaining_buttons,s,presses)
        best = min(best,recursiveFindMin(joltage_list,t_b,t_s,t_p))
    return best

def findFewestTotalPressesToConfig(joltage_list:list[int],buttons_list:list[list[int]]):
    presses = 0
    initial_state = [0 for i in range(len(joltage_list))]
    remaining_buttons = buttons_list # all are remaining at start
    # some joltages are exclusively incremented by pressing a single button. Let's increment them and remove the button
    initial_state,remaining_buttons,presses = recursiveFindExclusive(joltage_list,remaining_buttons,initial_state,presses)
    logging.debug(f"State after any initial exclusive buttons: {initial_state}")
    # # Then increment only buttons that can get to the smallest state, get there (exhaustively), then remove those buttons
    presses = recursiveFindMin(joltage_list,remaining_buttons,initial_state,presses)
    if presses == math.inf:
        logging.error(f"Failed to find valid presses")
        sys.exit(1)

    logging.debug(f"Returning after {presses} presses")
    return presses
    


def main():
    todaySolver = ContextualSolver()
    logging.info(f"Solving Part 1 with starter value {part1}")
    todaySolver.solve(part1)
    logging.info(f"Solving Part 2 with starter value {part2}")
    todaySolver.solve(part2)
    
if __name__ == "__main__":
    main()