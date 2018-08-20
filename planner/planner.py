import util
import random
from state import State
from node  import Node
import heuristics
#import numpy as np
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
        closer = float("inf")
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
            q_new, path, reached = planner.solve(q_near, q_rand, max_step=50)       
            if not reached:
                continue           
            qnew_cost = heuristics.h_add(self, q_new) # q_new is a set of atoms (state)
            qnew_node = RandomTree(q_new, q_near, cost=qnew_cost, edge=path)
            node_tree.add(qnew_node)
            q_goal, path, reached = planner.solve(qnew_node, State(self.problem.goal))
            if reached:
                full_rgs = True
                print('Goal found')
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

    def solve_log(self):
        # Initializing tree and set of nodes
        node_tree = set()
        init_state = self.problem.init
        root_node = RandomTree(init_state)
        node_tree.add(root_node)
        root_node.cost = heuristics.h_add(self, init_state)
        full_rgs = False # full random goal subset
        qrand_list = []
        planner = EHC(self.actions, self.problem) # subplanner of choice

        file_name  = 'log_{}_{}.txt'.format(self.problem.domain, self.problem.name)
        file = open(file_name, 'w+')
        file.write('LOG FILE -- RRT-Plan\n')
        file.write('\nGoal Atoms -> {}\n'.format(self.problem.goal))
        iteration = 1
        while not full_rgs:
            q_rand = self.sample_random()
            # i = len(q_rand)
            log_info = '>>> ITERATION N. {} <<<\n'.format(iteration)
            qrand_list.append(q_rand)
            q_near = self.nearest_neighbor(q_rand, node_tree)
            q_new, path, reached = planner.solve(q_near, q_rand, max_step=30)       
            log_info += '[{}] SAMPLE --- max_steps: {}\n'.format(reached, 30)
            log_info += '\nSAMPLED ATOMS -> {}\n'.format(set(q_rand))
            log_info += '\nSUB-PATH -> {}\n'.format(path)
            log_info += '\nNEAR ABSTRACT STATE -> {}\n'.format(set(q_near.node))
            if not reached:
                iteration += 1
                file.write('\n{}\n'.format(log_info))
                continue           
            qnew_cost = heuristics.h_add(self, q_new) # q_new is a set of atoms (state)
            qnew_node = RandomTree(q_new, q_near, cost=qnew_cost, edge=path)
            node_tree.add(qnew_node)
            q_goal, path, reached = planner.solve(qnew_node, State(self.problem.goal))
            log_info += '\nCONNECT TO GOAL --- max_steps: {}\n -> {}\n'.format(10, set(q_goal))
            if reached:
                full_rgs = True
                print('Goal found')
            else:
                qnew_cost = heuristics.h_add(self, q_goal)
                qnew_node = RandomTree(q_goal, qnew_node, cost=qnew_cost, edge=path)
                node_tree.add(qnew_node)
            iteration += 1
            file.write('\n{}\n'.format(log_info))
        state = qnew_node
        last_path = path
        path = []
        while state is not None:
            path[:0] = state.edge
            state = state.parent_node
        path.extend(last_path)
        validator_plan = ''
        for act in path:
            validator_plan += act.validator_format()
        file.close()
        file_name  = 'plan_{}_{}.txt'.format(self.problem.domain, self.problem.name)
        with open(file_name, 'w+') as file:
            file.write(validator_plan)
        return path, qrand_list

    def solve_graph_plot(self):
        import matplotlib.pyplot as plt
        import networkx as nx
        # Initializing tree and set of nodes  
        node_tree = set()
        init_state = self.problem.init
        root_node = RandomTree(init_state)
        node_tree.add(root_node)
        j = 0
        color_map = []
        graph_dict = dict()
        G = nx.Graph()
        G.add_node(j)
        idx = frozenset(root_node.node)
        graph_dict[idx] = j
        color_map.append('yellow')
        size_goal = len(self.problem.goal)

        root_node.cost = heuristics.h_add(self, init_state)
        full_rgs = False # full random goal subset
        qrand_list = []
        planner = EHC(self.actions, self.problem) # subplanner of choice

        while not full_rgs:
            q_rand = self.sample_random()

            i = len(q_rand)

            qrand_list.append(q_rand)
            q_near = self.nearest_neighbor(q_rand, node_tree)
            q_new, path, reached = planner.solve(q_near, q_rand, max_step=10)      
            if not reached:
                continue
            j += 1
            G.add_node(j)
            idx = frozenset(set(q_new))
            fidx = graph_dict.get(frozenset(q_near.node))
            graph_dict[idx] = j
            color_map.append('blue')
            G.add_edge(fidx, j, r='RGS:{}/{}'.format(i, size_goal))

            qnew_cost = heuristics.h_add(self, q_new) # q_new is a set of atoms (state)
            qnew_node = RandomTree(q_new, q_near, cost=qnew_cost, edge=path)
            node_tree.add(qnew_node)
            q_goal, path, reached = planner.solve(qnew_node, State(self.problem.goal))
            if reached:
                full_rgs = True

                j += 1
                G.add_node(j)
                color_map.append('red')
                idx = frozenset(set(q_goal))
                fidx = graph_dict.get(frozenset(qnew_node.node))
                graph_dict[idx] = j
                G.add_edge(fidx, j, r='final')

                print('Goal found')
            # codigo do else pode ser comentado...a performance foi boa sem adicionar esse no resultante da busca qNew -> goal
            else:
                j += 1
                G.add_node(j)
                color_map.append('green')
                idx = frozenset(set(q_goal))
                fidx = graph_dict.get(frozenset(qnew_node.node))
                graph_dict[idx] = j
                G.add_edge(fidx, j, r='ext.')

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
        validator_plan = ''
        for act in path:
            validator_plan += act.validator_format()
        file_name  = 'plan_{}_{}.txt'.format(self.problem.domain, self.problem.name)
        with open(file_name, 'w+') as file:
            file.write(validator_plan)

        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=300, node_color=color_map, with_labels=True, font_weight='bold')
        nx.draw_networkx_edges(G,pos,edge_color='black')
        edge_labels = nx.get_edge_attributes(G,'r')
        nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.axis('off')
        plt.savefig('fig_{}_{}.png'.format(self.problem.domain, self.problem.name))
        return path, qrand_list

    def solve_log_plot(self):
        # Initializing tree and set of nodes
        import matplotlib.pyplot as plt
        import networkx as nx
        node_tree = set()
        init_state = self.problem.init
        root_node = RandomTree(init_state)
        node_tree.add(root_node)
        j = 0
        color_map = []
        graph_dict = dict()
        G = nx.Graph()
        G.add_node(j)
        idx = frozenset(root_node.node)
        graph_dict[idx] = j
        color_map.append('yellow')
        size_goal = len(self.problem.goal)
        root_node.cost = heuristics.h_add(self, init_state)
        full_rgs = False # full random goal subset
        qrand_list = []
        planner = EHC(self.actions, self.problem) # subplanner of choice

        file_name  = 'log_{}_{}.txt'.format(self.problem.domain, self.problem.name)
        file = open(file_name, 'w+')
        file.write('LOG FILE -- RRT-Plan\n')
        file.write('\nGoal Atoms -> {}\n'.format(self.problem.goal))
        iteration = 1
        while not full_rgs:
            q_rand = self.sample_random()
            i = len(q_rand)
            log_info = '>>> ITERATION N. {} <<<\n'.format(iteration)
            qrand_list.append(q_rand)
            q_near = self.nearest_neighbor(q_rand, node_tree)
            q_new, path, reached = planner.solve(q_near, q_rand, max_step=10)       
            log_info += '[{}] SAMPLE --- max_steps: {}\n'.format(reached, 10)
            log_info += '\nSAMPLED ATOMS -> {}\n'.format(set(q_rand))
            log_info += '\nSUB-PATH -> {}\n'.format(path)
            log_info += '\nNEAR ABSTRACT STATE -> {}\n'.format(set(q_near.node))
            if not reached:
                iteration += 1
                file.write('\n{}\n'.format(log_info))
                continue           
            j += 1
            G.add_node(j)
            idx = frozenset(set(q_new))
            fidx = graph_dict.get(frozenset(q_near.node))
            graph_dict[idx] = j
            color_map.append('blue')
            G.add_edge(fidx, j, r='RGS:{}/{}'.format(i, size_goal))

            qnew_cost = heuristics.h_add(self, q_new) # q_new is a set of atoms (state)
            qnew_node = RandomTree(q_new, q_near, cost=qnew_cost, edge=path)
            node_tree.add(qnew_node)
            q_goal, path, reached = planner.solve(qnew_node, State(self.problem.goal))
            log_info += '\nCONNECT TO GOAL --- max_steps: {}\n -> {}\n'.format(10, set(q_goal))
            if reached:
                full_rgs = True
                j += 1
                G.add_node(j)
                color_map.append('red')
                idx = frozenset(set(q_goal))
                fidx = graph_dict.get(frozenset(qnew_node.node))
                graph_dict[idx] = j
                G.add_edge(fidx, j, r='final')
                print('Goal found')
            else:
                j += 1
                G.add_node(j)
                color_map.append('green')
                idx = frozenset(set(q_goal))
                fidx = graph_dict.get(frozenset(qnew_node.node))
                graph_dict[idx] = j
                G.add_edge(fidx, j, r='ext.')
                qnew_cost = heuristics.h_add(self, q_goal)
                qnew_node = RandomTree(q_goal, qnew_node, cost=qnew_cost, edge=path)
                node_tree.add(qnew_node)
            iteration += 1
            file.write('\n{}\n'.format(log_info))
        state = qnew_node
        last_path = path
        path = []
        while state is not None:
            path[:0] = state.edge
            state = state.parent_node
        path.extend(last_path)
        validator_plan = ''
        for act in path:
            validator_plan += act.validator_format()
        file.close()
        file_name  = 'plan_{}_{}.txt'.format(self.problem.domain, self.problem.name)
        with open(file_name, 'w+') as file:
            file.write(validator_plan)
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=300, node_color=color_map, with_labels=True, font_weight='bold')
        nx.draw_networkx_edges(G,pos,edge_color='black')
        edge_labels = nx.get_edge_attributes(G,'r')
        nx.draw_networkx_labels(G,pos,font_size=10,font_family='sans-serif')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.axis('off')
        plt.savefig('fig_{}_{}.png'.format(self.problem.domain, self.problem.name))
        return path, qrand_list
