#!/usr/bin/python3
import logging
import sys
from io import IOBase
#import re 
#import math
from dataclasses import dataclass
from pprint import pprint
#import itertools


TESTING_STATE = False
SUBMIT = True
logging_level = logging.DEBUG if TESTING_STATE else logging.INFO
logging.basicConfig(level=logging_level)
part1 = 1
part2 = 2

# custom constants


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
        nodes_dict = {line.split(':')[0]:line.split(':')[1].strip().split() for line in processed_input}
        # logging.debug("Nodes")
        # pprint(nodes_dict)
        root = populateTree("out",nodes_dict,"you") 
        solution = root.allPathsFromNode() if starter_val == part1 else partTwoSolution(nodes_dict)
        #logging.debug(root)
        #logging.debug(f"paths: {root.paths_from_here}, dac downstream: {root.dac_downstream}")
        return solution
    
    def testInput(self,solution:int,starter_val:int) -> bool:
        if starter_val == part1:
            return solution == 5 # expected result of part 1 test
        return solution == 2 # expected result of part 2 test

class DeviceNode:
    def __init__(self, name, children):
        self.name: str = name
        self.children: list = children
        self.paths_from_here = 0
        self.dac_downstream = name == "dac"
        self.fft_downstream = name == "fft"

    def __repr__(self):
        return str(self.name) + str(self.children)
    
    def allPathsFromNode(self) -> int:
        #logging.debug(f"node:{self.name} children: {self.children}")
        if self.children == [None]:
            return 1
        else:
            self.paths_from_here = sum([child.allPathsFromNode() if child is not None else 1 for child in self.children ])
            logging.debug(f"node:{self.name}; paths from here: {self.paths_from_here} ")
            return self.paths_from_here
        
def populateTree(bottom_node:str,nodes_dict:dict,node_name:str,filter:list=[]) -> DeviceNode:
    # if node_name not in nodes_dict.keys():
    #     return []
    if node_name == bottom_node:
        return None
    child_str_list = nodes_dict[node_name] if filter == [] else [x for x in nodes_dict[node_name] if x in filter]
    children_list = [populateTree(bottom_node,nodes_dict,x,filter) for x in child_str_list]
    return DeviceNode(node_name,children_list)

def findParents(search_node:str,node_dict:dict) -> list[str]:
    parents = []
    for k,v in node_dict.items():
        if search_node in v:
            parents.append(k)
    return parents

def twoWayTraversal(bottom_node:str,top_node:str,node_dict:dict) -> list[str]:
    next_layer = findParents(bottom_node,node_dict)
    #logging.debug(f"Staring node: {bottom_node}, starting parent: {next_layer}")
    #find everything upstream of bottom_node
    upward_list = [x for x in next_layer]
    while next_layer != []:
        these_parents = findParents(next_layer.pop(),node_dict)
        for p in these_parents:
            if p not in upward_list: # avoid duplication
                #logging.debug(f"appending {p} to {upward_list}")
                next_layer.append(p) # push not implemented, and insert less efficient
                upward_list.append(p)
    #find everything downstream of top_node that is in upstream list
    next_layer = node_dict[top_node]
    two_way_list = [x for x in next_layer if x in upward_list]
    next_layer = [x for x in two_way_list]
    while next_layer != []:
        these_children = node_dict[next_layer.pop()]
        for c in these_children:
            if c in upward_list and c not in two_way_list: # check validity and avoid duplication
                next_layer.append(c) # push not implemented, and insert less efficient
                two_way_list.append(c)
    logging.debug(f" Two way list between {bottom_node} and {top_node} is {two_way_list}")
    return two_way_list

def findPathsToSource(bottom_node:str,top_node:str,node_dict:dict) -> int:
    traversal_list = twoWayTraversal(bottom_node,top_node,node_dict)
    this_tree = populateTree(bottom_node,node_dict,top_node,traversal_list+[bottom_node,top_node])
    paths = this_tree.allPathsFromNode()
    logging.debug(f"Paths from {bottom_node} to {top_node} are {paths}")
    return paths
    # next_layer = [x for x in findParents(bottom_node,node_dict) if x in traversal_list]
    # paths = len(next_layer)
    # while next_layer != []:
    #     these_parents = []
    #     for p in next_layer:
    #         these_parents += [x for x in findParents(p,node_dict) if x in traversal_list]
    #     paths += len(these_parents)
    #     next_layer = these_parents
    #

def partTwoSolution(node_dict:dict) -> int:
    paths = findPathsToSource("out","dac",node_dict)
    paths *= findPathsToSource("dac","fft",node_dict)
    paths *= findPathsToSource("fft","svr",node_dict)
    return paths

    


def main():
    todaySolver = ContextualSolver()
    logging.info(f"Solving Part 1 with starter value {part1}")
    todaySolver.solve(part1)
    logging.info(f"Solving Part 2 with starter value {part2}")
    todaySolver.solve(part2)
    
if __name__ == "__main__":
    main()