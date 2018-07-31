import util
import random
from state import State
from node  import Node
import heuristics
import numpy as np
from RRT_Structure import RandomTree
from ProgressionPlanning import ProgressionPlanning
from subplanner import AStar, WAStar, EHC

class RRTPlan(ProgressionPlanning):
    '''
    RRT-Plan class
    '''
    def sample_random(self):
        '''
        not taking into account goal orderings, as proposed in agenda-driven planning algorithms
        '''
        goal_set = self.problem.goal
        num_samples = random.randint(1, len(goal_set))
        sample_goal = random.sample(goal_set, num_samples)
        # return set(sample_goal)
        return State(sample_goal)

    def nearest_neighbor(self, state, tree_set):
        near = None
        closer = np.inf
        for node in tree_set:
            distance = sum(node.cost[p] for p in state)
            if distance < closer:
                closer = distance
                near = node
        return near 

    def solve(self):
        # Initializing tree and set of nodes
        node_tree = set()
        init_state = self.problem.init
        root_node = RandomTree(init_state)
        node_tree.add(root_node)
        root_node.cost = heuristics.h_add(self, init_state)
        full_rgs = False # full random goal subset
        qrand_list = []
        planner = EHC(self.actions, self.problem) # subplanner of choice
        while not full_rgs:
            q_rand = self.sample_random()
            qrand_list.append(q_rand)
            q_near = self.nearest_neighbor(q_rand, node_tree)
            q_new, path, reached = planner.solve(q_near, q_rand, max_step=30)
            if not reached:
                continue
            qnew_cost = heuristics.h_add(self, q_new) # q_new is a set of atoms (state)
            qnew_node = RandomTree(q_new, q_near, cost=qnew_cost, edge=path)
            node_tree.add(qnew_node)
            q_goal, path, reached = planner.solve(qnew_node, State(self.problem.goal))
            if reached:
                full_rgs = True
                print('Goal found')
            # codigo do else pode ser comentado...a performance foi boa sem adicionar esse no resultante da busca qNew -> goal
            else:
                qnew_cost = heuristics.h_add(self, q_goal)
                qnew_node = RandomTree(q_goal, qnew_node, cost=qnew_cost, edge=path)
                node_tree.add(qnew_node)
        state = qnew_node
        last_path = path
        path = []
        while state is not None:
            path[:0] = state.edge
            state = state.parent_node
        path.extend(last_path)
        return path, qrand_list
