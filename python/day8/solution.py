#!/usr/bin/python3
import logging
import sys
from io import IOBase
#import re 
#import math
from dataclasses import dataclass
import math
from pprint import pprint
import bisect


TESTING_STATE = False
SUBMIT = True
logging_level = logging.DEBUG if TESTING_STATE else logging.INFO
logging.basicConfig(level=logging_level)
part1 = 1
part2 = 2

# custom constants
SPLIT='^'

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
        solution = 99
        junctions = [list(map(int,row.split(','))) for row in processed_input]
        if starter_val == 1:
            limit = 1000 if SUBMIT else 10
        elif starter_val == 2:
            limit = len(junctions)*len(junctions)
        closest_boxes_list = findAllShortest(junctions,limit)
        return_val = connectBoxes(closest_boxes_list,junctions)
        if starter_val == 1:
            return return_val
        elif starter_val == 2:
            (box1,box2) = return_val
            b1_x = list(map(int,box1[1:-1].split(',')))[0]
            b2_x = list(map(int,box2[1:-1].split(',')))[0]
            return b1_x * b2_x
        return solution
    
    def testInput(self,solution:int,starter_val:int) -> bool:
        if starter_val == part1:
            return solution == 40 # expected result of part 1 test
        return solution == 25272 # expected result of part 2 test

def calcDist(point1:list[int],point2:list[int]) -> float:
    return math.dist(tuple(point1),tuple(point2))

def findAllShortest(junction_list:list[list[int]],limit:int) -> list[tuple]:
    first_box = junction_list[0]
    closest_boxes_list = [(calcDist(first_box,x),str(first_box),str(x)) for x in junction_list[1:]]
    closest_boxes_list.append((math.inf,"impossible1","impossible2"))
    closest_boxes_list = sorted(closest_boxes_list, key=lambda x: x[0])
    #logging.debug(f"initial sorted list: {closest_boxes_list}")
    max = math.inf
    for idx,junction in enumerate(junction_list[1:]):
        junc_key = str(junction)
        if idx == len(junction_list) - 1: # last item, don't perform follow-on checks
            break
        for next_junction in junction_list[idx+2:]:
            n_junc_key = str(next_junction)
            this_dist = calcDist(junction,next_junction)
            if this_dist < max:
                #logging.debug(f"removing {closest_boxes_list.pop()}") # remove largest item from end
                if limit < len(junction_list) + 1:
                    closest_boxes_list.pop()
                bisect.insort(closest_boxes_list,(this_dist,junc_key,n_junc_key), key=lambda x: x[0])
                max = closest_boxes_list[-1][0]
    return closest_boxes_list[:limit]

def connectBoxes(closest_boxes_list:list[int],junction_list:list[list[int]]) -> dict:
    junction_map = {str(x):False for x in junction_list}
    circuit_groups = {}
    group_id = 0
    for dist,box1,box2 in closest_boxes_list:
        #logging.debug(f"box1:{box1}: {junction_map[box1]}, box2:{box2}: {junction_map[box2]}")
        if junction_map[box1] == junction_map[box2]: # both connected or both disconnected
            if junction_map[box1]: # both connected
                box1_gid = 0
                box2_gid = 0
                for gid,group_list in circuit_groups.items():
                    if box1 in group_list:
                        box1_gid = gid
                        if box2 in group_list:
                            box2_gid = gid
                    elif box2 in group_list:
                        box2_gid = gid
                    if box1_gid > 0 and box2_gid > 0: # we found both locations
                        break
                if box1_gid == box2_gid: # they are already connected on the same circuit. Go home
                    logging.debug(f"boxes [{box1},{box2}] are in the same group {box1_gid}")
                    continue
                else: # group merge
                    logging.debug(f"doing a group join between [{box1},{box2}]; joining contents of {box2_gid} to {box1_gid}")
                    circuit_groups[box1_gid] = list(set(circuit_groups[box1_gid] + circuit_groups[box2_gid]))
                    del circuit_groups[box2_gid]
            else:
                group_id += 1
                circuit_groups[group_id] = [box1,box2]
                junction_map[box2],junction_map[box1] = True,True
                logging.debug(f"Added new group [{box1},{box2}] with gid {group_id}")
        else: # one or the other connected
            logging.debug(f"One box already connected: box1:{box1}: {junction_map[box1]}, box2:{box2}: {junction_map[box2]}")
            if junction_map[box1]: # box1 connected
                for gid,group_list in circuit_groups.items():
                    if box1 in group_list:
                        circuit_groups[gid].append(box2)
                        junction_map[box2] = True
                        logging.debug(f"Added {box2}: to gid {gid}")
                        break
            else: # box 2 connected
                for gid,group_list in circuit_groups.items():
                    if box2 in group_list:
                        circuit_groups[gid].append(box1)
                        junction_map[box1] = True
                        logging.debug(f"Added {box1}: to gid {gid}")
                        break
        if len(circuit_groups) == 1 and len(list(circuit_groups.values())[0]) == len(junction_list): # all boxes connected in same group
            if TESTING_STATE:
                logging.debug(f"junction_map after connecting {len(closest_boxes_list)} closest boxes:")
                pprint(junction_map)
                logging.debug("and circuit groups:")
                pprint(circuit_groups)
            return (box1,box2) 
    if TESTING_STATE:
        logging.debug(f"junction_map after connecting {len(closest_boxes_list)} closest boxes:")
        pprint(junction_map)
        logging.debug("and circuit groups:")
        pprint(circuit_groups)
    group_sizes = sorted([len(x) for x in circuit_groups.values()])
    logging.debug(group_sizes)
    return math.prod(group_sizes[-3:])




def main():
    todaySolver = ContextualSolver()
    logging.info(f"Solving Part 1 with starter value {part1}")
    todaySolver.solve(part1)
    logging.info(f"Solving Part 2 with starter value {part2}")
    todaySolver.solve(part2)
    
if __name__ == "__main__":
    main()