import util
import random
from state import State
from node  import Node
import heuristics
import numpy as np
from RRT_Structure import RandomTree

class Frontier(object):
    '''
    Frontier class implement a search frontier using a
    PriorityQueue for ordering the nodes and a set for
    constant-time checks of states in frontier.

    OBSERVATION: it receives as input a function `f` that
    itself receives a node and returns the priority for
    the given node. Check util.PriorityQueueWithFunction for
    more details.
    '''

    def __init__(self, f):
        self._queue = util.PriorityQueueWithFunction(f)
        self._set = set()

    def __contains__(self, node):
        ''' Return true if `node.state` is in the frontier. '''
        return node.state in self._set

    def __len__(self):
        ''' Return the number of nodes in frontier. '''
        assert(len(self._queue) == len(self._set))
        return len(self._queue)

    def is_empty(self):
        ''' Return true if frontier is empty. '''
        return self._queue.isEmpty()

    def push(self, node):
        ''' Push `node` to frontier. '''
        self._queue.push(node)
        self._set.add(node.state)

    def pop(self):
        ''' Pop `node` from frontier. '''
        node = self._queue.pop()
        self._set.discard(node.state) # antes era remove
        return node

    def __str__(self):
        ''' Return string representation of frontier. '''
        return str(self._queue)

class ProgressionPlanning(object):
    '''
    ProgressionPlanning class implements all necessary components
    for implicitly generating the state space in a forward way (i.e., by progression).self
    '''

    def __init__(self, domain, problem):
        self._problem = problem
        self._all_actions = problem.ground_all_actions(domain)

    @property
    def problem(self):
        return self._problem

    @property
    def actions(self):
        return self._all_actions

    def applicable(self, state):
        ''' Return a list of applicable actions in a given `state`. '''
        app = list()
        for act in self.actions:
            if State(state).intersect(act.precond) == act.precond:
                app.append(act)
        return app

    def successor(self, state, action):
        ''' Return the sucessor state generated by executing `action` in `state`. '''
        return State(action.pos_effect).union(State(state).difference(action.neg_effect))

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
        while not full_rgs:
            q_rand = self.sample_random()
            qrand_list.append(q_rand)
            q_near = self.nearest_neighbor(q_rand, node_tree)
            q_new, path, reached = self.subplanner(q_near, q_rand, max_step=1000)
            # q_new, path, reached = self.subplanner(q_near, q_rand, max_step=30)
            if not reached:
                continue
            qnew_cost = heuristics.h_add(self, q_new) # q_new is a set of atoms (state)
            qnew_node = RandomTree(q_new, q_near, cost=qnew_cost, edge=path)
            node_tree.add(qnew_node)
            q_goal, path, reached = self.subplanner(qnew_node, State(self.problem.goal))
            # q_goal, path, reached = self.subplanner(qnew_node, State(self.problem.goal))
            if reached:
                full_rgs = True
                #print(q_goal, self.problem.goal)
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
            path.extend(state.edge)
            state = state.parent_node
        path.extend(last_path)
        # print('Init: ', init_state)
        # print('Goal: ', self.problem.goal)
        # print('Plan: ', path)
        return path, qrand_list

    def subplanner(self, init_state, goal_state, max_step=10):
        '''
        OBSERVATION: a state is 'explored' when it is removed from the frontier and
        a state is 'generated' when it is the successor state generated by an action
        regardless whether or not it is in the explored set or already in the frontier.

        init (nao eh) and goal are State objects
        return last state and plan to this state
        '''
        plan = []
        num_explored = 0
        num_generated = 0
        opened = list()
        if isinstance(init_state, RandomTree):
            initialNode = Node(init_state.node)
        else:
            initialNode = Node(init_state)
        frontier = util.PriorityQueue()
        frontier.update(initialNode, initialNode.h + initialNode.g) # antes initialNode.g
        reached = False
        for i in range(max_step):
            sNode = frontier.pop()
            opened.append(sNode.state)
            if goal_state.intersect(sNode.state) == goal_state:
                reached = True
                break
            actionsApplicable = self.applicable(sNode.state)
            for action in actionsApplicable:
                stateSon = self.successor(sNode.state, action)
                if stateSon in opened:
                    continue
                nodeSon = Node(stateSon,
                               action,
                               sNode,
                               sNode.g + 1,
                               heuristics.h_add_planner(stateSon, self, goal_state)) 
                fSon = nodeSon.g + nodeSon.h
                frontier.update(nodeSon, fSon)
            if frontier.isEmpty():
                print ('Problem does not have a solution')
                return None
        plan = sNode.path() # talvez dar um ´ultimo pop na fronteira
        return (sNode.state, plan, reached)
        #return (plan, num_explored, num_generated)

    def subplannerWA(self, init_state, goal_state, max_step=1000, W=3):
        '''
        OBSERVATION: a state is 'explored' when it is removed from the frontier and
        a state is 'generated' when it is the successor state generated by an action
        regardless whether or not it is in the explored set or already in the frontier.

        init (nao eh) and goal are State objects
        return last state and plan to this state
        '''
        plan = []
        num_explored = 0
        num_generated = 0
        opened = list()
        if isinstance(init_state, RandomTree):
            initialNode = Node(State(init_state.node))
        else:
            initialNode = Node(State(init_state))
        frontier = Frontier(lambda searchNode:(searchNode.g + W*searchNode.h))
        frontier.push(initialNode)
        reached = False
        for i in range(max_step):
            sNode = frontier.pop()
            opened.append(sNode.state)
            if goal_state.intersect(sNode.state) == goal_state:
                reached = True
                break
            actionsApplicable = self.applicable(sNode.state)
            for action in actionsApplicable:
                stateSon = self.successor(sNode.state, action)
                if stateSon in opened:
                    continue
                nodeSon = Node(stateSon,
                               action,
                               sNode,
                               sNode.g + 1,
                               heuristics.h_add_planner(stateSon, self, goal_state)) 
                # fSon = nodeSon.g + nodeSon.h
                frontier.push(nodeSon)
            if frontier.is_empty():
                print ('Problem does not have a solution')
                return None
        plan = sNode.path() # talvez dar um ´ultimo pop na fronteira
        return (sNode.state, plan, reached)
