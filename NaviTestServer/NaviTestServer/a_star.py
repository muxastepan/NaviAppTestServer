from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from NaviTestServer.models import Node,Point

import math

@dataclass
class AStarNode:
    node:Node
    from_node:Optional[AStarNode]
    heuristics_estimate_path_length: Optional[float]
    neighbors: Optional[list[AStarNode]]

    def __init__(self,node:Node,all_nodes:list[AStarNode]):
        self.node = node
        self.path_length_from_start = None
        self.heuristics_estimate_path_length = None
        self.neighbors = self.get_neighbors(all_nodes)
        self.from_node = None

    def get_neighbors(self,all_nodes:list[AStarNode])->list[AStarNode]:
        self.neighbors = []
        for node in self.node.nodes.all():
            all_nodes.append(self)
            linked_node = next(filter(lambda x: node == x.node,all_nodes),None)
            if linked_node:
                self.neighbors.append(linked_node)
                continue
            self.neighbors.append(AStarNode(node,all_nodes))

        return self.neighbors



class AStar:
    @staticmethod 
    def find_path(start:Node, goal:Node)->list[Point]:
        all_nodes = []
        start_node = AStarNode(start, all_nodes)
        goal_node = AStarNode(goal,all_nodes)
        closed_set = []
        open_set = []
        start_node.heuristics_estimate_path_length = AStar.__get_heuristics_path_length(start_node,goal_node)
        open_set.append(start_node)

        while len(open_set)>0:
            current_node = next(iter(sorted(open_set, key=lambda a: -a.heuristics_estimate_path_length)),None)
            if current_node.node == goal:
                return AStar.__get_path_for_node(current_node,start_node)
            open_set.remove(current_node)
            closed_set.append(current_node)

            for neighbour_node in current_node.neighbors:
                if neighbour_node in closed_set:
                    continue
                open_node = next(filter(lambda node:node==neighbour_node,open_set),None)

                if not open_node:
                    neighbour_node.heuristics_estimate_path_length = AStar.__get_heuristics_path_length(current_node, neighbour_node)
                    neighbour_node.from_node = current_node
                    open_set.append(neighbour_node)
                
                elif (AStar.__get_heuristics_path_length(current_node, open_node) 
                      < open_node.heuristics_estimate_path_length):
                    open_node.from_node = current_node

        return None

    
    @staticmethod
    def __get_path_for_node(path_node:AStarNode,start_node:AStarNode)->list[Point]:
        result_nodes = []
        current_node = path_node

        while(current_node):
            if (path_node == current_node.from_node or current_node == start_node):
                break
            result_nodes.append(current_node)
            current_node = current_node.from_node
        
        result_nodes.append(start_node)
        result_nodes.reverse()

        points = []
        for node in result_nodes:
            points.append(node.node.point)
        return points
        

    @staticmethod
    def __get_heuristics_path_length(start:AStarNode,end:AStarNode)->float:
        return math.sqrt((end.node.point.x - start.node.point.x)**2 + (end.node.point.y - start.node.point.y)**2)