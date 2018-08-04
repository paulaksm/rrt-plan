from ProgressionPlanning import ProgressionPlanning
from RRT_Structure import RandomTree
from node import Node
from state import State
import util
import heuristics

class Subplanner(ProgressionPlanning):
 
    def __init__(self, grounded_actions, problem):
        self._problem = problem
        self._grounded_actions = grounded_actions
    
    @property
    def problem(self):
        return self._problem

    @property
    def actions(self):
        return self._grounded_actions


class AStar(Subplanner):

    def solve(self, init_state, goal_state, max_step=10):
        plan = []
        num_explored = 0
        num_generated = 0
        opened = list()
        if isinstance(init_state, RandomTree):
            initialNode = Node(init_state.node)
        else:
            initialNode = Node(init_state)
        frontier = util.PriorityQueue()
        frontier.update(initialNode, initialNode.h + initialNode.g) 
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
                               # heuristics.h_ff(stateSon, self, goal_state))
                               heuristics.h_add_planner(stateSon, self, goal_state)) 
                fSon = nodeSon.g + nodeSon.h
                frontier.update(nodeSon, fSon)
            if frontier.isEmpty():
                print ('Problem does not have a solution')
                return None
        plan = sNode.path() 
        return (sNode.state, plan, reached)

class WAStar(Subplanner):

    def __init__(self, grounded_actions, problem, weight):
        super(WAStar, self).__init__(grounded_actions, problem)
        self._weight = weight

    @property
    def W(self):
        return self._weight

    def solve(self, init_state, goal_state, max_step=1000):
        plan = []
        num_explored = 0
        num_generated = 0
        opened = list()
        if isinstance(init_state, RandomTree):
            initialNode = Node(State(init_state.node))
        else:
            initialNode = Node(State(init_state))
        frontier = util.FrontierPriorityQueueWithFunction(lambda searchNode:(searchNode.g + self.W*searchNode.h))
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
                frontier.push(nodeSon)
            if frontier.is_empty():
                print ('Problem does not have a solution')
                return None
        plan = sNode.path() 
        return (sNode.state, plan, reached)

class EHC(Subplanner):

    def solve(self, init_state, goal_state, max_step=10):
        plan = []      
        state = State(init_state.node)
        h_state = heuristics.h_ff(state, self, goal_state)
        iteration = 0
        while h_state != 0 and iteration < max_step:
            best_state, plan_to_best = self._bfs_ehs(state, goal_state, h_state)
            if best_state is None:
                return _,_,False # not reached
            plan.extend(plan_to_best)
            h_state = heuristics.h_ff(best_state, self, goal_state)
            state = best_state
            iteration += 1
        if iteration >= max_step:
            return (state, plan, False)
        return (state, plan, True)

    def _bfs_ehs(self, init, goal, h_state):
        plan_queue = util.Queue()
        closed = set()
        # quando der o push na queue, passar um tupla (state, path) <State, List>
        actionsApplicable = self.applicable(init)
        for action in actionsApplicable:
            stateSon = self.successor(init, action)
            plan_queue.push((stateSon, [action]))
        while not plan_queue.isEmpty():
            nxt_state, plan = plan_queue.pop()
            if nxt_state in closed:
                continue
            h_nxt = heuristics.h_ff(nxt_state, self, goal)
            if h_nxt < h_state:
                return (nxt_state, plan)
            actionsApplicable = self.applicable(nxt_state)
            for action in actionsApplicable:
                stateSon = self.successor(nxt_state, action)
                path = plan + [action]
                plan_queue.push((stateSon, path))
            closed.add(nxt_state)
        return (None, [])